"""
project package: the Flask application factory.

create_app() builds and configures the Flask app, and `mysql` is the single
shared database object the whole app uses. Other modules (model.py, the views)
import this same `mysql` object so they all talk to one connection.

This follows the app-factory pattern shown in the unit's Milton Tours example.
"""
from dotenv import load_dotenv
import os
from flask import Flask
from flask_mysqldb import MySQL

load_dotenv()         # for env variables
mysql = MySQL()          # one shared object, imported elsewhere as: from project import mysql


def create_app():
    app = Flask(__name__)

    app.config["MYSQL_HOST"] = _db_host()
    app.config["MYSQL_USER"] = _db_user()
    app.config["MYSQL_PASSWORD"] = _db_password()
    app.config["MYSQL_PORT"] = _db_port()
    app.config["MYSQL_DB"] = _db()
    app.config["MYSQL_CURSORCLASS"] = "DictCursor"   # rows come back as dicts, e.g. row["title"]
    app.config["MYSQL_SSL_CA"] = "../../ca.pem"

    mysql.init_app(app)

    app.config["SECRET_KEY"] = "dev-secret-key"

    from project.views import views_bp
    app.register_blueprint(views_bp)

    from project.auth import auth_bp
    app.register_blueprint(auth_bp)

    from project.assessment import assessment_bp
    app.register_blueprint(assessment_bp)

    return app


def _db_password():
    """
    Each team member's MySQL password differs, so we never commit it.
    We read it from a local, untracked config.py (copy config.example.py to
    config.py and put your password there). If that file is missing we fall
    back to a MYSQL_PASSWORD environment variable, then to an empty string.
    """
    try:
        from config import MYSQL_PASSWORD
        return MYSQL_PASSWORD
    except ImportError:
        # if not found, load in env variable instead
        return os.environ.get("MYSQL_PASSWORD", "")

def _db_host():
    try:
        from config import MYSQL_HOST
        return MYSQL_HOST
    except ImportError:
        return os.environ.get("MYSQL_HOST", "")

def _db_user():
    try:
        from config import MYSQL_USER
        return MYSQL_USER
    except ImportError:
        return os.environ.get("MYSQL_USER", "")

def _db_port():
    try:
        from config import MYSQL_PORT
        return MYSQL_PORT
    except ImportError:
        return int(os.environ.get("MYSQL_PORT", 3306))

def _db():
    try:
        from config import MYSQL_DB
        return MYSQL_DB
    except ImportError:
        return os.environ.get("MYSQL_DB", "")
