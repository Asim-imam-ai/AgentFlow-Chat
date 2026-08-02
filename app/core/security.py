from fastapi import HTTPException, Security, status
from fastapi.security import APIKeyHeader

from app.core.settings import settings

API_KEY_NAME = "X-API-Key"
api_key_header = APIKeyHeader(name=API_KEY_NAME, auto_error=False)


async def get_api_key(api_key: str = Security(api_key_header)):
    # Simple api key verification if keys are set
    # In production, we'd check dynamic keys or JWT tokens
    if settings.DEBUG:
        return "debug-mode"

    if not api_key:
        raise HTTPException(
            status_code=status.HTTP_403_FORBIDDEN,
            detail="API Key missing",
        )

    # We can validate against settings.SECRET_KEY or standard client tokens
    if api_key != settings.SECRET_KEY:
        raise HTTPException(
            status_code=status.HTTP_403_FORBIDDEN,
            detail="Invalid API Key",
        )
    return api_key
