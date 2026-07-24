from pydantic import BaseModel

class RetrievalMetadata(BaseModel):
    requested: int
    returned: int