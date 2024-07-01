import os
from flask import Flask
from app.config import Config
from app.routes import healthcheck_bp, notifications_bp
from app.config import config_by_name
from app.extensions import db, migrate


def create_app(config_name="development"):
    os.makedirs(config_by_name[config_name].TEMP_FILES_DIR, exist_ok=True)
    app = Flask(__name__)
    app.config.from_object(config_by_name[config_name])
    db.init_app(app)
    migrate.init_app(app, db)

    from app.routes import healthcheck_bp
    app.register_blueprint(healthcheck_bp)
    app.register_blueprint(notifications_bp)

    return app
