from typing import Any

from pydantic import BaseModel, Field


class RetrievedDocument(BaseModel):

    content: str = Field(
        description="Retrieved document content"
    )

    metadata: dict[str, Any] = Field(
        default_factory=dict,
        description="Document metadata"
    )