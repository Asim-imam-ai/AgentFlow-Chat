from fastapi import APIRouter
from app.api.schemas.response import GenericResponse

router = APIRouter(tags=["Health"])

@router.get("/health", response_model=GenericResponse)
async def health_check():
    """
    Health check endpoint to verify the server status.
    """
    return GenericResponse(
        success=True,
        message="AgentFlow Chat API is healthy and running.",
        data={"status": "online"}
    )
