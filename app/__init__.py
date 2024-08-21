from flask import Flask, Blueprint
from app.local import local_bp

def create_app(config_class='config.Config'):
        # print("sdfsd")
        app = Flask(__name__)
        app.config.from_object(config_class)

        # print("Loaded KAKAO_APP_API_KEY:", app.config.get('KAKAO_APP_API_KEY'))
        # 블루프린트 등록
        app.register_blueprint(local_bp)

        return app