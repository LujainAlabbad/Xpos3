"""
Test JWT token creation and validation
"""
from app import create_app
from flask_jwt_extended import create_access_token, decode_token, get_jwt_identity
from flask import Flask
import jwt as pyjwt

app = create_app()

with app.app_context():
    print("\n" + "="*70)
    print("JWT TOKEN DIAGNOSTIC TEST")
    print("="*70)
    
    # Test 1: Create token with INTEGER (current broken behavior)
    print("\n[TEST 1] Creating token with INTEGER identity...")
    try:
        token_int = create_access_token(identity=1)
        print(f"  ✓ Token created: {token_int[:50]}...")
        
        # Try to decode it
        try:
            decoded = decode_token(token_int)
            print(f"  ✓ Token decoded successfully")
            print(f"    Subject (identity): {decoded['sub']}")
        except Exception as e:
            print(f"  ✗ DECODE FAILED: {str(e)}")
    except Exception as e:
        print(f"  ✗ CREATE FAILED: {str(e)}")
    
    # Test 2: Create token with STRING (correct behavior)
    print("\n[TEST 2] Creating token with STRING identity...")
    try:
        token_str = create_access_token(identity=str(1))
        print(f"  ✓ Token created: {token_str[:50]}...")
        
        # Try to decode it
        try:
            decoded = decode_token(token_str)
            print(f"  ✓ Token decoded successfully")
            print(f"    Subject (identity): {decoded['sub']}")
            print(f"    Type: {type(decoded['sub'])}")
        except Exception as e:
            print(f"  ✗ DECODE FAILED: {str(e)}")
    except Exception as e:
        print(f"  ✗ CREATE FAILED: {str(e)}")
    
    # Test 3: Simulate what happens in a request
    print("\n[TEST 3] Simulating JWT verification in a request...")
    token = create_access_token(identity=str(1))
    
    with app.test_request_context(
        '/api/scans/',
        headers={'Authorization': f'Bearer {token}'}
    ):
        try:
            from flask_jwt_extended import verify_jwt_in_request
            verify_jwt_in_request()
            user_id = get_jwt_identity()
            print(f"  ✓ JWT verified successfully!")
            print(f"    User ID from token: {user_id}")
            print(f"    Type: {type(user_id)}")
        except Exception as e:
            print(f"  ✗ JWT VERIFICATION FAILED: {str(e)}")
    
    print("\n" + "="*70)
    print("DIAGNOSTIC COMPLETE")
    print("="*70 + "\n")