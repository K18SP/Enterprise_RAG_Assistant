from pydantic import BaseModel


class ErrorDetail(BaseModel):
    """
    Error information.
    """

    type: str
    message: str


class APIError(BaseModel):
    """
    Standard error response.
    """

    success: bool = False
    error: ErrorDetail