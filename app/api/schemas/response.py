from typing import Any

from pydantic import BaseModel, Field


class GenericResponse(BaseModel):
    success: bool = Field(
        ...,
        description="Flag indicating if the request was successful.",
    )
    message: str = Field(..., description="Informative status message.")
    data: Any | None = Field(
        None,
        description="Optional payload returned by the operation.",
    )
