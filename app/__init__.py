from flask import Flask

def create_app():
    app = Flask(__name__)
    app.config.from_object('config.Config')

    
    with app.app_context():
        # 애플리케이션 컨텍스트 내에서 초기화 코드 실행
        from app.local import local_bp
        from app.weather import weather_bp
        app.register_blueprint(local_bp, url_prefix='/local')
        app.register_blueprint(weather_bp, url_prefix='/weather')

    return app
