from enum import Enum


class ResponseCode(Enum):
    """
    Enum for system response codes.
    """

    SUCCESS = (0, "Success")
    SERVICE_INTERNAL_ERROR = (-1, "Service internal error")

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

    @property
    def msg(self):
        return self.value[0]
