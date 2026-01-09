from flask import Blueprint, request, jsonify
from flask_jwt_extended import jwt_required
from werkzeug.security import generate_password_hash
from models import db, User

user_bp = Blueprint('users', __name__)


@user_bp.route('', methods=['GET'])
@jwt_required()
def get_users():
    """Get all users"""
    role = request.args.get('role')
    query = User.query
    
    if role:
        query = query.filter_by(role=role)
    
    users = query.all()
    return jsonify([user.to_dict() for user in users]), 200


@user_bp.route('/<int:user_id>', methods=['GET'])
@jwt_required()
def get_user(user_id):
    """Get user by ID"""
    user = User.query.get(user_id)
    
    if not user:
        return jsonify({'error': 'User not found'}), 404
    
    return jsonify(user.to_dict()), 200


@user_bp.route('/<int:user_id>', methods=['PUT'])
@jwt_required()
def update_user(user_id):
    """Update user"""
    user = User.query.get(user_id)
    
    if not user:
        return jsonify({'error': 'User not found'}), 404
    
    data = request.get_json()
    
    if data.get('username'):
        user.username = data['username']
    if data.get('full_name'):
        user.full_name = data['full_name']
    if data.get('password'):
        user.password_hash = generate_password_hash(data['password'])
    if data.get('role'):
        user.role = data['role']
    if data.get('reference_photo_url'):
        user.reference_photo_url = data['reference_photo_url']
    
    db.session.commit()
    
    return jsonify(user.to_dict()), 200


@user_bp.route('/<int:user_id>', methods=['DELETE'])
@jwt_required()
def delete_user(user_id):
    """Delete user"""
    user = User.query.get(user_id)
    
    if not user:
        return jsonify({'error': 'User not found'}), 404
    
    db.session.delete(user)
    db.session.commit()
    
    return jsonify({'message': 'User deleted successfully'}), 200


@user_bp.route('/students', methods=['GET'])
def get_students():
    """Get all students"""
    students = User.query.filter_by(role='Student').all()
    return jsonify([s.to_dict() for s in students]), 200
