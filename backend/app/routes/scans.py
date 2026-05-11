"""
Scan management endpoints
"""
from flask import request, jsonify
from flask_jwt_extended import jwt_required, get_jwt_identity
from app.routes import scans_bp
from app.services.scan_service import ScanService

@scans_bp.route('/upload', methods=['POST'])
@jwt_required()
def upload_scan():
    """Upload file and initiate scan"""
    try:
        # Validate file
        if 'file' not in request.files:
            return jsonify({'error': 'No file provided'}), 400
        
        file = request.files['file']
        if file.filename == '':
            return jsonify({'error': 'No file selected'}), 400
        
        if not file.filename.endswith('.py'):
            return jsonify({'error': 'Only Python (.py) files are allowed'}), 400
        
        # Convert JWT identity (string) to int
        user_id = int(get_jwt_identity())
        
        scan = ScanService.create_scan(user_id, file)
        
        print(f"✓ Scan created: User={user_id}, File={scan.filename}")
        
        return jsonify({
            'message': 'Scan initiated successfully',
            'scan': scan.to_dict()
        }), 201
        
    except ValueError as e:
        print(f"✗ Validation: {str(e)}")
        return jsonify({'error': str(e)}), 400
    except Exception as e:
        print(f"✗ Upload error: {str(e)}")
        import traceback
        traceback.print_exc()
        return jsonify({'error': 'Upload failed', 'message': str(e)}), 500

@scans_bp.route('/', methods=['GET'])
@jwt_required()
def get_user_scans():
    """Get user's scan history"""
    try:
        user_id = int(get_jwt_identity())
        scans = ScanService.get_user_scans(user_id)
        
        return jsonify({'scans': [scan.to_dict() for scan in scans]}), 200
    except Exception as e:
        print(f"✗ Get scans: {str(e)}")
        import traceback
        traceback.print_exc()
        return jsonify({'error': 'Failed to retrieve scans'}), 500

@scans_bp.route('/<int:scan_id>', methods=['GET'])
@jwt_required()
def get_scan_report(scan_id):
    """Get detailed scan report"""
    try:
        user_id = int(get_jwt_identity())
        report = ScanService.get_scan_report(user_id, scan_id)
        return jsonify(report), 200
    except ValueError as e:
        return jsonify({'error': str(e)}), 404
    except Exception as e:
        print(f"✗ Get report: {str(e)}")
        return jsonify({'error': 'Failed to retrieve report'}), 500

@scans_bp.route('/<int:scan_id>/status', methods=['GET'])
@jwt_required()
def get_scan_status(scan_id):
    """Check scan progress"""
    try:
        user_id = int(get_jwt_identity())
        status = ScanService.get_scan_status(user_id, scan_id)
        return jsonify(status), 200
    except ValueError as e:
        return jsonify({'error': str(e)}), 404
    except Exception as e:
        return jsonify({'error': 'Failed to retrieve status'}), 500

@scans_bp.route('/<int:scan_id>', methods=['DELETE'])
@jwt_required()
def delete_scan(scan_id):
    """Delete scan record"""
    try:
        user_id = int(get_jwt_identity())
        ScanService.delete_scan(user_id, scan_id)
        return jsonify({'message': 'Scan deleted successfully'}), 200
    except ValueError as e:
        return jsonify({'error': str(e)}), 404
    except Exception as e:
        return jsonify({'error': 'Failed to delete scan'}), 500