"""
project package: the Flask application factory.

create_app() builds and configures the Flask app, and `mysql` is the single
shared database object the whole app uses. Other modules (model.py, the views)
import this same `mysql` object so they all talk to one connection.

This follows the app-factory pattern shown in the unit's Milton Tours example.
"""
from dotenv import load_dotenv
import os
from flask import Flask, g, send_from_directory
import psycopg
_COLUMN_NAMES = {
    name.lower(): name for name in (
        "roleID", "roleName", "roleDescription", "collectionID", "collectionName",
        "collectionDescription", "collectionTheme", "statusID", "statusName",
        "statusDescription", "userID", "fullName", "username", "email",
        "passwordHash", "accountStatus", "createdDate", "itemID", "authorCreator",
        "itemType", "thumbnailPath", "nextReviewDate", "metadataID", "communityGroup",
        "subjectArea", "culturalSensitivityNotes", "culturalProtocolNotes",
        "accessRecommendations", "requestID", "requestReason", "supportingDocuments",
        "requestDate", "requestStatus", "decisionID", "reviewerID", "decisionType",
        "decisionNotes", "accessConditions", "commentID", "commentText",
    )
}


def _dict_row(cursor):
    columns = [column.name for column in cursor.description]

    def make_row(values):
        return {_COLUMN_NAMES.get(column, column): value for column, value in zip(columns, values)}

    return make_row

load_dotenv()         # for env variables


class _Database:
    @property
    def connection(self):
        if "db" not in g:
            database_url = os.environ.get("DATABASE_URL")
            if not database_url:
                raise RuntimeError("DATABASE_URL is not configured")
            g.db = psycopg.connect(database_url, row_factory=_dict_row)
        return g.db


# Compatibility name keeps existing model/view imports unchanged.
mysql = _Database()


def create_app():
    app = Flask(__name__)

    app.config["SECRET_KEY"] = os.environ.get("SECRET_KEY", "dev-only-secret")
    app.config["RESET_SECRET"] = os.environ.get("RESET_SECRET", "")

    @app.teardown_appcontext
    def close_db(exception=None):
        connection = g.pop("db", None)
        if connection is not None:
            connection.close()

    # load favicon from assets - Some browsers/crawlers request /favicon.ico directly instead of using the <link> tag.
    @app.route('/favicon.ico') 
    def favicon():
        return send_from_directory(
            os.path.join(app.root_path, 'static', 'favicon'),
            'favicon.ico',
            mimetype='image/vnd.microsoft.icon'
        )

    from project.views import views_bp
    app.register_blueprint(views_bp)

    from project.auth import auth_bp
    app.register_blueprint(auth_bp)

    from project.assessment import assessment_bp
    app.register_blueprint(assessment_bp)

    from project.maintenance import maintenance_bp
    app.register_blueprint(maintenance_bp)

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


def _reset_secret():
    try:
        from config import MYSQL_DB
        return MYSQL_DB
    except ImportError:
        return os.environ.get("RESET_SECRET", "")
