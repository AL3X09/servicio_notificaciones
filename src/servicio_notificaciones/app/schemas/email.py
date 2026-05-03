from pydantic import BaseModel, EmailStr

class EmailSchema(BaseModel):
    to_email: EmailStr
    subject: str
    html_content: str

    class Config:
        json_schema_extra = {
            "example": {
                "to_email": "usuario@ejemplo.com",
                "subject": "Hola Mundo",
                "html_content": "<p>¡Hola, Mundo!</p>"
            }
        }