from flask import Flask
from app.local import local_bp

def create_app(config_class='config.Config'):
    app = Flask(__name__)
    app.config.from_object(config_class)

    app.register_blueprint(local_bp)

    return app