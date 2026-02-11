from app.extensions import db
from app.models.bird import Pajaro
from app.models.genetics import Especie
from sqlalchemy.exc import SQLAlchemyError
import uuid

class BirdService:
    @staticmethod
    def get_all_birds(filters=None):
        query = Pajaro.query
        if filters:
            if 'especie_id' in filters:
                query = query.filter_by(id_especie=filters['especie_id'])
            if 'estado' in filters:
                query = query.filter_by(estado=filters['estado'])
            # Add more filters as needed
        return query.all()

    @staticmethod
    def get_bird_by_id(bird_id):
        return Pajaro.query.get(bird_id)

    @staticmethod
    def create_bird(data):
        try:
            # Handle Species resolution if needed (by name or ID)
            # For now assume 'id_especie' is passed or we verify it
            
            # Generate UUID if not present
            if 'uuid' not in data:
                data['uuid'] = str(uuid.uuid4())
            
            new_bird = Pajaro(**data)
            db.session.add(new_bird)
            db.session.commit()
            return new_bird
        except SQLAlchemyError as e:
            db.session.rollback()
            raise e

    @staticmethod
    def update_bird(bird_id, data):
        bird = Pajaro.query.get(bird_id)
        if not bird:
            return None
        
        try:
            for key, value in data.items():
                if hasattr(bird, key):
                    setattr(bird, key, value)
            
            db.session.commit()
            return bird
        except SQLAlchemyError as e:
            db.session.rollback()
            raise e

    @staticmethod
    def delete_bird(bird_id):
        bird = Pajaro.query.get(bird_id)
        if not bird:
            return False
            
        try:
            bird.delete() # Uses SoftDeleteMixin
            db.session.commit()
            return True
        except SQLAlchemyError as e:
            db.session.rollback()
            raise e
