from typing import Generic, TypeVar

from pydantic import BaseModel

T = TypeVar("T")


class APISuccess(BaseModel, Generic[T]):
    """
    Standard success response.
    """

    success: bool = True
    data: T