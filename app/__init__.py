from flask import Flask
from config import Config
from .database import init_db
from .routes import todo_api
from flask_cors import CORS

def create_app():
    app = Flask(__name__)
    CORS(app)
    app.config.from_object(Config)
    with app.app_context():
        init_db()
    app.register_blueprint(todo_api, url_prefix='/api')

    return app