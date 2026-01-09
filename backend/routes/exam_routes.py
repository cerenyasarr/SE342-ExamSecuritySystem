from flask import Blueprint, request, jsonify
from flask_jwt_extended import jwt_required
from models import db, Exam, StudentExam

exam_bp = Blueprint('exams', __name__)


@exam_bp.route('', methods=['GET'])
def get_exams():
    """Get all exams"""
    status = request.args.get('status')
    course_id = request.args.get('course_id')
    
    query = Exam.query
    
    if status:
        query = query.filter_by(status=status)
    if course_id:
        query = query.filter_by(course_id=course_id)
    
    exams = query.order_by(Exam.start_time.desc()).all()
    return jsonify([exam.to_dict() for exam in exams]), 200


@exam_bp.route('/<int:exam_id>', methods=['GET'])
def get_exam(exam_id):
    """Get exam by ID"""
    exam = Exam.query.get(exam_id)
    
    if not exam:
        return jsonify({'error': 'Exam not found'}), 404
    
    return jsonify(exam.to_dict()), 200


@exam_bp.route('', methods=['POST'])
@jwt_required()
def create_exam():
    """Create a new exam"""
    data = request.get_json()
    
    required_fields = ['name', 'start_time', 'end_time']
    for field in required_fields:
        if not data.get(field):
            return jsonify({'error': f'{field} is required'}), 400
    
    exam = Exam(
        course_id=data.get('course_id'),
        room_id=data.get('room_id'),
        name=data['name'],
        start_time=data['start_time'],
        end_time=data['end_time'],
        status=data.get('status', 'Scheduled')
    )
    
    db.session.add(exam)
    db.session.commit()
    
    return jsonify(exam.to_dict()), 201


@exam_bp.route('/<int:exam_id>', methods=['PUT'])
@jwt_required()
def update_exam(exam_id):
    """Update exam"""
    exam = Exam.query.get(exam_id)
    
    if not exam:
        return jsonify({'error': 'Exam not found'}), 404
    
    data = request.get_json()
    
    if data.get('course_id') is not None:
        exam.course_id = data['course_id']
    if data.get('room_id') is not None:
        exam.room_id = data['room_id']
    if data.get('name'):
        exam.name = data['name']
    if data.get('start_time'):
        exam.start_time = data['start_time']
    if data.get('end_time'):
        exam.end_time = data['end_time']
    if data.get('status'):
        exam.status = data['status']
    
    db.session.commit()
    
    return jsonify(exam.to_dict()), 200


@exam_bp.route('/<int:exam_id>', methods=['DELETE'])
@jwt_required()
def delete_exam(exam_id):
    """Delete exam"""
    exam = Exam.query.get(exam_id)
    
    if not exam:
        return jsonify({'error': 'Exam not found'}), 404
    
    db.session.delete(exam)
    db.session.commit()
    
    return jsonify({'message': 'Exam deleted successfully'}), 200


@exam_bp.route('/<int:exam_id>/students', methods=['GET'])
def get_exam_students(exam_id):
    """Get all students enrolled in an exam"""
    exam = Exam.query.get(exam_id)
    
    if not exam:
        return jsonify({'error': 'Exam not found'}), 404
    
    student_exams = StudentExam.query.filter_by(exam_id=exam_id).all()
    return jsonify([se.to_dict() for se in student_exams]), 200


@exam_bp.route('/<int:exam_id>/status', methods=['PUT'])
@jwt_required()
def update_exam_status(exam_id):
    """Update exam status"""
    exam = Exam.query.get(exam_id)
    
    if not exam:
        return jsonify({'error': 'Exam not found'}), 404
    
    data = request.get_json()
    if data.get('status'):
        exam.status = data['status']
        db.session.commit()
    
    return jsonify(exam.to_dict()), 200
