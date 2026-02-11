from flask import Blueprint, jsonify, request
from app.services.bird_service import BirdService

bp = Blueprint('birds', __name__)

@bp.route('/', methods=['GET'])
def get_birds():
    """Get all birds from optimized VIEW"""
    filters = request.args.to_dict()
    birds = BirdService.get_all_birds(filters)
    # Birds already returned as dicts from VIEW query
    return jsonify(birds)

@bp.route('/<id>', methods=['GET'])
def get_bird(id):
    """Get single bird with full genetics and state"""
    bird = BirdService.get_bird_by_id(id)
    if not bird:
        return jsonify({'error': 'Bird not found'}), 404
    # Bird already returned as dict with nested data
    return jsonify(bird)

@bp.route('/', methods=['POST'])
def create_bird():
    """Create bird with genetics and initial state"""
    data = request.get_json() or request.form.to_dict()
    try:
        bird = BirdService.create_bird(data)
        return jsonify(bird.to_dict()), 201
    except Exception as e:
        return jsonify({'error': str(e)}), 400

@bp.route('/<id>', methods=['PUT'])
def update_bird(id):
    """Update bird including genetics and state"""
    data = request.get_json() or request.form.to_dict()
    try:
        bird = BirdService.update_bird(id, data)
        if not bird:
            return jsonify({'error': 'Bird not found'}), 404
        return jsonify(bird.to_dict())
    except Exception as e:
        return jsonify({'error': str(e)}), 400

@bp.route('/<id>', methods=['DELETE'])
def delete_bird(id):
    """Soft delete bird"""
    try:
        success = BirdService.delete_bird(id)
        if not success:
            return jsonify({'error': 'Bird not found'}), 404
        return jsonify({'message': 'Bird deleted successfully'})
    except Exception as e:
        return jsonify({'error': str(e)}), 400

@bp.route('/<int:id>/history', methods=['GET'])
def get_bird_history(id):
    """Get event history for a bird"""
    try:
        history = BirdService.get_bird_history(id)
        return jsonify(history)
    except Exception as e:
        return jsonify({'error': str(e)}), 400

@bp.route('/<int:id>/events', methods=['POST'])
def add_bird_event(id):
    """Add an event to bird history"""
    data = request.get_json()
    try:
        event = BirdService.add_bird_event(id, data)
        return jsonify(event.to_dict()), 201
    except Exception as e:
        return jsonify({'error': str(e)}), 400
