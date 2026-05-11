"""
Custom decorators for route validation
"""
from functools import wraps
from flask import request, jsonify
from app.utils.validators import allowed_file, validate_file_size

def validate_file():
    """Decorator to validate uploaded files"""
    def decorator(f):
        @wraps(f)
        def decorated_function(*args, **kwargs):
            # Check if file is present
            if 'file' not in request.files:
                return jsonify({'error': 'No file provided'}), 400
            
            file = request.files['file']
            
            # Check if filename is empty
            if file.filename == '':
                return jsonify({'error': 'No file selected'}), 400
            
            # Validate file extension
            if not allowed_file(file.filename):
                return jsonify({'error': 'Only Python (.py) files are allowed'}), 400
            
            # Validate file size
            if not validate_file_size(file):
                return jsonify({'error': 'File size exceeds 10MB limit'}), 400
            
            return f(*args, **kwargs)
        return decorated_function
    return decorator