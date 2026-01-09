from flask import Blueprint, request, jsonify
from flask_jwt_extended import jwt_required
from models import db, Room

room_bp = Blueprint('rooms', __name__)


@room_bp.route('', methods=['GET'])
def get_rooms():
    """Get all rooms"""
    rooms = Room.query.all()
    return jsonify([room.to_dict() for room in rooms]), 200


@room_bp.route('/<int:room_id>', methods=['GET'])
def get_room(room_id):
    """Get room by ID"""
    room = Room.query.get(room_id)
    
    if not room:
        return jsonify({'error': 'Room not found'}), 404
    
    return jsonify(room.to_dict()), 200


@room_bp.route('', methods=['POST'])
@jwt_required()
def create_room():
    """Create a new room"""
    data = request.get_json()
    
    required_fields = ['name', 'capacity']
    for field in required_fields:
        if not data.get(field):
            return jsonify({'error': f'{field} is required'}), 400
    
    room = Room(
        name=data['name'],
        capacity=data['capacity'],
        layout_config=data.get('layout_config')
    )
    
    db.session.add(room)
    db.session.commit()
    
    return jsonify(room.to_dict()), 201


@room_bp.route('/<int:room_id>', methods=['PUT'])
@jwt_required()
def update_room(room_id):
    """Update room"""
    room = Room.query.get(room_id)
    
    if not room:
        return jsonify({'error': 'Room not found'}), 404
    
    data = request.get_json()
    
    if data.get('name'):
        room.name = data['name']
    if data.get('capacity'):
        room.capacity = data['capacity']
    if data.get('layout_config') is not None:
        room.layout_config = data['layout_config']
    
    db.session.commit()
    
    return jsonify(room.to_dict()), 200


@room_bp.route('/<int:room_id>', methods=['DELETE'])
@jwt_required()
def delete_room(room_id):
    """Delete room"""
    room = Room.query.get(room_id)
    
    if not room:
        return jsonify({'error': 'Room not found'}), 404
    
    db.session.delete(room)
    db.session.commit()
    
    return jsonify({'message': 'Room deleted successfully'}), 200
