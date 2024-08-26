from .http_exception import HttpException

class NotFoundException(HttpException):
    def __init__(self, description):
        super().__init__(code=404, title="Not Found Exception", description=description)