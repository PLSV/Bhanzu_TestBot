import http

class ApplicationException(Exception):
    def __init__(
        self,
        error="application exception occurred",
        status_code=http.HTTPStatus.BAD_REQUEST,
    ):
        self.error = error
        self.status_code = status_code
        super().__init__(self.error)

    def __str__(self):
        return str(self.error)