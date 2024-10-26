"""Customer exceptions"""

import http


class ServiceException(Exception):
    """
    Base service exception for handling service-related errors.

    Args:
        code: An integer representing the error code.
        msg: A string containing the error message.
        status_code: An optional integer representing the HTTP status code (default is 200 OK).
    """

    def __init__(self, code: int, msg: str, status_code: int = http.HTTPStatus.OK):
        """
        Initializes the ServiceException with the given parameters.

        Args:
            code: Error code indicating the type of error.
            msg: Error message providing details about the error.
            status_code: HTTP status code corresponding to the error (default is 200 OK).
        """
        self.code = code
        self.msg = msg
        self.status_code = status_code

    def __repr__(self) -> str:
        """
        Returns a string representation of the main configuration.

        Returns:
            str: A string representation of the instance.
        """
        return f"{self.__class__.__name__}({self.__dict__})"
