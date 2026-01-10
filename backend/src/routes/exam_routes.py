from flask import Blueprint, request, jsonify
from flask_jwt_extended import jwt_required
from datetime import datetime
from src.models import db, Exam, ExamEnrollment

exam_bp = Blueprint('exams', __name__)


def parse_datetime(dt_string):
    """Parse datetime string from frontend (ISO format)"""
    if not dt_string:
        return None
    try:
        # Try ISO format first (2026-01-10T14:30:00)
        if 'T' in dt_string:
            # Handle with or without seconds
            if len(dt_string) == 16:  # 2026-01-10T14:30
                return datetime.strptime(dt_string, '%Y-%m-%dT%H:%M')
            else:
                return datetime.fromisoformat(dt_string.replace('Z', '+00:00'))
        else:
            return datetime.strptime(dt_string, '%Y-%m-%d %H:%M:%S')
    except Exception as e:
        print(f"[DEBUG] DateTime parse error: {e}, input: {dt_string}")
        return None


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
    
    # Parse datetime strings
    start_time = parse_datetime(data['start_time'])
    end_time = parse_datetime(data['end_time'])
    
    if not start_time or not end_time:
        return jsonify({'error': 'Invalid datetime format'}), 400
    
    exam = Exam(
        course_code=data['course_code'],
        exam_title=data['exam_title'],
        start_time=start_time,
        end_time=end_time,
        status=data.get('status', 'scheduled'),
        room_id=data.get('room_id') if data.get('room_id') else None,
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
        parsed_start = parse_datetime(data['start_time'])
        if parsed_start:
            exam.start_time = parsed_start
    if 'end_time' in data:
        parsed_end = parse_datetime(data['end_time'])
        if parsed_end:
            exam.end_time = parsed_end
    if 'status' in data:
        exam.status = data['status']
    if 'room_id' in data:
        exam.room_id = data['room_id'] if data['room_id'] else None
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


@exam_bp.route('/<exam_id>/seats', methods=['GET'])
def get_exam_seats(exam_id):
    """Get seat status for an exam - which seats are occupied"""
    from src.models import Room
    
    exam = Exam.query.get(exam_id)
    if not exam:
        return jsonify({'error': 'Exam not found'}), 404
    
    # Get room info
    room = exam.room
    if not room:
        return jsonify({
            'error': 'No room assigned to this exam',
            'has_room': False
        }), 200
    
    # Get all enrollments with seat assignments
    enrollments = ExamEnrollment.query.filter_by(exam_id=exam_id).all()
    
    # Build occupied seats list
    occupied_seats = []
    for e in enrollments:
        if e.assigned_row and e.assigned_col:
            occupied_seats.append({
                'row': e.assigned_row,
                'col': e.assigned_col,
                'student_id': e.student_id,
                'student_name': e.student.full_name if e.student else None,
                'enrollment_id': e.enrollment_id
            })
    
    return jsonify({
        'has_room': True,
        'room_id': room.room_id,
        'room_name': room.room_name,
        'total_rows': room.total_rows or 5,
        'total_columns': room.total_columns or 6,
        'capacity': room.capacity,
        'occupied_seats': occupied_seats,
        'occupied_count': len(occupied_seats)
    }), 200
