from fastapi import APIRouter, Depends, HTTPException, status
from ...services.sms_service import ServicioSMS
from ...schemas.sms import SMSSchema
from ...core.security import get_api_key

router = APIRouter(
    prefix="/sms",
    tags=["sms"],
    responses={404: {"description": "No encontrado"}},
)

@router.post(
    "/enviar",
    status_code=status.HTTP_202_ACCEPTED,
    summary="Enviar un SMS",
    description="Envía un SMS utilizando Twilio. Requiere API Key en el encabezado.",
    response_description="SMS aceptado para envío",
)
async def enviar_sms(
    sms_data: SMSSchema,
    api_key: str = Depends(get_api_key)
):
    """
    Endpoint para enviar un SMS.
    """
    #print(f"rere recibida: {sms_data}")
    #print(f"API Key recibida: {api_key}")
    sms_service = ServicioSMS()
    try:
        resultado = await sms_service.enviar_sms(
            numero_para=sms_data.to_number,
            cuerpo_mensaje=sms_data.message_body
        )
        return {
            "mensaje": "SMS aceptado para envío",
            "detalles": resultado
        }
    except Exception as e:
        raise HTTPException(
            status_code=status.HTTP_500_INTERNAL_SERVER_ERROR,
            detail=f"Error al enviar SMS: {str(e)}"
        )