from app.models.health import Tratamiento, Receta
from app.extensions import db
from datetime import date

class HealthService:
    # TREATMENTS
    @staticmethod
    def get_treatments(active_only=False):
        query = Tratamiento.query
        if active_only:
             query = query.filter_by(estado='Activo')
        return query.order_by(Tratamiento.fecha_inicio.desc()).all()

    @staticmethod
    def get_treatment_by_id(t_id):
        return Tratamiento.query.get(t_id)

    @staticmethod
    def create_treatment(data):
        t = Tratamiento(
            id_ave=data.get('id_ave'),
            id_receta=data.get('id_receta'),
            tipo=data.get('tipo'),
            fecha_inicio=data.get('fecha_inicio') or date.today(),
            fecha_fin=data.get('fecha_fin'),
            sintomas=data.get('sintomas'),
            diagnostico=data.get('diagnostico'),
            observaciones=data.get('observaciones'),
            estado=data.get('estado', 'Activo'),
            resultado=data.get('resultado')
        )
        db.session.add(t)
        db.session.commit()
        return t

    @staticmethod
    def update_treatment(t_id, data):
        t = Tratamiento.query.get(t_id)
        if not t:
            return None
            
        allowed = ['id_receta', 'tipo', 'fecha_inicio', 'fecha_fin', 'sintomas', 'diagnostico', 'observaciones', 'estado', 'resultado']
        for key in allowed:
            if key in data:
                setattr(t, key, data[key])
                
        db.session.commit()
        return t

    @staticmethod
    def delete_treatment(t_id):
        t = Tratamiento.query.get(t_id)
        if not t:
            return False
        db.session.delete(t)
        db.session.commit()
        return True

    # RECIPES
    @staticmethod
    def get_all_recipes():
        return Receta.query.order_by(Receta.nombre_receta).all()

    @staticmethod
    def create_recipe(data):
        r = Receta(
            nombre_receta=data.get('nombre_receta'),
            indicaciones=data.get('indicaciones'),
            dosis=data.get('dosis'),
            ingredientes=data.get('ingredientes')
        )
        db.session.add(r)
        db.session.commit()
        return r

    @staticmethod
    def update_recipe(r_id, data):
        r = Receta.query.get(r_id)
        if not r:
            return None
            
        for key in ['nombre_receta', 'indicaciones', 'dosis', 'ingredientes']:
             if key in data:
                 setattr(r, key, data[key])
                 
        db.session.commit()
        return r

    @staticmethod
    def delete_recipe(r_id):
        r = Receta.query.get(r_id)
        if not r:
            return False
        db.session.delete(r)
        db.session.commit()
        return True
