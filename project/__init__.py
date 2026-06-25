"""
project package: the Flask application factory.

create_app() builds and configures the Flask app, and `mysql` is the single
shared database object the whole app uses. Other modules (model.py, the views)
import this same `mysql` object so they all talk to one connection.

This follows the app-factory pattern shown in the unit's Milton Tours example.
"""
import os
from flask import Flask
from flask_mysqldb import MySQL

mysql = MySQL()          # one shared object, imported elsewhere as: from project import mysql


def create_app():
    app = Flask(__name__)

    app.config["MYSQL_HOST"] = "localhost"
    app.config["MYSQL_USER"] = "root"
    app.config["MYSQL_PASSWORD"] = _db_password()
    app.config["MYSQL_DB"] = "ifq582_a2"
    app.config["MYSQL_CURSORCLASS"] = "DictCursor"   # rows come back as dicts, e.g. row["title"]

    mysql.init_app(app)

    # Views get registered here later, e.g.:
    #   from project.views import main
    #   app.register_blueprint(main)

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
        return os.environ.get("MYSQL_PASSWORD", "")
