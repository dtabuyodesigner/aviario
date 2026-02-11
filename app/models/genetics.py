from app.extensions import db
from app.models.base import BaseModel, TimestampMixin, SoftDeleteMixin

class Especie(BaseModel, TimestampMixin):
    __tablename__ = 'especies'

    id_especie = db.Column(db.Integer, primary_key=True, autoincrement=True)
    nombre_comun = db.Column(db.String, unique=True, nullable=False)
    nombre_cientifico = db.Column(db.String)
    dias_incubacion = db.Column(db.Integer, default=21)
    dias_anillado = db.Column(db.Integer, default=8)
    grupo_genetico = db.Column(db.String)
    categoria = db.Column(db.String)
    continente = db.Column(db.String)
    uuid = db.Column(db.String) # Not PK in legacy, but important
    dimorfismo_sexual = db.Column(db.String)
    tamano_puesta = db.Column(db.String)
    notas = db.Column(db.String)
    tiene_mutaciones = db.Column(db.Boolean, default=False)
    es_propio = db.Column(db.Boolean, default=False)

    # Relationships
    variedades = db.relationship('Variedad', 
                                 primaryjoin='Especie.uuid==foreign(Variedad.especie_uuid)',
                                 backref='especie', 
                                 lazy=True)


class Variedad(BaseModel, TimestampMixin, SoftDeleteMixin):
    __tablename__ = 'variedades'

    uuid = db.Column(db.String, primary_key=True)
    especie_uuid = db.Column(db.String, nullable=False) # Foreign Key logic handling manually for now or via property if strict FK not exists
    nombre = db.Column(db.String, nullable=False)
    
    # Relationships
    # Note: species relationship is a bit complex due to mixed IDs (int vs uuid). 
    # logic should rely on species.uuid matching variedad.especie_uuid

    mutaciones = db.relationship('Mutacion', secondary='variedad_mutaciones', backref='variedades')


class Mutacion(BaseModel, TimestampMixin, SoftDeleteMixin):
    __tablename__ = 'mutaciones'

    uuid = db.Column(db.String, primary_key=True)
    nombre = db.Column(db.String, nullable=False)
    tipo_herencia = db.Column(db.String)
    locus = db.Column(db.String)
    dominante = db.Column(db.Integer)

class VariedadMutacion(BaseModel, TimestampMixin, SoftDeleteMixin):
    __tablename__ = 'variedad_mutaciones'

    uuid = db.Column(db.String, primary_key=True)
    variedad_uuid = db.Column(db.String, db.ForeignKey('variedades.uuid'), nullable=False)
    mutacion_uuid = db.Column(db.String, db.ForeignKey('mutaciones.uuid'), nullable=False)

class CanaryBreed(BaseModel, TimestampMixin, SoftDeleteMixin):
    __tablename__ = 'canary_breeds'
    
    id_breed = db.Column(db.Integer, primary_key=True, autoincrement=True)
    nombre = db.Column(db.String, nullable=False)
    tipo = db.Column(db.String)
    variedad_uuid = db.Column(db.String) # Linking loosely to variedad uuid
