from fastapi import Security, HTTPException, status
from fastapi.security import APIKeyHeader
from .config import settings

# Define API key header
api_key_header = APIKeyHeader(name="X-API-Key", auto_error=False)


async def get_api_key(api_key_header: str = Security(api_key_header)):
    """
    Valida la API key proporcionada en el encabezado X-API-Key.
    """
    if api_key_header is None:
        raise HTTPException(
            status_code=status.HTTP_403_FORBIDDEN,
            detail="No se proporcionó API Key",
        )
    if api_key_header != settings.INTERNAL_API_KEY:
        raise HTTPException(
            status_code=status.HTTP_403_FORBIDDEN,
            detail="API Key inválida",
        )
    return api_key_header