from pydantic import BaseModel, Field


class UploadResponse(BaseModel):
    filename: str = Field(..., description="The name of the uploaded file.")
    content_type: str = Field(..., description="The media content type of the file.")
    size_bytes: int = Field(..., description="The size of the file in bytes.")
    message: str = Field(
        ...,
        description="Status message indicating the result of the upload.",
    )
    text_length: int = Field(
        0,
        description="Number of characters extracted from the document.",
    )
    chunks: int = Field(
        0,
        description="Number of text chunks created during splitting.",
    )
    embeddings: int = Field(
        0,
        description="Number of embeddings stored in the vector store.",
    )
    conversation_id: str | None = Field(
        None,
        description="The conversation/thread this document is scoped to.",
    )
