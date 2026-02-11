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
    from flask import request
    species = request.args.get('species')
    variety_uuid = request.args.get('variety_uuid')
    
    if species or variety_uuid:
        mutations = GeneticsService.get_mutations_filtered(species, variety_uuid)
    else:
        mutations = GeneticsService.get_all_mutations()
        
    return jsonify([m.to_dict() for m in mutations])

@bp.route('/varieties', methods=['GET'])
def get_all_varieties():
    from flask import request
    from app.services.genetics_service import GeneticsService
    species_uuid = request.args.get('species_uuid')
    
    if species_uuid:
        varieties = GeneticsService.get_varieties_by_species(species_uuid)
    else:
        from app.models.genetics import Variedad
        varieties = Variedad.query.all()
        
    return jsonify([v.to_dict() for v in varieties])

@bp.route('/canary_breeds', methods=['GET'])
def get_canary_breeds():
    from flask import request
    from app.models.genetics import CanaryBreed
    
    variety_uuid = request.args.get('variety_uuid')
    
    query = CanaryBreed.query
    if variety_uuid:
        query = query.filter_by(variedad_uuid=variety_uuid)
    
    breeds = query.all()
    return jsonify([b.to_dict() for b in breeds])
