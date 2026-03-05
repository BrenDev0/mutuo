from pathlib import Path
import os
import json
from src.security import get_random_code, EncryptionService, HashingService
from src.persistence import CollisionException, AsyncSessionRepository
from src.communications import Email, EmailService
from ..rules import EmailAvailability

class VerifyEmail:
    """Send verification code to users email for user registration"""
    def __init__(
        self,
        encryption: EncryptionService,
        hashing: HashingService,
        session_repository: AsyncSessionRepository,
        email_service: EmailService,
        email_availible_rule: EmailAvailability
    ):
        _from_addr = os.getenv("MAILER_USER")

        if not _from_addr:
            raise ValueError("Email variables not set")
        
        self._from_addr = _from_addr
        self._subject = "Verificar Correo Electrónico"

        self._email_service = email_service
        self._email_available_rule = email_availible_rule
        
        self._encryption = encryption
        self._hashing = hashing
        self._session_repository = session_repository

    def __build_email( 
        self,
        to: str,
        verification_code: int
    ) -> Email:
        """
        Build email

        Args:
            to: Email to send to,
            verification_code: random generated code to be sent to email

        Returns:
            Email: Object for smpt
        """
        template_path = Path(__file__).parent / "template.html"

        with open(template_path, 'r', encoding="utf-8") as f:
            template = f.read()
        
        email_body = template.replace('{{verification_code}}', str(verification_code))
        
        return Email(
            sender=self._from_addr,
            recipient=to,
            subject=self._subject,
            html=str(email_body)
        )
    
    async def execute(
        self,
        to: str
    ):
        """
        Execute the use case 

        Args:
            to: email address to receive verifiaction email

        Returns:
            str: Webtoken that contains the verification code for frontend 

        Raises:
            CollisionException: If email is already in use
        """
        email_hash = self._hashing.hash_for_search(data=to)
        email_available = await self._email_available_rule.validate(email_hash=email_hash)

        if not email_available:
            raise CollisionException(
                detail="Email in use",
                status_code=409
            )
        
        verification_code = get_random_code()

        email = self.__build_email(
            to=to,
            verification_code=verification_code
        )

        self._email_service.send_email(
            email=email
        )

        session_data = {
            "verification_code": self._encryption.encrypt(verification_code),
            "attempts": 0
        }

        await self._session_repository.set_session(
            key=f"verification:{email_hash}",
            value=json.dumps(session_data),
            expire_seconds=900
        )

        
        

        