import typing as t
from pydantic import BaseModel

class BaseResponse(BaseModel):
    status: t.Union[str, None] = None
    message: t.Union[str, None] = None

    def __init__(self, status, message):
        super().__init__()
        self.status = status
        self.message = message


class ErrorResponse(BaseResponse):
    exception: t.Union[str, None]

    def __init__(self, error="Something went wrong!", exception="global-exception"):
        super().__init__("FAILURE", error)
        self.exception = exception


class SuccessResponse(BaseResponse):
    def __init__(self, message, resp={}):
        super().__init__("SUCCESS", message)
        if resp:
            for key in resp:
                self.__dict__[key] = resp[key]
