from pydantic import BaseModel, Field, EmailStr, AnyUrl
from pydantic_settings import BaseSettings


class Settings(BaseSettings):
    # SendGrid settings
    SENDGRID_API_KEY: str = Field(..., env='SENDGRID_API_KEY')
    SENDGRID_FROM_EMAIL: str = Field(..., env='SENDGRID_FROM_EMAIL')
    
    # Twilio settings
    TWILIO_ACCOUNT_SID: str = Field(..., env='TWILIO_ACCOUNT_SID')
    TWILIO_AUTH_TOKEN: str = Field(..., env='TWILIO_AUTH_TOKEN')
    TWILIO_FROM_NUMBER: str = Field(..., env='TWILIO_FROM_NUMBER')
    
    # API Key for internal service authentication
    INTERNAL_API_KEY: str = Field(..., env='INTERNAL_API_KEY')

    # Email settings
    EMAIL_FROM: EmailStr = Field(..., env='EMAIL_FROM')
    EMAIL_BACKEND: str = Field(default='sendgrid', env='EMAIL_BACKEND')
    MAIL_USERNAME: str = Field(..., env='MAIL_USERNAME')
    MAIL_PASSWORD: str = Field(..., env='MAIL_PASSWORD')
    MAIL_FROM: EmailStr = Field(..., env='MAIL_FROM')
    MAIL_PORT: int = Field(default=587, env='MAIL_PORT')
    MAIL_SERVER: str = Field(..., env='MAIL_SERVER')
    MAIL_TLS: bool = Field(default=True, env='MAIL_TLS')
    MAIL_SSL: bool = Field(default=False, env='MAIL_SSL')
    MAIL_FROM_NAME: str = Field(..., env='MAIL_FROM_NAME')

    class Config:
        env_file = ".env.dev"
        env_file_encoding = 'utf-8'

settings = Settings()