from flask import Blueprint, request, jsonify
from flask_jwt_extended import create_access_token, jwt_required, get_jwt_identity
from werkzeug.security import generate_password_hash, check_password_hash
from src.models import db, SystemUser

auth_bp = Blueprint('auth', __name__)


@auth_bp.route('/login', methods=['POST'])
def login():
    """Login endpoint for system users (admin/proctor)"""
    data = request.get_json()
    
    print(f"[DEBUG] Login attempt - Data received: {data}")
    
    if not data or 'username' not in data or 'password' not in data:
        print("[DEBUG] Missing username or password")
        return jsonify({'error': 'Username and password required'}), 400
    
    user = SystemUser.query.filter_by(username=data['username']).first()
    
    print(f"[DEBUG] User found: {user}")
    if user:
        print(f"[DEBUG] User password_hash: {user.password_hash}")
        print(f"[DEBUG] Provided password: {data['password']}")
    
    if not user:
        print("[DEBUG] User not found in database")
        return jsonify({'error': 'Invalid username or password'}), 401
    
    # Support both hashed and plain text passwords (for backward compatibility)
    password_valid = False
    
    # Check if password_hash looks like a proper hash (starts with hash algorithm prefix)
    if user.password_hash.startswith(('scrypt:', 'pbkdf2:', 'sha256:')):
        # It's a hashed password
        password_valid = check_password_hash(user.password_hash, data['password'])
        print(f"[DEBUG] Hash check result: {password_valid}")
    else:
        # It's a plain text password
        password_valid = (user.password_hash == data['password'])
        print(f"[DEBUG] Plain text comparison result: {password_valid}")
    
    if not password_valid:
        print("[DEBUG] Password validation failed")
        return jsonify({'error': 'Invalid username or password'}), 401
    
    # Create JWT token with user identity (must be a string)
    # Additional user data goes in additional_claims
    additional_claims = {
        'username': user.username,
        'role': user.role.name if user.role else 'proctor',
        'full_name': user.full_name
    }
    
    access_token = create_access_token(
        identity=str(user.user_id),  # Identity must be a string
        additional_claims=additional_claims
    )
    
    return jsonify({
        'access_token': access_token,
        'user': user.to_dict()
    }), 200


@auth_bp.route('/register', methods=['POST'])
def register():
    """Register a new system user"""
    data = request.get_json()
    
    required_fields = ['username', 'password', 'full_name']
    for field in required_fields:
        if field not in data:
            return jsonify({'error': f'{field} is required'}), 400
    
    # Check if username exists
    if SystemUser.query.filter_by(username=data['username']).first():
        return jsonify({'error': 'Username already exists'}), 409
    
    user = SystemUser(
        username=data['username'],
        password_hash=generate_password_hash(data['password']),
        full_name=data['full_name'],
        role_id=data.get('role_id', 'proctor')  # Default to proctor
    )
    
    db.session.add(user)
    db.session.commit()
    
    return jsonify({
        'message': 'User created successfully',
        'user': user.to_dict()
    }), 201


@auth_bp.route('/me', methods=['GET'])
@jwt_required()
def get_current_user():
    """Get current logged-in user info"""
    user_id = get_jwt_identity()  # Now returns string user_id
    user = SystemUser.query.get(user_id)
    
    if not user:
        return jsonify({'error': 'User not found'}), 404
    
    return jsonify(user.to_dict()), 200
