from flask import Blueprint, jsonify, request
from app.services.bird_service import BirdService

bp = Blueprint('birds', __name__)

@bp.route('/', methods=['GET'])
def get_birds():
    filters = request.args.to_dict()
    birds = BirdService.get_all_birds(filters)
    return jsonify([bird.to_dict() for bird in birds])

@bp.route('/<int:id>', methods=['GET'])
def get_bird(id):
    bird = BirdService.get_bird_by_id(id)
    if not bird:
        return jsonify({'error': 'Bird not found'}), 404
    return jsonify(bird.to_dict())

@bp.route('/', methods=['POST'])
def create_bird():
    data = request.get_json() or request.form.to_dict()
    try:
        bird = BirdService.create_bird(data)
        return jsonify(bird.to_dict()), 201
    except Exception as e:
        return jsonify({'error': str(e)}), 400

@bp.route('/<int:id>', methods=['PUT'])
def update_bird(id):
    data = request.get_json() or request.form.to_dict()
    try:
        bird = BirdService.update_bird(id, data)
        if not bird:
            return jsonify({'error': 'Bird not found'}), 404
        return jsonify(bird.to_dict())
    except Exception as e:
        return jsonify({'error': str(e)}), 400

@bp.route('/<int:id>', methods=['DELETE'])
def delete_bird(id):
    try:
        success = BirdService.delete_bird(id)
        if not success:
            return jsonify({'error': 'Bird not found'}), 404
        return jsonify({'message': 'Bird deleted successfully'})
    except Exception as e:
        return jsonify({'error': str(e)}), 400
