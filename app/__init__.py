from flask import Flask
from app.global_handlers.excpetion_handler import register_error_handlers 

def create_app():
    app = Flask(__name__)
    
    app.config.from_object('config.Config')
    register_error_handlers(app)

    
    with app.app_context():
        # 애플리케이션 컨텍스트 내에서 초기화 코드 실행
        from app.local import local_bp
        from app.weather import weather_bp
        from app.gpt import gpt_bp
        from app.traffic import traffic_bp
        app.register_blueprint(local_bp, url_prefix='/local')
        app.register_blueprint(weather_bp, url_prefix='/weather')
        app.register_blueprint(gpt_bp, url_prefix='/gpt')
        app.register_blueprint(traffic_bp, url_prefix='/traffic')

    return app