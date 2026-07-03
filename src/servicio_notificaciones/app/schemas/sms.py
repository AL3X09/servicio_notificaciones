from pydantic import BaseModel, validator
import re

class SMSSchema(BaseModel):
    to_number: str
    message_body: str

    @validator('to_number')
    def validate_phone_number(cls, v):
        # Colombia: +57 seguido de 10 dígitos (celular: 3XXXXXXXXX)
        if not re.match(r'^\+57[3][0-9]{9}$', v):
            raise ValueError(
                'El número debe ser colombiano en formato E.164 (ej: +573011234567)'
            )
        return v

    class Config:
        json_schema_extra = {
            "example": {
                "to_number": "+573011234567",
                "message_body": "Hola desde Twilio!"
            }
        }