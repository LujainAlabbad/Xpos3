"""
Automatically fix the auth.py file to use string identity
"""
import os

auth_file_path = 'app/routes/auth.py'

print("Reading auth.py...")
with open(auth_file_path, 'r', encoding='utf-8') as f:
    content = f.read()

print("Applying fixes...")

# Fix 1: Access token
content = content.replace(
    'create_access_token(identity=user.id)',
    'create_access_token(identity=str(user.id))'
)

# Fix 2: Refresh token
content = content.replace(
    'create_refresh_token(identity=user.id)',
    'create_refresh_token(identity=str(user.id))'
)

# Fix 3: In verify route (convert back to int)
if 'int(current_user_id)' not in content:
    content = content.replace(
        "return jsonify({'user_id': current_user_id}), 200",
        "return jsonify({'user_id': int(current_user_id), 'valid': True}), 200"
    )

print("Writing fixed auth.py...")
with open(auth_file_path, 'w', encoding='utf-8') as f:
    f.write(content)

print("✓ Fix applied successfully!")
print("\nNow restart your backend:")
print("  python run.py")