from .http_exception import HttpException

class InternalServerException(HttpException):
    def __init__(self, description):
        super().__init__(code=500, title="Internal Server Exception", description=description)