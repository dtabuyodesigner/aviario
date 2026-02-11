from flask import Blueprint, jsonify, request
from app.services.breeding_service import BreedingService

bp = Blueprint('breeding', __name__)

# PAIRS
@bp.route('/pairs', methods=['GET'])
def get_pairs():
    # Frontend expects filtering or order?
    # Logic in service is simple order_by.
    pairs = BreedingService.get_all_pairs()
    return jsonify([p.to_dict() for p in pairs])

@bp.route('/pairs', methods=['POST'])
def create_pair():
    data = request.get_json()
    try:
        new_pair = BreedingService.create_pair(data)
        return jsonify(new_pair.to_dict()), 201
    except Exception as e:
        return jsonify({'error': str(e)}), 400

@bp.route('/pairs/<int:id>', methods=['PUT'])
def update_pair(id):
    data = request.get_json()
    try:
        pair = BreedingService.update_pair(id, data)
        if not pair:
            return jsonify({'error': 'Pair not found'}), 404
        return jsonify(pair.to_dict())
    except Exception as e:
        return jsonify({'error': str(e)}), 400

@bp.route('/pairs/<int:id>', methods=['DELETE'])
def delete_pair(id):
    try:
        success = BreedingService.delete_pair(id)
        if not success:
            return jsonify({'error': 'Pair not found'}), 404
        return jsonify({'message': 'Pair deleted'})
    except Exception as e:
        return jsonify({'error': str(e)}), 400

# CLUTCHES
@bp.route('/pairs/<int:pair_id>/clutches', methods=['GET'])
def get_clutches(pair_id):
    clutches = BreedingService.get_clutches_by_pair(pair_id)
    return jsonify([c.to_dict() for c in clutches])

@bp.route('/clutches', methods=['POST'])
def create_clutch():
    data = request.get_json()
    try:
        new_clutch = BreedingService.create_clutch(data)
        return jsonify(new_clutch.to_dict()), 201
    except Exception as e:
        return jsonify({'error': str(e)}), 400
        
@bp.route('/clutches/<int:id>', methods=['PUT'])
def update_clutch(id):
    data = request.get_json()
    try:
        clutch = BreedingService.update_clutch(id, data)
        if not clutch:
            return jsonify({'error': 'Clutch not found'}), 404
        return jsonify(clutch.to_dict())
    except Exception as e:
        return jsonify({'error': str(e)}), 400

@bp.route('/clutches/<int:id>', methods=['DELETE'])
def delete_clutch(id):
    try:
        success = BreedingService.delete_clutch(id)
        if not success:
            return jsonify({'error': 'Clutch not found'}), 404
        return jsonify({'message': 'Clutch deleted'})
    except Exception as e:
        return jsonify({'error': str(e)}), 400

# CONFIG
@bp.route('/incubation-parameters', methods=['GET'])
def get_params():
    params = BreedingService.get_incubation_parameters()
    return jsonify([p.to_dict() for p in params])
