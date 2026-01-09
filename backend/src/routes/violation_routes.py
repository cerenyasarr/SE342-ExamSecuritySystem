from flask import Blueprint, request, jsonify
from flask_jwt_extended import jwt_required
from datetime import datetime
from src.models import db, Violation, ExamEnrollment, Exam

violation_bp = Blueprint('violations', __name__)


@violation_bp.route('', methods=['GET'])
def get_violations():
    """Get all violations"""
    violations = Violation.query.all()
    return jsonify([v.to_dict() for v in violations]), 200


@violation_bp.route('/<violation_id>', methods=['GET'])
def get_violation(violation_id):
    """Get a violation by ID"""
    violation = Violation.query.get(violation_id)
    if not violation:
        return jsonify({'error': 'Violation not found'}), 404
    return jsonify(violation.to_dict()), 200


@violation_bp.route('', methods=['POST'])
@jwt_required()
def create_violation():
    """Create a new violation"""
    data = request.get_json()
    
    required_fields = ['enrollment_id', 'violation_type']
    for field in required_fields:
        if field not in data:
            return jsonify({'error': f'{field} is required'}), 400
    
    # Verify enrollment exists
    enrollment = ExamEnrollment.query.get(data['enrollment_id'])
    if not enrollment:
        return jsonify({'error': 'Enrollment not found'}), 404
    
    violation = Violation(
        enrollment_id=data['enrollment_id'],
        violation_type=data['violation_type'],
        description=data.get('description'),
        evidence_image_path=data.get('evidence_image_path')
    )
    
    db.session.add(violation)
    db.session.commit()
    
    return jsonify(violation.to_dict()), 201


@violation_bp.route('/<violation_id>', methods=['PUT'])
@jwt_required()
def update_violation(violation_id):
    """Update a violation"""
    violation = Violation.query.get(violation_id)
    if not violation:
        return jsonify({'error': 'Violation not found'}), 404
    
    data = request.get_json()
    
    if 'violation_type' in data:
        violation.violation_type = data['violation_type']
    if 'description' in data:
        violation.description = data['description']
    if 'evidence_image_path' in data:
        violation.evidence_image_path = data['evidence_image_path']
    
    db.session.commit()
    return jsonify(violation.to_dict()), 200


@violation_bp.route('/<violation_id>', methods=['DELETE'])
@jwt_required()
def delete_violation(violation_id):
    """Delete a violation"""
    violation = Violation.query.get(violation_id)
    if not violation:
        return jsonify({'error': 'Violation not found'}), 404
    
    db.session.delete(violation)
    db.session.commit()
    return jsonify({'message': 'Violation deleted'}), 200


@violation_bp.route('/exam/<exam_id>', methods=['GET'])
def get_violations_by_exam(exam_id):
    """Get all violations for an exam"""
    exam = Exam.query.get(exam_id)
    if not exam:
        return jsonify({'error': 'Exam not found'}), 404
    
    enrollments = ExamEnrollment.query.filter_by(exam_id=exam_id).all()
    enrollment_ids = [e.enrollment_id for e in enrollments]
    
    violations = Violation.query.filter(Violation.enrollment_id.in_(enrollment_ids)).all()
    
    return jsonify({
        'exam_id': exam_id,
        'exam_title': exam.exam_title,
        'violations': [v.to_dict() for v in violations]
    }), 200


@violation_bp.route('/types', methods=['GET'])
def get_violation_types():
    """Get available violation types"""
    return jsonify([
        {'code': 'face_mismatch', 'name': 'Yüz Uyuşmazlığı'},
        {'code': 'wrong_seat', 'name': 'Yanlış Koltuk'},
        {'code': 'phone_detected', 'name': 'Telefon Tespit Edildi'},
        {'code': 'talking', 'name': 'Konuşma'},
        {'code': 'looking_around', 'name': 'Etrafı İzleme'},
        {'code': 'unauthorized_material', 'name': 'İzinsiz Materyal'},
        {'code': 'absence', 'name': 'Devamsızlık'},
        {'code': 'other', 'name': 'Diğer'}
    ]), 200
