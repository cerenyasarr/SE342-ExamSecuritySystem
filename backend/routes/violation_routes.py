from flask import Blueprint, request, jsonify
from flask_jwt_extended import jwt_required
from datetime import datetime
from models import db, Violation, StudentExam, Exam

violation_bp = Blueprint('violations', __name__)


@violation_bp.route('', methods=['GET'])
def get_violations():
    """Get all violations"""
    exam_id = request.args.get('exam_id')
    violation_type = request.args.get('type')
    
    query = Violation.query
    
    if exam_id:
        # Get student_exams for this exam
        se_ids = [se.id for se in StudentExam.query.filter_by(exam_id=exam_id).all()]
        query = query.filter(Violation.student_exam_id.in_(se_ids))
    
    if violation_type:
        query = query.filter_by(violation_type=violation_type)
    
    violations = query.order_by(Violation.detected_at.desc()).all()
    
    return jsonify([v.to_dict() for v in violations]), 200


@violation_bp.route('/<int:violation_id>', methods=['GET'])
def get_violation(violation_id):
    """Get violation by ID"""
    violation = Violation.query.get(violation_id)
    
    if not violation:
        return jsonify({'error': 'Violation not found'}), 404
    
    return jsonify(violation.to_dict()), 200


@violation_bp.route('', methods=['POST'])
@jwt_required()
def create_violation():
    """Report a new violation"""
    data = request.get_json()
    
    required_fields = ['student_exam_id', 'violation_type']
    for field in required_fields:
        if not data.get(field):
            return jsonify({'error': f'{field} is required'}), 400
    
    # Check if student_exam exists
    se = StudentExam.query.get(data['student_exam_id'])
    if not se:
        return jsonify({'error': 'StudentExam not found'}), 404
    
    violation = Violation(
        student_exam_id=data['student_exam_id'],
        violation_type=data['violation_type'],
        description=data.get('description'),
        evidence_url=data.get('evidence_url'),
        status=data.get('status', 'Pending Review')
    )
    
    # Update student exam status to Flagged
    se.status = 'Flagged'
    
    db.session.add(violation)
    db.session.commit()
    
    return jsonify(violation.to_dict()), 201


@violation_bp.route('/<int:violation_id>', methods=['PUT'])
@jwt_required()
def update_violation(violation_id):
    """Update violation"""
    violation = Violation.query.get(violation_id)
    
    if not violation:
        return jsonify({'error': 'Violation not found'}), 404
    
    data = request.get_json()
    
    if data.get('violation_type'):
        violation.violation_type = data['violation_type']
    if data.get('description'):
        violation.description = data['description']
    if data.get('evidence_url'):
        violation.evidence_url = data['evidence_url']
    if data.get('status'):
        violation.status = data['status']
    
    db.session.commit()
    
    return jsonify(violation.to_dict()), 200


@violation_bp.route('/<int:violation_id>', methods=['DELETE'])
@jwt_required()
def delete_violation(violation_id):
    """Delete violation"""
    violation = Violation.query.get(violation_id)
    
    if not violation:
        return jsonify({'error': 'Violation not found'}), 404
    
    db.session.delete(violation)
    db.session.commit()
    
    return jsonify({'message': 'Violation deleted successfully'}), 200


@violation_bp.route('/exam/<int:exam_id>', methods=['GET'])
def get_exam_violations(exam_id):
    """Get all violations for an exam"""
    exam = Exam.query.get(exam_id)
    if not exam:
        return jsonify({'error': 'Exam not found'}), 404
    
    se_ids = [se.id for se in StudentExam.query.filter_by(exam_id=exam_id).all()]
    violations = Violation.query.filter(Violation.student_exam_id.in_(se_ids)).all()
    
    return jsonify({
        'exam_id': exam_id,
        'exam_name': exam.name,
        'total_violations': len(violations),
        'violations': [v.to_dict() for v in violations]
    }), 200


@violation_bp.route('/types', methods=['GET'])
def get_violation_types():
    """Get list of violation types"""
    types = [
        {'code': 'face_mismatch', 'name': 'Yüz Uyuşmazlığı'},
        {'code': 'wrong_seat', 'name': 'Yanlış Koltuk'},
        {'code': 'phone_detected', 'name': 'Telefon Tespit Edildi'},
        {'code': 'talking', 'name': 'Konuşma'},
        {'code': 'looking_around', 'name': 'Etrafı Süzme'},
        {'code': 'unauthorized_material', 'name': 'Yetkisiz Materyal'},
        {'code': 'absence', 'name': 'Devamsızlık'},
        {'code': 'other', 'name': 'Diğer'}
    ]
    return jsonify(types), 200
