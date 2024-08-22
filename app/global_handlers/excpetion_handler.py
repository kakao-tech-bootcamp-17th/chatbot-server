from flask import jsonify
from app.exception.http_exception import HttpException
from app.exception.bad_reqeust_exception import BadRequestException
from requests.exceptions import HTTPError

def register_error_handlers(app):
    @app.errorhandler(HttpException)
    def handle_http_exception(e):
        print("catched")
        response = {
            "code": e.code,
            "title": e.title,
            "description": e.description,
        }
        
        return jsonify(response), e.code

    @app.errorhandler(HTTPError)
    def handle_http_error(e):
        print("Caught HTTPError")
        # 상태 코드와 메시지 추출
        status_code = getattr(e.response, 'status_code', 500)  # 상태 코드 추출
        error_message = str(e)
        response = {
            "code": status_code,
            "title": "HTTP Error",
            "description": error_message
        }
        return jsonify(response), status_code
