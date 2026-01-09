from flask import Blueprint, request, jsonify
from flask_jwt_extended import jwt_required
from src.models import db, Exam, ExamEnrollment

exam_bp = Blueprint('exams', __name__)


@exam_bp.route('', methods=['GET'])
def get_exams():
    """Get all exams"""
    status = request.args.get('status')
    
    query = Exam.query
    if status:
        query = query.filter_by(status=status)
    
    exams = query.all()
    return jsonify([e.to_dict() for e in exams]), 200


@exam_bp.route('/<exam_id>', methods=['GET'])
def get_exam(exam_id):
    """Get an exam by ID"""
    exam = Exam.query.get(exam_id)
    if not exam:
        return jsonify({'error': 'Exam not found'}), 404
    return jsonify(exam.to_dict()), 200


@exam_bp.route('', methods=['POST'])
@jwt_required()
def create_exam():
    """Create a new exam"""
    data = request.get_json()
    
    required_fields = ['course_code', 'exam_title', 'start_time', 'end_time']
    for field in required_fields:
        if field not in data:
            return jsonify({'error': f'{field} is required'}), 400
    
    exam = Exam(
        course_code=data['course_code'],
        exam_title=data['exam_title'],
        start_time=data['start_time'],
        end_time=data['end_time'],
        status=data.get('status', 'scheduled'),
        room_id=data.get('room_id'),
        proctor_id=data.get('proctor_id')
    )
    
    db.session.add(exam)
    db.session.commit()
    
    return jsonify(exam.to_dict()), 201


@exam_bp.route('/<exam_id>', methods=['PUT'])
@jwt_required()
def update_exam(exam_id):
    """Update an exam"""
    exam = Exam.query.get(exam_id)
    if not exam:
        return jsonify({'error': 'Exam not found'}), 404
    
    data = request.get_json()
    
    if 'course_code' in data:
        exam.course_code = data['course_code']
    if 'exam_title' in data:
        exam.exam_title = data['exam_title']
    if 'start_time' in data:
        exam.start_time = data['start_time']
    if 'end_time' in data:
        exam.end_time = data['end_time']
    if 'status' in data:
        exam.status = data['status']
    if 'room_id' in data:
        exam.room_id = data['room_id']
    if 'proctor_id' in data:
        exam.proctor_id = data['proctor_id']
    
    db.session.commit()
    return jsonify(exam.to_dict()), 200


@exam_bp.route('/<exam_id>', methods=['DELETE'])
@jwt_required()
def delete_exam(exam_id):
    """Delete an exam"""
    exam = Exam.query.get(exam_id)
    if not exam:
        return jsonify({'error': 'Exam not found'}), 404
    
    db.session.delete(exam)
    db.session.commit()
    return jsonify({'message': 'Exam deleted'}), 200


@exam_bp.route('/<exam_id>/status', methods=['PUT'])
@jwt_required()
def update_exam_status(exam_id):
    """Update exam status"""
    exam = Exam.query.get(exam_id)
    if not exam:
        return jsonify({'error': 'Exam not found'}), 404
    
    data = request.get_json()
    if 'status' not in data:
        return jsonify({'error': 'status is required'}), 400
    
    exam.status = data['status']
    db.session.commit()
    
    return jsonify(exam.to_dict()), 200


@exam_bp.route('/<exam_id>/enrollments', methods=['GET'])
def get_exam_enrollments(exam_id):
    """Get all students enrolled in an exam"""
    exam = Exam.query.get(exam_id)
    if not exam:
        return jsonify({'error': 'Exam not found'}), 404
    
    enrollments = ExamEnrollment.query.filter_by(exam_id=exam_id).all()
    return jsonify([e.to_dict() for e in enrollments]), 200
