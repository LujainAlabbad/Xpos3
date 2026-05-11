"""
Authentication service for user registration and login
"""
from werkzeug.security import generate_password_hash, check_password_hash
from app.models.user import User
from app.extensions import db

class AuthService:
    @staticmethod
    def register_user(data):
        """Register a new user"""
        # Check if user already exists
        if User.query.filter_by(email=data['email']).first():
            raise ValueError('Email already registered')
        
        if User.query.filter_by(username=data['username']).first():
            raise ValueError('Username already taken')
        
        # Create new user
        user = User(
            username=data['username'],
            email=data['email'],
            password_hash=generate_password_hash(data['password'])
        )
        
        db.session.add(user)
        db.session.commit()
        
        return user
    
    @staticmethod
    def authenticate_user(email, password):
        """Authenticate user credentials"""
        user = User.query.filter_by(email=email).first()
        
        if not user or not check_password_hash(user.password_hash, password):
            raise ValueError('Invalid email or password')
        
        return user