from fastapi import FastAPI
from .api.routes import email, sms

app = FastAPI(
    title="Servicio de Notificaciones API",
    description="Un servicio backend para enviar emails y SMS utilizando SendGrid y Twilio.",
    version="1.0.0",
)

# Incluir los routers
app.include_router(email.router)
app.include_router(sms.router)

@app.get("/", tags=["raíz"])
async def raíz():
    return {"mensaje": "Bienvenido al Servicio de Notificaciones API"}