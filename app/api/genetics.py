from flask import Blueprint, jsonify
from app.services.genetics_service import GeneticsService

bp = Blueprint('genetics', __name__)

@bp.route('/species', methods=['GET'])
def get_species():
    species = GeneticsService.get_all_species()
    return jsonify([s.to_dict() for s in species])

@bp.route('/species/<uuid>/varieties', methods=['GET'])
def get_varieties(uuid):
    varieties = GeneticsService.get_varieties_by_species(uuid)
    return jsonify([v.to_dict() for v in varieties])

@bp.route('/varieties/<uuid>/mutations', methods=['GET'])
def get_mutations(uuid):
    mutations = GeneticsService.get_mutations_by_variety(uuid)
    return jsonify([m.to_dict() for m in mutations])

@bp.route('/mutations', methods=['GET'])
def get_all_mutations():
    mutations = GeneticsService.get_all_mutations()
    return jsonify([m.to_dict() for m in mutations])
