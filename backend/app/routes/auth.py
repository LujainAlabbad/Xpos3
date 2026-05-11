"""
Authentication endpoints
"""
from flask import request, jsonify
from flask_jwt_extended import create_access_token, create_refresh_token, jwt_required, get_jwt_identity
from marshmallow import ValidationError
from app.routes import auth_bp
from app.services.auth_service import AuthService
from app.schemas.auth_schemas import RegisterSchema, LoginSchema

@auth_bp.route('/register', methods=['POST'])
def register():
    """Register a new user"""
    try:
        schema = RegisterSchema()
        data = schema.load(request.get_json())
        
        user = AuthService.register_user(data)
        return jsonify({'message': 'User registered successfully', 'user': user.to_dict()}), 201
    
    except ValidationError as e:
        return jsonify({'error': 'Validation error', 'messages': e.messages}), 400
    except ValueError as e:
        return jsonify({'error': str(e)}), 400
    except Exception as e:
        return jsonify({'error': 'Registration failed', 'message': str(e)}), 500

@auth_bp.route('/login', methods=['POST'])
def login():
    """Authenticate user and return tokens"""
    try:
        schema = LoginSchema()
        data = schema.load(request.get_json())
        
        user = AuthService.authenticate_user(data['email'], data['password'])
        
        access_token = create_access_token(identity=str(user.id))
        refresh_token = create_refresh_token(identity=str(user.id))
        
        return jsonify({
            'access_token': access_token,
            'refresh_token': refresh_token,
            'user': user.to_dict()
        }), 200
    
    except ValidationError as e:
        return jsonify({'error': 'Validation error', 'messages': e.messages}), 400
    except ValueError as e:
        return jsonify({'error': str(e)}), 401
    except Exception as e:
        return jsonify({'error': 'Login failed', 'message': str(e)}), 500

@auth_bp.route('/refresh', methods=['POST'])
@jwt_required(refresh=True)
def refresh():
    """Refresh access token"""
    current_user_id = get_jwt_identity()
    new_access_token = create_access_token(identity=current_user_id)
    return jsonify({'access_token': new_access_token}), 200

@auth_bp.route('/verify', methods=['GET'])
@jwt_required()
def verify():
    """Verify token validity"""
    current_user_id = get_jwt_identity()
    return jsonify({'user_id': int(current_user_id), 'valid': True}), 200