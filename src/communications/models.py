from pydantic import BaseModel

class Email(BaseModel):
    sender: str
    recipient: str
    subject: str
    html: str