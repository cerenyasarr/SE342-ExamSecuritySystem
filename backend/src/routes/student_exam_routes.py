from flask import Blueprint, request, jsonify
from flask_jwt_extended import jwt_required
from datetime import datetime
from src.models import db, ExamEnrollment, Exam, Student, CheckInLog

student_exam_bp = Blueprint('student_exams', __name__)


@student_exam_bp.route('', methods=['GET'])
@jwt_required()
def get_enrollments():
    """Get all exam enrollments"""
    enrollments = ExamEnrollment.query.all()
    return jsonify([e.to_dict() for e in enrollments]), 200


@student_exam_bp.route('/<enrollment_id>', methods=['GET'])
def get_enrollment(enrollment_id):
    """Get an enrollment by ID"""
    enrollment = ExamEnrollment.query.get(enrollment_id)
    if not enrollment:
        return jsonify({'error': 'Enrollment not found'}), 404
    return jsonify(enrollment.to_dict()), 200


@student_exam_bp.route('', methods=['POST'])
@jwt_required()
def create_enrollment():
    """Enroll a student in an exam"""
    data = request.get_json()
    
    required_fields = ['exam_id', 'student_id']
    for field in required_fields:
        if field not in data:
            return jsonify({'error': f'{field} is required'}), 400
    
    # Check if already enrolled
    existing = ExamEnrollment.query.filter_by(
        exam_id=data['exam_id'],
        student_id=data['student_id']
    ).first()
    
    if existing:
        return jsonify({'error': 'Student already enrolled in this exam'}), 409
    
    enrollment = ExamEnrollment(
        exam_id=data['exam_id'],
        student_id=data['student_id'],
        assigned_row=data.get('assigned_row'),
        assigned_col=data.get('assigned_col'),
        status='registered'
    )
    
    db.session.add(enrollment)
    db.session.commit()
    
    return jsonify(enrollment.to_dict()), 201


@student_exam_bp.route('/<enrollment_id>', methods=['PUT'])
@jwt_required()
def update_enrollment(enrollment_id):
    """Update an enrollment"""
    enrollment = ExamEnrollment.query.get(enrollment_id)
    if not enrollment:
        return jsonify({'error': 'Enrollment not found'}), 404
    
    data = request.get_json()
    
    if 'assigned_row' in data:
        enrollment.assigned_row = data['assigned_row']
    if 'assigned_col' in data:
        enrollment.assigned_col = data['assigned_col']
    if 'status' in data:
        enrollment.status = data['status']
    
    db.session.commit()
    return jsonify(enrollment.to_dict()), 200


@student_exam_bp.route('/<enrollment_id>', methods=['DELETE'])
@jwt_required()
def delete_enrollment(enrollment_id):
    """Delete an enrollment"""
    enrollment = ExamEnrollment.query.get(enrollment_id)
    if not enrollment:
        return jsonify({'error': 'Enrollment not found'}), 404
    
    db.session.delete(enrollment)
    db.session.commit()
    return jsonify({'message': 'Enrollment deleted'}), 200


@student_exam_bp.route('/checkin', methods=['POST'])
@jwt_required()
def process_checkin():
    """Process student check-in"""
    data = request.get_json()
    
    required_fields = ['exam_id', 'student_id']
    for field in required_fields:
        if field not in data:
            return jsonify({'error': f'{field} is required'}), 400
    
    # Find enrollment
    enrollment = ExamEnrollment.query.filter_by(
        exam_id=data['exam_id'],
        student_id=data['student_id']
    ).first()
    
    if not enrollment:
        return jsonify({'error': 'Student not enrolled in this exam'}), 404
    
    # Check seat
    current_row = data.get('current_row')
    current_col = data.get('current_col')
    is_seat_correct = True
    
    if current_row and current_col:
        is_seat_correct = (
            enrollment.assigned_row == current_row and
            enrollment.assigned_col == current_col
        )
    
    # Create check-in log
    log = CheckInLog(
        enrollment_id=enrollment.enrollment_id,
        captured_image_path=data.get('captured_image_path'),
        confidence_score=data.get('confidence_score', 1.0),
        is_verified=data.get('is_verified', True),
        is_seat_correct=is_seat_correct
    )
    
    # Update enrollment status
    if is_seat_correct:
        enrollment.status = 'attended'
    
    db.session.add(log)
    db.session.commit()
    
    return jsonify({
        'success': True,
        'message': 'Check-in successful' if is_seat_correct else 'Check-in with wrong seat',
        'enrollment': enrollment.to_dict(),
        'is_seat_correct': is_seat_correct
    }), 200


@student_exam_bp.route('/exam/<exam_id>/status', methods=['GET'])
def get_exam_status(exam_id):
    """Get exam attendance status"""
    exam = Exam.query.get(exam_id)
    if not exam:
        return jsonify({'error': 'Exam not found'}), 404
    
    enrollments = ExamEnrollment.query.filter_by(exam_id=exam_id).all()
    
    total = len(enrollments)
    attended = len([e for e in enrollments if e.status == 'attended'])
    registered = len([e for e in enrollments if e.status == 'registered'])
    
    return jsonify({
        'exam_id': exam_id,
        'exam_title': exam.exam_title,
        'total_enrolled': total,
        'attended': attended,
        'pending': registered,
        'attendance_rate': round((attended / total * 100), 1) if total > 0 else 0,
        'students': [e.to_dict() for e in enrollments]
    }), 200


@student_exam_bp.route('/exam/<exam_id>/assign-seats', methods=['POST'])
@jwt_required()
def auto_assign_seats(exam_id):
    """Auto-assign seats for an exam"""
    exam = Exam.query.get(exam_id)
    if not exam:
        return jsonify({'error': 'Exam not found'}), 404
    
    room = exam.room
    if not room:
        return jsonify({'error': 'No room assigned to exam'}), 400
    
    enrollments = ExamEnrollment.query.filter_by(exam_id=exam_id).all()
    
    rows = room.total_rows or 5
    cols = room.total_columns or 6
    
    seat_index = 0
    for enrollment in enrollments:
        row = (seat_index // cols) + 1
        col = (seat_index % cols) + 1
        enrollment.assigned_row = row
        enrollment.assigned_col = col
        seat_index += 1
    
    db.session.commit()
    
    return jsonify({
        'message': f'Assigned seats for {len(enrollments)} students',
        'students': [e.to_dict() for e in enrollments]
    }), 200
