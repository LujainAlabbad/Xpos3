"""
Test JWT token generation and validation
"""
from app import create_app
from flask_jwt_extended import create_access_token, decode_token
from app.extensions import jwt

app = create_app()

with app.app_context():
    # Create a test token
    test_user_id = 1
    token = create_access_token(identity=test_user_id)
    
    print("=" * 60)
    print("JWT TOKEN TEST")
    print("=" * 60)
    print(f"\n✓ Token generated for user_id: {test_user_id}")
    print(f"\n  Token (first 50 chars): {token[:50]}...")
    print(f"\n  Token length: {len(token)}")
    
    # Try to decode it
    try:
        decoded = decode_token(token)
        print(f"\n✓ Token decoded successfully!")
        print(f"\n  User Identity: {decoded['sub']}")
        print(f"  Token Type: {decoded.get('type', 'access')}")
        print(f"  Expires: {decoded.get('exp', 'N/A')}")
    except Exception as e:
        print(f"\n✗ Token decode FAILED: {str(e)}")
    
    print("\n" + "=" * 60)