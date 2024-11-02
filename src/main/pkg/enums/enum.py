from enum import Enum


class ResponseCode(Enum):
    """
    Enum for system response codes.
    """

    SUCCESS = (0, "Success")
    SERVICE_INTERNAL_ERROR = (-1, "Service internal error")

    PARAMETER_ERROR = (400, "Parameter error")
    DB_UNKNOWN_ERROR = (400, "Db unknown error")
    AUTH_FAILED = (403, "Username or password error")
    PARAMETER_CHECK_ERROR = (402, "Parameter error")
    USER_NAME_EXISTS = (100, "Username already exists")
    ROLE_ALREADY_EXISTS = (101, "Assign role already exists")

    @property
    def code(self):
        return self.value[0]

    @property
    def msg(self):
        return self.value[1]


class ConstantCode(Enum):
    """
    Enum for system constant codes.
    """

    USER_KEY = "user:"
    AUTH_KEY = "Authorization"

    @property
    def msg(self):
        return self.value


class SortEnum(str, Enum):
    """
    Enum for specifying sorting order.
    """

    ascending = "asc"
    descending = "desc"


class TokenTypeEnum(str, Enum):
    """
    Enum for token type.
    """

    access = "access"
    refresh = "refresh"
    bearer = "Bearer"
