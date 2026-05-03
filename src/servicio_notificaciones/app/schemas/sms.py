from pydantic import BaseModel, validator
import re

class SMSSchema(BaseModel):
    to_number: str
    message_body: str

    @validator('to_number')
    def validate_phone_number(cls, v):
        # Simple validation for phone number (E.164 format)
        if not re.match(r'^\+[1-9]\d{1,14}$', v):
            raise ValueError('Phone number must be in E.164 format (e.g., +1234567890)')
        return v

    class Config:
        json_schema_extra = {
            "example": {
                "to_number": "+1234567890",
                "message_body": "Hello from Twilio!"
            }
        }