from app.extensions import db
from app.models.base import BaseModel, TimestampMixin, SoftDeleteMixin

class Cruce(BaseModel, TimestampMixin, SoftDeleteMixin):
    __tablename__ = 'cruces'
    
    id_cruce = db.Column(db.Integer, primary_key=True, autoincrement=True)
    id_macho = db.Column(db.String, db.ForeignKey('pajaros.uuid'))
    id_hembra = db.Column(db.String, db.ForeignKey('pajaros.uuid'))
    fecha_union = db.Column(db.Date)
    fecha_separacion = db.Column(db.Date)
    variedad_objetivo = db.Column(db.String)
    id_ubicacion = db.Column(db.String) # Should be FK? Legacy uses string/int loose link sometimes.
    estado = db.Column(db.String, default='Juntos')
    
    # Relationships
    macho = db.relationship('Pajaro', foreign_keys=[id_macho], backref='cruces_como_macho')
    hembra = db.relationship('Pajaro', foreign_keys=[id_hembra], backref='cruces_como_hembra')
    nidadas = db.relationship('Nidada', backref='cruce', lazy=True, cascade='all, delete-orphan')
    
    def to_dict(self):
        d = super().to_dict()
        if self.macho:
            d['macho_anilla'] = self.macho.anilla
            d['macho_mutacion'] = self.macho.mutacion_visual
            d['macho_foto'] = self.macho.foto_path
        if self.hembra:
            d['hembra_anilla'] = self.hembra.anilla
            d['hembra_mutacion'] = self.hembra.mutacion_visual
            d['hembra_foto'] = self.hembra.foto_path
        return d


class Nidada(BaseModel, TimestampMixin, SoftDeleteMixin):
    __tablename__ = 'nidadas'
    
    id_nidada = db.Column(db.Integer, primary_key=True, autoincrement=True)
    id_cruce = db.Column(db.Integer, db.ForeignKey('cruces.id_cruce'), nullable=False)
    numero_nidada = db.Column(db.Integer, nullable=False)
    estado = db.Column(db.String, default='Puesta')
    huevos_totales = db.Column(db.Integer, default=0)
    huevos_fertiles = db.Column(db.Integer, default=0)
    pollos_nacidos = db.Column(db.Integer, default=0)
    pollos_anillados = db.Column(db.Integer, default=0)
    fecha_primer_huevo = db.Column(db.Date)
    fecha_nacimiento = db.Column(db.Date)
    fecha_inicio_incubacion = db.Column(db.Date)
    
class ConfigIncubacion(BaseModel, TimestampMixin, SoftDeleteMixin):
    __tablename__ = 'config_incubacion'
    
    id_config = db.Column(db.Integer, primary_key=True, autoincrement=True)
    especie = db.Column(db.String, nullable=False)
    dias_incubacion = db.Column(db.String) # e.g. "13" or "13-15"
    temperatura_incubacion = db.Column(db.Float)
    humedad_incubacion = db.Column(db.Float)
