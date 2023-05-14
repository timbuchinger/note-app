import os

from flask import Flask
from flask_jwt_extended import JWTManager
from flask_limiter import Limiter
from flask_limiter.util import get_remote_address

from .auth.routes import auth
from .notes.routes import notes
from .search.routes import note_search


def create_app():
    app = Flask(__name__)

    app.config["SECRET_KEY"] = os.environ.get(
        "SECRET_KEY", default="a_not_so_secret_key"
    )

    JWTManager(app)

    Limiter(
        get_remote_address,
        app=app,
        default_limits=["200 per day", "50 per hour"],
        storage_uri="memory://",
    )

    app.register_blueprint(auth, url_prefix="/api/auth")
    app.register_blueprint(notes, url_prefix="/api/notes")
    app.register_blueprint(note_search, url_prefix="/api/search")

    return app
