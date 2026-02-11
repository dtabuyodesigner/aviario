from app.extensions import db
from app.models.base import BaseModel, TimestampMixin, SoftDeleteMixin

class Receta(BaseModel, TimestampMixin, SoftDeleteMixin):
    __tablename__ = 'recetas'
    
    id_receta = db.Column(db.Integer, primary_key=True, autoincrement=True)
    nombre_receta = db.Column(db.String, nullable=False)
    indicaciones = db.Column(db.String)
    dosis = db.Column(db.String)
    ingredientes = db.Column(db.String)
    
    def to_dict(self):
        d = super().to_dict()
        return d

class Tratamiento(BaseModel, TimestampMixin, SoftDeleteMixin):
    __tablename__ = 'tratamientos'
    
    id_tratamiento = db.Column(db.Integer, primary_key=True, autoincrement=True)
    bird_uuid = db.Column(db.String, db.ForeignKey('pajaros.uuid'), nullable=False)
    id_receta = db.Column(db.Integer, db.ForeignKey('recetas.id_receta'), nullable=True)
    tipo = db.Column(db.String) # Curativo, Preventivo, etc.
    fecha_inicio = db.Column(db.Date)
    fecha_fin = db.Column(db.Date)
    sintomas = db.Column(db.String)
    diagnostico = db.Column(db.String)
    observaciones = db.Column(db.String)
    estado = db.Column(db.String, default='Activo')
    resultado = db.Column(db.String)
    
    # Relationships
    ave = db.relationship('Pajaro', backref='tratamientos')
    receta = db.relationship('Receta', backref='tratamientos')

    def to_dict(self):
        d = super().to_dict()
        if self.ave:
            d['anilla'] = self.ave.anilla
        if self.receta:
            d['nombre_receta'] = self.receta.nombre_receta
        return d
