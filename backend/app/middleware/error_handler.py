"""
Global error handlers
"""
from flask import jsonify
from werkzeug.exceptions import HTTPException

def register_error_handlers(app):
    """Register error handlers with Flask app"""
    
    @app.errorhandler(400)
    def bad_request(e):
        return jsonify({'error': 'Bad request', 'message': str(e)}), 400
    
    @app.errorhandler(401)
    def unauthorized(e):
        return jsonify({'error': 'Unauthorized', 'message': 'Authentication required'}), 401
    
    @app.errorhandler(403)
    def forbidden(e):
        return jsonify({'error': 'Forbidden', 'message': 'Access denied'}), 403
    
    @app.errorhandler(404)
    def not_found(e):
        return jsonify({'error': 'Not found', 'message': 'Resource not found'}), 404
    
    @app.errorhandler(500)
    def internal_error(e):
        return jsonify({'error': 'Internal server error', 'message': 'An unexpected error occurred'}), 500
    
    @app.errorhandler(Exception)
    def handle_exception(e):
        # Handle HTTPException
        if isinstance(e, HTTPException):
            return jsonify({'error': e.name, 'message': e.description}), e.code
        
        # Handle other exceptions
        return jsonify({'error': 'Internal server error', 'message': str(e)}), 500