from fastapi import APIRouter, Depends, HTTPException, status
from ...services.email_service import ServicioEmail
from ...schemas.email import EmailSchema
from ...core.security import get_api_key

router = APIRouter(
    prefix="/email",
    tags=["email"],
    responses={404: {"description": "No encontrado"}},
)

@router.post(
    "/enviar",
    status_code=status.HTTP_202_ACCEPTED,
    summary="Enviar un email",
    description="Envía un email utilizando SendGrid. Requiere API Key en el encabezado.",
    response_description="Email aceptado para envío",
)
async def enviar_email(
    email_data: EmailSchema,
    api_key: str = Depends(get_api_key)
):
    """
    Endpoint para enviar un email.
    """
    email_service = ServicioEmail()
    try:
        resultado = await email_service.enviar_email(
            para_email=email_data.to_email,
            asunto=email_data.subject,
            contenido_html=email_data.html_content
        )
        return {
            "mensaje": "Email aceptado para envío",
            "detalles": resultado
        }
    except Exception as e:
        raise HTTPException(
            status_code=status.HTTP_500_INTERNAL_SERVER_ERROR,
            detail=f"Error al enviar email: {str(e)}"
        )