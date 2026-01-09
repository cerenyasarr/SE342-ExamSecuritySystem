from flask import Blueprint, request, jsonify
from flask_jwt_extended import jwt_required
from src.models import db, Room

room_bp = Blueprint('rooms', __name__)


@room_bp.route('', methods=['GET'])
def get_rooms():
    """Get all rooms"""
    rooms = Room.query.all()
    return jsonify([r.to_dict() for r in rooms]), 200


@room_bp.route('/<room_id>', methods=['GET'])
def get_room(room_id):
    """Get a room by ID"""
    room = Room.query.get(room_id)
    if not room:
        return jsonify({'error': 'Room not found'}), 404
    return jsonify(room.to_dict()), 200


@room_bp.route('', methods=['POST'])
@jwt_required()
def create_room():
    """Create a new room"""
    data = request.get_json()
    
    required_fields = ['room_name', 'capacity']
    for field in required_fields:
        if field not in data:
            return jsonify({'error': f'{field} is required'}), 400
    
    room = Room(
        room_name=data['room_name'],
        capacity=data['capacity'],
        total_rows=data.get('total_rows'),
        total_columns=data.get('total_columns')
    )
    
    db.session.add(room)
    db.session.commit()
    
    return jsonify(room.to_dict()), 201


@room_bp.route('/<room_id>', methods=['PUT'])
@jwt_required()
def update_room(room_id):
    """Update a room"""
    room = Room.query.get(room_id)
    if not room:
        return jsonify({'error': 'Room not found'}), 404
    
    data = request.get_json()
    
    if 'room_name' in data:
        room.room_name = data['room_name']
    if 'capacity' in data:
        room.capacity = data['capacity']
    if 'total_rows' in data:
        room.total_rows = data['total_rows']
    if 'total_columns' in data:
        room.total_columns = data['total_columns']
    
    db.session.commit()
    return jsonify(room.to_dict()), 200


@room_bp.route('/<room_id>', methods=['DELETE'])
@jwt_required()
def delete_room(room_id):
    """Delete a room"""
    room = Room.query.get(room_id)
    if not room:
        return jsonify({'error': 'Room not found'}), 404
    
    db.session.delete(room)
    db.session.commit()
    return jsonify({'message': 'Room deleted'}), 200
