from app.models.breeding import Cruce, Nidada, ConfigIncubacion
from app.models.bird import Pajaro
from app.extensions import db
from datetime import date

class BreedingService:
    @staticmethod
    def get_all_pairs():
        # Eager load relationships if needed, or rely on lazy loading
        # Based on legacy app.py SQL, we want male/female details
        return Cruce.query.order_by(Cruce.estado, Cruce.id_cruce.desc()).all()

    @staticmethod
    def get_pair_by_id(pair_id):
        return Cruce.query.get(pair_id)

    @staticmethod
    def create_pair(data):
        # Create Pair
        new_pair = Cruce(
            id_macho=data.get('id_macho'),
            id_hembra=data.get('id_hembra'),
            fecha_union=data.get('fecha_union') or date.today(),
            variedad_objetivo=data.get('variedad_objetivo'),
            id_ubicacion=data.get('id_ubicacion'),
            estado='Juntos'
        )
        db.session.add(new_pair)
        db.session.flush() # get ID

        # Automation: Create First Clutch
        first_clutch = Nidada(
            id_cruce=new_pair.id_cruce,
            numero_nidada=1,
            estado='Puesta',
            huevos_totales=0
        )
        db.session.add(first_clutch)
        
        db.session.commit()
        return new_pair

    @staticmethod
    def update_pair(pair_id, data):
        pair = Cruce.query.get(pair_id)
        if not pair:
            return None
            
        allowed = ['estado', 'fecha_separacion', 'variedad_objetivo', 'id_ubicacion', 'fecha_union', 'id_macho', 'id_hembra']
        for key in allowed:
            if key in data:
                setattr(pair, key, data[key])
        
        db.session.commit()
        return pair

    @staticmethod
    def delete_pair(pair_id):
        pair = Cruce.query.get(pair_id)
        if not pair:
            return False
        
        # Cascade delete (handled by relationship cascade usually, but explicit here if needed)
        # Nidadas are cascade='all, delete-orphan' in model definition
        db.session.delete(pair)
        db.session.commit()
        return True

    @staticmethod
    def get_clutches_by_pair(pair_id):
        return Nidada.query.filter_by(id_cruce=pair_id).order_by(Nidada.numero_nidada).all()
        
    @staticmethod
    def get_clutch_by_id(clutch_id):
        return Nidada.query.get(clutch_id)

    @staticmethod
    def create_clutch(data):
        new_clutch = Nidada(
            id_cruce=data.get('id_cruce'),
            numero_nidada=data.get('numero_nidada'),
            estado=data.get('estado', 'Puesta'),
            fecha_primer_huevo=data.get('fecha_primer_huevo')
        )
        db.session.add(new_clutch)
        db.session.commit()
        return new_clutch

    @staticmethod
    def update_clutch(clutch_id, data):
        clutch = Nidada.query.get(clutch_id)
        if not clutch:
            return None
            
        # Allow any field update from model
        for key, value in data.items():
            if hasattr(clutch, key):
                setattr(clutch, key, value)
                
        db.session.commit()
        return clutch

    @staticmethod
    def delete_clutch(clutch_id):
        clutch = Nidada.query.get(clutch_id)
        if not clutch:
            return False
        db.session.delete(clutch)
        db.session.commit()
        return True

    @staticmethod
    def get_incubation_parameters():
        return ConfigIncubacion.query.all()
