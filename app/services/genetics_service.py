from app.models.genetics import Especie, Variedad, Mutacion
from app.extensions import db

class GeneticsService:
    @staticmethod
    def get_all_species():
        return Especie.query.all()

    @staticmethod
    def get_varieties_by_species(species_uuid):
        return Variedad.query.filter_by(especie_uuid=species_uuid).all()

    @staticmethod
    def get_mutations_by_variety(variety_uuid):
        # Using the relationship defined in Variedad model
        variety = Variedad.query.get(variety_uuid)
        if variety:
            return variety.mutaciones
        return []
        
    @staticmethod
    def get_mutations_filtered(species_name=None, variety_uuid=None):
        query = Mutacion.query
        
        if variety_uuid:
            # Join via VariedadMutacion
            # Assuming VariedadMutacion model is available or using the relationship
            from app.models.genetics import VariedadMutacion
            query = query.join(VariedadMutacion, Mutacion.uuid == VariedadMutacion.mutacion_uuid)\
                         .filter(VariedadMutacion.variedad_uuid == variety_uuid)
        elif species_name:
             from app.models.genetics import VariedadMutacion, Variedad, Especie
             query = query.join(VariedadMutacion, Mutacion.uuid == VariedadMutacion.mutacion_uuid)\
                          .join(Variedad, VariedadMutacion.variedad_uuid == Variedad.uuid)\
                          .join(Especie, Variedad.especie_uuid == Especie.uuid)\
                          .filter(db.func.lower(Especie.nombre_comun) == species_name.lower())

        return query.all()

    @staticmethod
    def get_all_mutations():
         return Mutacion.query.all()
