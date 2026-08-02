from pydantic import BaseModel, Field
from typing import Optional, Any

class GenericResponse(BaseModel):
    success: bool = Field(..., description="Flag indicating if the request was successful.")
    message: str = Field(..., description="Informative status message.")
    data: Optional[Any] = Field(None, description="Optional payload returned by the operation.")
