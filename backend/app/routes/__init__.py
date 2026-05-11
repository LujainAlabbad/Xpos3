"""
Blueprint registration
"""
from flask import Blueprint

auth_bp = Blueprint('auth', __name__)
scans_bp = Blueprint('scans', __name__)
community_bp = Blueprint('community', __name__)
users_bp = Blueprint('users', __name__)

from app.routes import auth, scans, community, users