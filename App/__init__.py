import os

from flask import Flask

from config import INSTANCE_DIR, Config


def create_app():
    os.makedirs(INSTANCE_DIR, exist_ok=True)

    App = Flask(__name__, instance_relative_config=True)
    App.config.from_object(Config)

    from App.routes import bp as api_bp, paginas as paginas_bp

    App.register_blueprint(api_bp)
    App.register_blueprint(paginas_bp)

    return App


App = create_app()
