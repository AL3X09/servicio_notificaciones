import sys

import sendgrid
from sendgrid.helpers.mail import Mail
from fastapi_mail import FastMail, MessageSchema, ConnectionConfig
from ..core.config import settings


class ServicioEmail:
    def __init__(self):
        # Inicializar cliente SendGrid siempre (para backward compatibility)
        self.sg = sendgrid.SendGridAPIClient(api_key=settings.SENDGRID_API_KEY)
        self.email_desde = settings.SENDGRID_FROM_EMAIL
        self.email_backend = settings.EMAIL_BACKEND
        
        # Configuración de FastMail para SMTP
        self.mail_config = ConnectionConfig(
            MAIL_USERNAME=settings.MAIL_USERNAME,
            MAIL_PASSWORD=settings.MAIL_PASSWORD,
            MAIL_FROM=settings.MAIL_FROM,
            MAIL_PORT=settings.MAIL_PORT,
            MAIL_SERVER=settings.MAIL_SERVER,
            MAIL_STARTTLS=settings.MAIL_TLS,
            MAIL_SSL_TLS=settings.MAIL_SSL,
            MAIL_FROM_NAME=settings.MAIL_FROM_NAME,
            USE_CREDENTIALS=True,
            VALIDATE_CERTS=True,
            TIMEOUT=30
        )
        self.fm = FastMail(self.mail_config)

    async def enviar_email(self, para_email: str, asunto: str, contenido_html: str):
        """
        Envía un email utilizando el backend configurado (SendGrid o SMTP).
        """
        # Seleccionar backend basado en configuración
        if self.email_backend == "smtp":
            return await self._enviar_email_smtp(para_email, asunto, contenido_html)
        else:
            # Por defecto usar SendGrid
            return await self._enviar_email_sendgrid(para_email, asunto, contenido_html)

    async def _enviar_email_sendgrid(self, para_email: str, asunto: str, contenido_html: str):
        """
        Envía email usando SendGrid API.
        """
        mensaje = Mail(
            from_email=self.email_desde,
            to_emails=para_email,
            subject=asunto,
            html_content=contenido_html
        )
        try:
            respuesta = self.sg.send(mensaje)
            return {
                "codigo_estado": respuesta.status_code,
                "cuerpo": respuesta.body,
                "encabezados": respuesta.headers
            }
        except Exception as e:
            print(f"Error al enviar email con SendGrid para {para_email}: {str(e)}", file=sys.stderr)
            raise e

    async def _enviar_email_smtp(self, para_email: str, asunto: str, contenido_html: str):
        """
        Envía email usando servidor SMTP con FastMail.
        """
        try:
            # Crear mensaje usando MessageSchema de FastMail
            mensaje = MessageSchema(
                subject=asunto,
                recipients=[para_email],
                body=contenido_html,
                subtype="html"
            )
            
            # Enviar usando FastMail
            await self.fm.send_message(mensaje)
            
            return {
                "codigo_estado": 250,
                "cuerpo": "Email enviado exitosamente",
                "encabezados": {}
            }
        except Exception as e:
            print(f"Error al enviar email con SMTP para {para_email}: {str(e)}", file=sys.stderr)
            raise e

    async def send_checkout_email(self, para_email: str, asunto: str, contenido_html: str):
        """
        Envía email de recibo al finalizar la reserva con el costo total.
        
        Se ejecuta como background task cuando el visitante escanea por segunda vez
        (checkout / salida del parqueadero).
        
        Args:
            para_email: Email del visitante
            asunto: Asunto del email
            contenido_html: Contenido HTML del email
        """
        try:
            # Enviar email usando el backend configurado
            await self.enviar_email(para_email, asunto, contenido_html)
            
        except Exception as e:
            print(f"Error al enviar email de checkout para {para_email}: {str(e)}", file=sys.stderr)
            raise e
