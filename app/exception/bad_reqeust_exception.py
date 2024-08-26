from .http_exception import HttpException

class BadRequestException(HttpException):
    def __init__(self, description):
        super().__init__(code=400, title="Bad Request", description=description)