from flask import Blueprint, request, jsonify
from flask_jwt_extended import create_access_token, jwt_required, get_jwt_identity
from werkzeug.security import generate_password_hash, check_password_hash
from models import db, User

auth_bp = Blueprint('auth', __name__)


@auth_bp.route('/login', methods=['POST'])
def login():
    """User login - returns JWT token"""
    data = request.get_json()
    
    if not data or not data.get('username') or not data.get('password'):
        return jsonify({'error': 'Username and password required'}), 400
    
    user = User.query.filter_by(username=data['username']).first()
    
    if not user or not check_password_hash(user.password_hash, data['password']):
        return jsonify({'error': 'Invalid username or password'}), 401
    
    # Create JWT token
    access_token = create_access_token(identity={
        'user_id': user.id,
        'username': user.username,
        'role': user.role
    })
    
    return jsonify({
        'access_token': access_token,
        'user': user.to_dict()
    }), 200


@auth_bp.route('/register', methods=['POST'])
def register():
    """Register new user"""
    data = request.get_json()
    
    required_fields = ['username', 'password', 'full_name']
    for field in required_fields:
        if not data.get(field):
            return jsonify({'error': f'{field} is required'}), 400
    
    # Check if username exists
    if User.query.filter_by(username=data['username']).first():
        return jsonify({'error': 'Username already exists'}), 409
    
    # Create user
    user = User(
        username=data['username'],
        password_hash=generate_password_hash(data['password']),
        full_name=data['full_name'],
        role=data.get('role', 'Student')
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
    identity = get_jwt_identity()
    user = User.query.get(identity['user_id'])
    
    if not user:
        return jsonify({'error': 'User not found'}), 404
    
    return jsonify(user.to_dict()), 200
