from app.extensions import db
from app.models.base import BaseModel

class Contacto(BaseModel):
    __tablename__ = 'contactos'

    id_contacto = db.Column(db.Integer, primary_key=True, autoincrement=True)
    tipo = db.Column(db.String)
    nombre_razon_social = db.Column(db.String, nullable=False)
    dni_cif = db.Column(db.String)
    n_criador = db.Column(db.String)
    telefono = db.Column(db.String)
    email = db.Column(db.String)
    direccion = db.Column(db.String)
    observaciones = db.Column(db.String)

class Ubicacion(BaseModel):
    __tablename__ = 'ubicaciones'

    id_ubicacion = db.Column(db.Integer, primary_key=True, autoincrement=True)
    codigo = db.Column(db.String, unique=True, nullable=False)
    tipo = db.Column(db.String)
    capacidad_maxima = db.Column(db.Integer)
