from .base_exception import BaseCustomException


class LLMError(BaseCustomException):
    """
    Raised when the language model fails.
    """

    pass