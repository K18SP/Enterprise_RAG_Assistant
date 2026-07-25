class BaseCustomException(Exception):
    """
    Base class for all application exceptions.
    """

    def __init__(self, message: str):

        self.message = message

        super().__init__(message)