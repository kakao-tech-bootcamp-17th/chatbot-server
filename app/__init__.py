from flask import Flask

def create_app():
    app = Flask(__name__)

    from app.local import local_bp
    from app.weather import weather_bp

    app.register_blueprint(local_bp, url_prefix='/local')
    app.register_blueprint(weather_bp, url_prefix='/weather')

    return app
