from twilio.rest import Client
from ..core.config import settings

class ServicioSMS:
    def __init__(self):
        self.cliente = Client(settings.TWILIO_ACCOUNT_SID, settings.TWILIO_AUTH_TOKEN)
        self.numero_desde = settings.TWILIO_FROM_NUMBER

    async def enviar_sms(self, numero_para: str, cuerpo_mensaje: str):
        """
        Envía un SMS utilizando Twilio.
        """
        try:
            mensaje = self.cliente.messages.create(
                body=cuerpo_mensaje,
                from_=self.numero_desde,
                to=numero_para
            )
            return {
                "sid": mensaje.sid,
                "estado": mensaje.status,
                "para": mensaje.to,
                "desde": mensaje.from_
            }
        except Exception as e:
            # Dejaremos que la excepción sea manejada por quien llama (ruta)
            raise e