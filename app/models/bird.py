from app.extensions import db
from app.models.base import BaseModel, TimestampMixin, SoftDeleteMixin
from app.models.core import Contacto, Ubicacion
from datetime import datetime

class Pajaro(BaseModel, TimestampMixin, SoftDeleteMixin):
    __tablename__ = 'pajaros'

    id_ave = db.Column(db.Integer, primary_key=True, autoincrement=True)
    anilla = db.Column(db.String, unique=True, nullable=False)
    id_especie = db.Column(db.Integer, db.ForeignKey('especies.id_especie'))
    mutacion_visual = db.Column(db.String)
    portador_de = db.Column(db.String)
    id_raza = db.Column(db.String) # Text field in legacy
    sexo = db.Column(db.String)
    fecha_nacimiento = db.Column(db.Date)
    anio_nacimiento = db.Column(db.Integer)
    origen = db.Column(db.String)
    
    # Genealogía
    id_padre = db.Column(db.Integer, db.ForeignKey('pajaros.id_ave'))
    id_madre = db.Column(db.Integer, db.ForeignKey('pajaros.id_ave'))
    id_criador_externo = db.Column(db.Integer, db.ForeignKey('contactos.id_contacto'))
    
    # Estado y Ubicación
    estado = db.Column(db.String, default='Activo')
    id_ubicacion = db.Column(db.Integer, db.ForeignKey('ubicaciones.id_ubicacion'))
    disponible_venta = db.Column(db.Boolean, default=False)
    reservado = db.Column(db.Boolean, default=False)

    # Campos Nuevos v2
    uuid = db.Column(db.String)
    owner_id = db.Column(db.String)
    observaciones = db.Column(db.String)
    
    # Relationships
    especie = db.relationship('Especie', backref='pajaros')
    padre = db.relationship('Pajaro', remote_side=[id_ave], foreign_keys=[id_padre], backref='hijos_padre')
    madre = db.relationship('Pajaro', remote_side=[id_ave], foreign_keys=[id_madre], backref='hijos_madre')
    criador = db.relationship('Contacto', foreign_keys=[id_criador_externo])
    ubicacion = db.relationship('Ubicacion')
    
    gallery = db.relationship('BirdPhoto', backref='bird', cascade="all, delete-orphan")
    movimientos = db.relationship('Movimiento', backref='bird', lazy=True)


class BirdPhoto(BaseModel, TimestampMixin, SoftDeleteMixin):
    __tablename__ = 'bird_photos' # Assuming this table name from schema/app.py logic
    # Note: schema.sql didn't explicitly show bird_photos creation in the snippet I saw, 
    # but app.py uses it. I should double check if I missed it in schema view or if it's there.
    # Ah, app.py uses it. Let's assume it exists or I might have missed it in schema.sql view.
    # Re-checking app.py: "INSERT INTO bird_photos (id_bird, file_path)..."
    # Re-checking schema.sql: It WAS NOT in the snippet I viewed.
    # It might be in a migration or I missed scrolling.
    # Update: I see `bird_mutations` in schema.sql.
    # I will define it based on app.py usage.
    
    id_photo = db.Column(db.Integer, primary_key=True, autoincrement=True)
    id_bird = db.Column(db.Integer, db.ForeignKey('pajaros.id_ave'))
    file_path = db.Column(db.String)

class Movimiento(BaseModel):
    __tablename__ = 'movimientos'

    id_movimiento = db.Column(db.Integer, primary_key=True, autoincrement=True)
    id_ave = db.Column(db.Integer, db.ForeignKey('pajaros.id_ave'), nullable=False)
    tipo_evento = db.Column(db.String, nullable=False)
    fecha = db.Column(db.Date, default=datetime.utcnow)
    id_contacto = db.Column(db.Integer, db.ForeignKey('contactos.id_contacto'))
    precio = db.Column(db.Float, default=0.0)
    gastos_asociados = db.Column(db.Float, default=0.0)
    detalles = db.Column(db.String)
    
    contacto = db.relationship('Contacto')
