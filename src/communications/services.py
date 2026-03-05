import os
import smtplib
from email.message import EmailMessage
from .models import Email

class EmailService:
    def __init__(self):
        host = os.getenv("MAILER_HOST")
        port = int(os.getenv("MAILER_PORT", 587))
        user = os.getenv("MAILER_USER")
        password = os.getenv("MAILER_PASSWORD")
        from_addr = os.getenv("MAILER_USER")
        if not all([host, port, user, password, from_addr]):
            raise ValueError("smtp variables not set")
        
        self._host = host
        self._port = port
        self._user = user
        self._password = password
        self._from_addr = from_addr


    def send_email(
        self,
        email: Email
    ):
        msg = EmailMessage()
        msg["From"] = email.sender
        msg["To"] = email.recipient
        msg["Subject"] = email.subject
        msg.set_content(email.html, subtype="html")
        msg["X-Mailgun-Track"] = "no"

        try:
            with smtplib.SMTP(self._host, self._port) as server:
                server.starttls()
                server.login(self._user, self._password)
                server.send_message(msg)
                
        except Exception:
            raise 