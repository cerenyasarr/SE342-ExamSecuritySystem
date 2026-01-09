from flask import Blueprint, request, jsonify
from flask_jwt_extended import jwt_required
from models import db, Course

course_bp = Blueprint('courses', __name__)


@course_bp.route('', methods=['GET'])
def get_courses():
    """Get all courses"""
    courses = Course.query.all()
    return jsonify([course.to_dict() for course in courses]), 200


@course_bp.route('/<int:course_id>', methods=['GET'])
def get_course(course_id):
    """Get course by ID"""
    course = Course.query.get(course_id)
    
    if not course:
        return jsonify({'error': 'Course not found'}), 404
    
    return jsonify(course.to_dict()), 200


@course_bp.route('', methods=['POST'])
@jwt_required()
def create_course():
    """Create a new course"""
    data = request.get_json()
    
    required_fields = ['code', 'name']
    for field in required_fields:
        if not data.get(field):
            return jsonify({'error': f'{field} is required'}), 400
    
    # Check if code exists
    if Course.query.filter_by(code=data['code']).first():
        return jsonify({'error': 'Course code already exists'}), 409
    
    course = Course(
        code=data['code'],
        name=data['name'],
        instructor_id=data.get('instructor_id')
    )
    
    db.session.add(course)
    db.session.commit()
    
    return jsonify(course.to_dict()), 201


@course_bp.route('/<int:course_id>', methods=['PUT'])
@jwt_required()
def update_course(course_id):
    """Update course"""
    course = Course.query.get(course_id)
    
    if not course:
        return jsonify({'error': 'Course not found'}), 404
    
    data = request.get_json()
    
    if data.get('code'):
        course.code = data['code']
    if data.get('name'):
        course.name = data['name']
    if data.get('instructor_id') is not None:
        course.instructor_id = data['instructor_id']
    
    db.session.commit()
    
    return jsonify(course.to_dict()), 200


@course_bp.route('/<int:course_id>', methods=['DELETE'])
@jwt_required()
def delete_course(course_id):
    """Delete course"""
    course = Course.query.get(course_id)
    
    if not course:
        return jsonify({'error': 'Course not found'}), 404
    
    db.session.delete(course)
    db.session.commit()
    
    return jsonify({'message': 'Course deleted successfully'}), 200
