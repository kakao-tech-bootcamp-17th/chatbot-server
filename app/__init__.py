from flask import Flask
from dotenv import load_dotenv

def create_app():
    load_dotenv()
    app = Flask(__name__)
    
    from app.local.services import local_bp
    from app.weather.services import weather_bp
    
    app.register_blueprint(local_bp, url_prefix="/local")
    app.register_blueprint(weather_bp, url_prefix="/weather")
    
    return app
    