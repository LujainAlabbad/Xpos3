"""
Flask application factory and initialization
"""
from flask import Flask
from flask_cors import CORS
from celery import Celery

from app.config import config
from app.extensions import db, jwt, bcrypt, migrate, limiter

celery_app = Celery(__name__)

def create_app(config_name='development'):
    app = Flask(__name__)
    app.config.from_object(config[config_name])
    
    # Initialize extensions
    db.init_app(app)
    jwt.init_app(app)
    bcrypt.init_app(app)
    migrate.init_app(app, db)
    limiter.init_app(app)
    CORS(app, resources={r"/api/*": {"origins": "*"}})
    
    # Configure Celery
    celery_app.conf.update(app.config)
    
    # Register blueprints
    from app.routes import auth_bp, scans_bp, community_bp, users_bp
    app.register_blueprint(auth_bp, url_prefix='/api/auth')
    app.register_blueprint(scans_bp, url_prefix='/api/scans')
    app.register_blueprint(community_bp, url_prefix='/api/community')
    app.register_blueprint(users_bp, url_prefix='/api/users')
    
    # Register error handlers
    from app.middleware.error_handler import register_error_handlers
    register_error_handlers(app)
    
    return app