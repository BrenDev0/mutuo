import bcrypt
import hashlib
from ..services import HashingService

class BcryptHashingService(HashingService):
    def hash_for_search(self, data: str) -> str:
        email_bytes = data.lower().encode('utf-8')  
        hashed_data = hashlib.sha256(email_bytes).hexdigest()
        return hashed_data

    def hash(self, password: str) -> str:
        salt = bcrypt.gensalt()
        hashed = bcrypt.hashpw(password.encode('utf-8'), salt)
        return hashed.decode('utf-8')

    def compare(
        self,
        unhashed: str, 
        hashed: str,
    ) -> bool:
        return bcrypt.checkpw(unhashed.encode('utf-8'), hashed.encode('utf-8'))
            