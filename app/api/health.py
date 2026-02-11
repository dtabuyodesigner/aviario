from flask import Blueprint, jsonify, request
from app.services.health_service import HealthService

bp = Blueprint('health', __name__)

# TREATMENTS
@bp.route('/treatments', methods=['GET'])
def get_treatments():
    active = request.args.get('active', 'false').lower() == 'true'
    treatments = HealthService.get_treatments(active)
    return jsonify([t.to_dict() for t in treatments])

@bp.route('/treatments', methods=['POST'])
def create_treatment():
    data = request.get_json()
    try:
        t = HealthService.create_treatment(data)
        return jsonify({'id': t.id_tratamiento}), 201
    except Exception as e:
        return jsonify({'error': str(e)}), 400

@bp.route('/treatments/<int:id>', methods=['PUT'])
def update_treatment(id):
    data = request.get_json()
    try:
        t = HealthService.update_treatment(id, data)
        if not t:
            return jsonify({'error': 'Treatment not found'}), 404
        return jsonify({'message': 'Treatment updated'})
    except Exception as e:
        return jsonify({'error': str(e)}), 400

@bp.route('/treatments/<int:id>', methods=['DELETE'])
def delete_treatment(id):
    try:
        success = HealthService.delete_treatment(id)
        if not success:
             return jsonify({'error': 'Treatment not found'}), 404
        return jsonify({'message': 'Treatment deleted'})
    except Exception as e:
        return jsonify({'error': str(e)}), 400

# RECIPES
@bp.route('/recipes', methods=['GET'])
def get_recipes():
    recipes = HealthService.get_all_recipes()
    return jsonify([r.to_dict() for r in recipes])

@bp.route('/recipes', methods=['POST'])
def create_recipe():
    data = request.get_json()
    try:
        r = HealthService.create_recipe(data)
        return jsonify({'id': r.id_receta}), 201
    except Exception as e:
         return jsonify({'error': str(e)}), 400

@bp.route('/recipes/<int:id>', methods=['PUT'])
def update_recipe(id):
    data = request.get_json()
    try:
        r = HealthService.update_recipe(id, data)
        if not r:
             return jsonify({'error': 'Recipe not found'}), 404
        return jsonify({'message': 'Recipe updated'})
    except Exception as e:
        return jsonify({'error': str(e)}), 400

@bp.route('/recipes/<int:id>', methods=['DELETE'])
def delete_recipe(id):
    try:
        success = HealthService.delete_recipe(id)
        if not success:
            return jsonify({'error': 'Recipe not found'}), 404
        return jsonify({'message': 'Recipe deleted'})
    except Exception as e:
        return jsonify({'error': str(e)}), 400
