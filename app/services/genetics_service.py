from app.models.genetics import Especie, Variedad, Mutacion

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
    def get_all_mutations():
         return Mutacion.query.all()
