from datetime import datetime

from pydantic import BaseModel
from pydantic import EmailStr


class UserResponse(BaseModel):

    id: int

    username: str

    email: EmailStr

    created_at: datetime

    model_config = {
        "from_attributes": True
    }