from app.extensions import db
from app.models.bird import Pajaro, PajaroGenetica, PajaroEstado, PajaroEvento
from app.models.genetics import Especie, Mutacion
from sqlalchemy.exc import SQLAlchemyError
from sqlalchemy import text
import uuid as uuid_lib
from datetime import datetime

class BirdService:
    @staticmethod
    def get_all_birds(filters=None):
        """Get all birds using the optimized VIEW"""
        query = text("""
            SELECT * FROM vista_pajaros_listado
            ORDER BY created_at DESC
        """)
        
        result = db.session.execute(query)
        return [dict(row._mapping) for row in result]

    @staticmethod
    def get_bird_by_id(bird_uuid):
        """Get bird with all related data using UUID"""
        bird = Pajaro.query.get(bird_uuid)
        if not bird:
            # Fallback for old views that might still send integer IDs if any exist
            # but ideally everything is UUID now
            return None
            
        bird_dict = bird.to_dict()
        
        # Add genetics from view or relation
        query_gen = text("SELECT * FROM vista_pajaro_genetica WHERE pajaro_uuid = :uuid")
        res_gen = db.session.execute(query_gen, {"uuid": bird_uuid})
        bird_dict['genetica'] = [dict(row._mapping) for row in res_gen]
            
        return bird_dict

    @staticmethod
    def create_bird(data):
        """
        Create bird using the Final Model:
        1. Insert into pajaros
        2. Insert associated genetics
        """
        try:
            # Generate UUID
            bird_uuid = data.get('uuid') or str(uuid_lib.uuid4())
            
            # Extract genetics
            genetics_data = data.pop('genetica', [])
            
            # Clean and convert data types
            for key in list(data.keys()):
                if data[key] == '':
                    data[key] = None
            
            # Convert fecha_nacimiento
            if data.get('fecha_nacimiento') and isinstance(data['fecha_nacimiento'], str):
                from datetime import datetime as dt
                try:
                    data['fecha_nacimiento'] = dt.strptime(data['fecha_nacimiento'], '%Y-%m-%d').date()
                except ValueError:
                    data['fecha_nacimiento'] = None
            
            # 1. Create bird record
            data['uuid'] = bird_uuid
            data['estado'] = data.get('estado', 'Activo')
            data['created_at'] = datetime.utcnow().isoformat()
            data['sync_version'] = 1
            
            new_bird = Pajaro(**data)
            db.session.add(new_bird)
            db.session.flush() 
            
            # 2. Create genetics records
            for gen in genetics_data:
                genetica = PajaroGenetica(
                    uuid=str(uuid_lib.uuid4()),
                    bird_uuid=bird_uuid,
                    mutacion_uuid=gen.get('mutacion_uuid'),
                    expresion=gen.get('expresion', 'Visual'),
                    genotipo=gen.get('genotipo', '')
                )
                db.session.add(genetica)
            
            db.session.commit()
            return new_bird
            
        except SQLAlchemyError as e:
            db.session.rollback()
            raise e

    @staticmethod
    def update_bird(bird_uuid, data):
        """Update bird using UUID"""
        bird = Pajaro.query.get(bird_uuid)
        if not bird:
            return None
        
        try:
            genetics_data = data.pop('genetica', None)
            
            # Clean and convert data types (same as create_bird)
            for key in list(data.keys()):
                if data[key] == '':
                    data[key] = None
            
            # Convert fecha_nacimiento
            if data.get('fecha_nacimiento') and isinstance(data['fecha_nacimiento'], str):
                from datetime import datetime as dt
                try:
                    data['fecha_nacimiento'] = dt.strptime(data['fecha_nacimiento'], '%Y-%m-%d').date()
                except ValueError:
                    data['fecha_nacimiento'] = None
            
            # Update main bird record
            for key, value in data.items():
                if hasattr(bird, key) and key != 'uuid':
                    setattr(bird, key, value)
            
            bird.updated_at = datetime.utcnow().isoformat()
            
            # Update genetics if provided
            if genetics_data is not None:
                PajaroGenetica.query.filter_by(bird_uuid=bird.uuid).delete()
                for gen in genetics_data:
                    genetica = PajaroGenetica(
                        uuid=str(uuid_lib.uuid4()),
                        bird_uuid=bird.uuid,
                        mutacion_uuid=gen.get('mutacion_uuid'),
                        expresion=gen.get('expresion', 'Visual'),
                        genotipo=gen.get('genotipo', '')
                    )
                    db.session.add(genetica)
            
            db.session.commit()
            return bird
        except SQLAlchemyError as e:
            db.session.rollback()
            raise e

    @staticmethod
    def delete_bird(bird_uuid):
        """Soft delete bird using UUID"""
        bird = Pajaro.query.get(bird_uuid)
        if not bird:
            return False
            
        try:
            bird.deleted_at = datetime.utcnow().isoformat()
            db.session.commit()
            return True
        except SQLAlchemyError as e:
            db.session.rollback()
            raise e

    @staticmethod
    def add_bird_event(bird_id, event_data):
        """Add an event to bird history"""
        try:
            evento = PajaroEvento(
                id_ave=bird_id,
                tipo_evento=event_data.get('tipo_evento'),
                fecha=event_data.get('fecha') or datetime.utcnow(),
                id_contacto=event_data.get('id_contacto'),
                precio=event_data.get('precio', 0.0),
                detalles=event_data.get('detalles', '')
            )
            db.session.add(evento)
            db.session.commit()
            return evento
        except SQLAlchemyError as e:
            db.session.rollback()
            raise e

    @staticmethod
    def get_bird_history(bird_id):
        """Get all events for a bird"""
        eventos = PajaroEvento.query.filter_by(id_ave=bird_id).order_by(PajaroEvento.fecha.desc()).all()
        return [e.to_dict() for e in eventos]
