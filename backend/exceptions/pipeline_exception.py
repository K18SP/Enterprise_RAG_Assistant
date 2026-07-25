from .base_exception import BaseCustomException


class PipelineError(BaseCustomException):
    """
    Raised when the RAG pipeline execution fails.
    """

    pass