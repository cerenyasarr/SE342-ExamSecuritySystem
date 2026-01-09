from flask import Blueprint, request, jsonify
from flask_jwt_extended import jwt_required
from werkzeug.security import generate_password_hash
from src.models import db, Student, SystemUser

user_bp = Blueprint('users', __name__)


# ============ STUDENTS (exam takers) ============

@user_bp.route('/students', methods=['GET'])
def get_students():
    """Get all students"""
    students = Student.query.all()
    return jsonify([s.to_dict() for s in students]), 200


@user_bp.route('/students/<student_id>', methods=['GET'])
def get_student(student_id):
    """Get a student by ID"""
    student = Student.query.get(student_id)
    if not student:
        return jsonify({'error': 'Student not found'}), 404
    return jsonify(student.to_dict()), 200


@user_bp.route('/students', methods=['POST'])
@jwt_required()
def create_student():
    """Create a new student"""
    data = request.get_json()
    
    required_fields = ['student_number', 'full_name']
    for field in required_fields:
        if field not in data:
            return jsonify({'error': f'{field} is required'}), 400
    
    if Student.query.filter_by(student_number=data['student_number']).first():
        return jsonify({'error': 'Student number already exists'}), 409
    
    student = Student(
        student_number=data['student_number'],
        full_name=data['full_name'],
        email=data.get('email'),
        reference_image_path=data.get('reference_image_path')
    )
    
    db.session.add(student)
    db.session.commit()
    
    return jsonify(student.to_dict()), 201


@user_bp.route('/students/<student_id>', methods=['PUT'])
@jwt_required()
def update_student(student_id):
    """Update a student"""
    student = Student.query.get(student_id)
    if not student:
        return jsonify({'error': 'Student not found'}), 404
    
    data = request.get_json()
    
    if 'full_name' in data:
        student.full_name = data['full_name']
    if 'email' in data:
        student.email = data['email']
    if 'reference_image_path' in data:
        student.reference_image_path = data['reference_image_path']
    
    db.session.commit()
    return jsonify(student.to_dict()), 200


@user_bp.route('/students/<student_id>', methods=['DELETE'])
@jwt_required()
def delete_student(student_id):
    """Delete a student"""
    student = Student.query.get(student_id)
    if not student:
        return jsonify({'error': 'Student not found'}), 404
    
    db.session.delete(student)
    db.session.commit()
    return jsonify({'message': 'Student deleted'}), 200


# ============ SYSTEM USERS (admins/proctors) ============

@user_bp.route('', methods=['GET'])
@jwt_required()
def get_system_users():
    """Get all system users (admins/proctors)"""
    role_id = request.args.get('role')
    
    query = SystemUser.query
    if role_id:
        query = query.filter_by(role_id=role_id)
    
    users = query.all()
    return jsonify([u.to_dict() for u in users]), 200


@user_bp.route('/<user_id>', methods=['GET'])
@jwt_required()
def get_system_user(user_id):
    """Get a system user by ID"""
    user = SystemUser.query.get(user_id)
    if not user:
        return jsonify({'error': 'User not found'}), 404
    return jsonify(user.to_dict()), 200


@user_bp.route('/<user_id>', methods=['DELETE'])
@jwt_required()
def delete_system_user(user_id):
    """Delete a system user"""
    user = SystemUser.query.get(user_id)
    if not user:
        return jsonify({'error': 'User not found'}), 404
    
    db.session.delete(user)
    db.session.commit()
    return jsonify({'message': 'User deleted'}), 200
