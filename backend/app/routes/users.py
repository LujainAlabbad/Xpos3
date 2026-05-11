"""
User management endpoints — profile view, update, password change, account delete.
"""
from flask import request, jsonify
from flask_jwt_extended import jwt_required, get_jwt_identity
from werkzeug.security import check_password_hash, generate_password_hash
from app.routes import users_bp
from app.models.user import User
from app.extensions import db


@users_bp.route('/profile', methods=['GET'])
@jwt_required()
def get_profile():
    """Return the authenticated user's profile."""
    try:
        user_id = int(get_jwt_identity())
        user = User.query.get(user_id)
        if not user:
            return jsonify({'error': 'User not found'}), 404
        return jsonify({'user': user.to_dict()}), 200
    except Exception as exc:
        print(f"get_profile error: {exc}")
        return jsonify({'error': 'Failed to get profile'}), 500


@users_bp.route('/profile', methods=['PUT'])
@jwt_required()
def update_profile():
    """Update the authenticated user's username."""
    try:
        user_id = int(get_jwt_identity())
        user = User.query.get(user_id)
        if not user:
            return jsonify({'error': 'User not found'}), 404

        data = request.get_json() or {}
        username = data.get('username', '').strip()

        if not username:
            return jsonify({'error': 'Username cannot be empty'}), 400
        if len(username) < 3:
            return jsonify({'error': 'Username must be at least 3 characters'}), 400

        existing = User.query.filter_by(username=username).first()
        if existing and existing.id != user_id:
            return jsonify({'error': 'Username already taken'}), 400

        user.username = username
        db.session.commit()
        return jsonify({'user': user.to_dict()}), 200

    except Exception as exc:
        db.session.rollback()
        print(f"update_profile error: {exc}")
        return jsonify({'error': 'Failed to update profile'}), 500


@users_bp.route('/change-password', methods=['PUT'])
@jwt_required()
def change_password():
    """Change the authenticated user's password after verifying the current one."""
    try:
        user_id = int(get_jwt_identity())
        user = User.query.get(user_id)
        if not user:
            return jsonify({'error': 'User not found'}), 404

        data = request.get_json() or {}
        current_password = data.get('current_password', '')
        new_password = data.get('new_password', '')

        if not check_password_hash(user.password_hash, current_password):
            return jsonify({'error': 'Current password is incorrect'}), 400
        if len(new_password) < 8:
            return jsonify({'error': 'New password must be at least 8 characters'}), 400

        user.password_hash = generate_password_hash(new_password)
        db.session.commit()
        return jsonify({'message': 'Password updated successfully'}), 200

    except Exception as exc:
        db.session.rollback()
        print(f"change_password error: {exc}")
        return jsonify({'error': 'Failed to change password'}), 500


@users_bp.route('/account', methods=['DELETE'])
@jwt_required()
def delete_account():
    """Permanently delete the account after password confirmation."""
    try:
        user_id = int(get_jwt_identity())
        user = User.query.get(user_id)
        if not user:
            return jsonify({'error': 'User not found'}), 404

        data = request.get_json() or {}
        password = data.get('password', '')

        if not check_password_hash(user.password_hash, password):
            return jsonify({'error': 'Password confirmation is incorrect'}), 400

        db.session.delete(user)
        db.session.commit()
        return jsonify({'message': 'Account deleted successfully'}), 200

    except Exception as exc:
        db.session.rollback()
        print(f"delete_account error: {exc}")
        return jsonify({'error': 'Failed to delete account'}), 500
