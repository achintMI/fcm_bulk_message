from flask import Blueprint

healthcheck_bp = Blueprint('healthcheck', __name__)
notifications_bp = Blueprint('notifications', __name__)

# Import routes
from app.routes import healthcheck
from app.routes import notifications
