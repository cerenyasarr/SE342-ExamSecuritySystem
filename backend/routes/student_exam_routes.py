from flask import Blueprint, request, jsonify
from flask_jwt_extended import jwt_required
from datetime import datetime
from models import db, StudentExam, Exam, User
from services.checkin_service import get_checkin_service

student_exam_bp = Blueprint('student_exams', __name__)


@student_exam_bp.route('', methods=['GET'])
def get_student_exams():
    """Get all student-exam registrations"""
    exam_id = request.args.get('exam_id')
    student_id = request.args.get('student_id')
    
    query = StudentExam.query
    
    if exam_id:
        query = query.filter_by(exam_id=exam_id)
    if student_id:
        query = query.filter_by(student_id=student_id)
    
    student_exams = query.all()
    return jsonify([se.to_dict() for se in student_exams]), 200


@student_exam_bp.route('/<int:id>', methods=['GET'])
def get_student_exam(id):
    """Get student-exam by ID"""
    se = StudentExam.query.get(id)
    
    if not se:
        return jsonify({'error': 'StudentExam not found'}), 404
    
    return jsonify(se.to_dict()), 200


@student_exam_bp.route('', methods=['POST'])
@jwt_required()
def create_student_exam():
    """Register a student for an exam"""
    data = request.get_json()
    
    required_fields = ['exam_id', 'student_id']
    for field in required_fields:
        if not data.get(field):
            return jsonify({'error': f'{field} is required'}), 400
    
    # Check duplicates
    existing = StudentExam.query.filter_by(
        exam_id=data['exam_id'],
        student_id=data['student_id']
    ).first()
    if existing:
        return jsonify({'error': 'Student already registered for this exam'}), 409
    
    se = StudentExam(
        exam_id=data['exam_id'],
        student_id=data['student_id'],
        seat_number=data.get('seat_number'),
        status='Registered'
    )
    
    db.session.add(se)
    db.session.commit()
    
    return jsonify(se.to_dict()), 201


@student_exam_bp.route('/<int:id>', methods=['PUT'])
@jwt_required()
def update_student_exam(id):
    """Update student-exam (seat, status)"""
    se = StudentExam.query.get(id)
    
    if not se:
        return jsonify({'error': 'StudentExam not found'}), 404
    
    data = request.get_json()
    
    if data.get('seat_number') is not None:
        se.seat_number = data['seat_number']
    if data.get('status'):
        se.status = data['status']
    
    db.session.commit()
    
    return jsonify(se.to_dict()), 200


@student_exam_bp.route('/<int:id>', methods=['DELETE'])
@jwt_required()
def delete_student_exam(id):
    """Delete student-exam registration"""
    se = StudentExam.query.get(id)
    
    if not se:
        return jsonify({'error': 'StudentExam not found'}), 404
    
    db.session.delete(se)
    db.session.commit()
    
    return jsonify({'message': 'Registration deleted'}), 200


# ============ CHECK-IN ENDPOINTS ============

@student_exam_bp.route('/checkin', methods=['POST'])
def process_checkin():
    """
    Process student check-in with face verification and seating check.
    
    Request body:
    {
        "student_id": 1,
        "exam_id": 1,
        "captured_image_path": "/path/to/photo.jpg" (optional),
        "current_seat": "A1" (optional)
    }
    """
    data = request.get_json()
    
    if not data.get('student_id') or not data.get('exam_id'):
        return jsonify({'error': 'student_id and exam_id required'}), 400
    
    checkin_service = get_checkin_service()
    
    result = checkin_service.process_checkin(
        student_id=data['student_id'],
        exam_id=data['exam_id'],
        captured_image_path=data.get('captured_image_path'),
        current_seat=data.get('current_seat')
    )
    
    status_code = 200 if result.success else 400
    
    return jsonify(result.to_dict()), status_code


@student_exam_bp.route('/verify-seat', methods=['POST'])
def verify_seat():
    """
    Quick seat verification.
    
    Request body:
    {
        "student_id": 1,
        "exam_id": 1,
        "current_seat": "A1"
    }
    """
    data = request.get_json()
    
    required = ['student_id', 'exam_id', 'current_seat']
    for field in required:
        if not data.get(field):
            return jsonify({'error': f'{field} is required'}), 400
    
    checkin_service = get_checkin_service()
    
    result = checkin_service.verify_seat(
        student_id=data['student_id'],
        exam_id=data['exam_id'],
        current_seat=data['current_seat']
    )
    
    return jsonify(result), 200


@student_exam_bp.route('/status/<int:exam_id>', methods=['GET'])
def get_checkin_status(exam_id):
    """Get check-in status for an exam"""
    exam = Exam.query.get(exam_id)
    if not exam:
        return jsonify({'error': 'Exam not found'}), 404
    
    student_exams = StudentExam.query.filter_by(exam_id=exam_id).all()
    
    total = len(student_exams)
    present = len([se for se in student_exams if se.status == 'Present'])
    absent = len([se for se in student_exams if se.status == 'Absent'])
    flagged = len([se for se in student_exams if se.status == 'Flagged'])
    registered = len([se for se in student_exams if se.status == 'Registered'])
    
    return jsonify({
        'exam_id': exam_id,
        'exam_name': exam.name,
        'total_students': total,
        'present': present,
        'absent': absent,
        'flagged': flagged,
        'pending': registered,
        'attendance_rate': round((present / total * 100), 2) if total > 0 else 0,
        'students': [se.to_dict() for se in student_exams]
    }), 200


@student_exam_bp.route('/assign-seats/<int:exam_id>', methods=['POST'])
@jwt_required()
def auto_assign_seats(exam_id):
    """Auto-assign seats for all students in an exam"""
    exam = Exam.query.get(exam_id)
    if not exam:
        return jsonify({'error': 'Exam not found'}), 404
    
    student_exams = StudentExam.query.filter_by(exam_id=exam_id).all()
    
    # Simple seat assignment: A1, A2, A3, B1, B2, B3, etc.
    rows = 'ABCDEFGHIJ'
    cols = 10
    
    for i, se in enumerate(student_exams):
        row = rows[i // cols] if i // cols < len(rows) else 'X'
        col = (i % cols) + 1
        se.seat_number = f"{row}{col}"
    
    db.session.commit()
    
    return jsonify({
        'message': f'Assigned seats to {len(student_exams)} students',
        'students': [se.to_dict() for se in student_exams]
    }), 200
