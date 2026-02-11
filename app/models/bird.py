from app.extensions import db
from app.models.base import BaseModel, TimestampMixin, SoftDeleteMixin
from app.models.core import Contacto, Ubicacion
from datetime import datetime

class Pajaro(BaseModel, TimestampMixin, SoftDeleteMixin):
    __tablename__ = 'pajaros'

    uuid = db.Column(db.String, primary_key=True)
    anilla = db.Column(db.String, unique=True, nullable=False)
    
    # Species and Variety (UUID-based for new system)
    variety_uuid = db.Column(db.String, db.ForeignKey('variedades.uuid'))
    
    # Basic info
    sexo = db.Column(db.String) # 'M', 'H', '?'
    fecha_nacimiento = db.Column(db.Date)
    
    # Genealogía (UUID-based)
    padre_uuid = db.Column(db.String)
    madre_uuid = db.Column(db.String)
    nidada_uuid = db.Column(db.String)
    
    # Estado and Metadata
    estado = db.Column(db.String, default='Activo')
    owner_id = db.Column(db.String)
    sync_version = db.Column(db.Integer, default=1)
    observaciones = db.Column(db.String)
    
    # Sales flags (kept in main table for query performance)
    disponible_venta = db.Column(db.Boolean, default=False)
    reservado = db.Column(db.Boolean, default=False)

    foto_path = db.Column(db.String)

    # Relationships
    variedad = db.relationship('Variedad', backref='pajaros')
    
    # NEW: Relationships to separate tables
    genetica = db.relationship('PajaroGenetica', backref='pajaro', lazy='dynamic', cascade='all, delete-orphan')
    estados = db.relationship('PajaroEstado', backref='pajaro', lazy='dynamic', cascade='all, delete-orphan', order_by='PajaroEstado.fecha_estado.desc()')
    eventos = db.relationship('PajaroEvento', backref='pajaro', lazy='dynamic', cascade='all, delete-orphan')
    
    gallery = db.relationship('BirdPhoto', backref='bird', cascade="all, delete-orphan")
    
    @property
    def estado_actual(self):
        """Get the most recent state"""
        return self.estados.first()
    
    def to_dict(self):
        """Enhanced to_dict with joined data"""
        d = super().to_dict()
        
        # Add species and variety names
        if self.variedad:
            d['variedad'] = self.variedad.nombre
            if self.variedad.especie:
                d['especie'] = self.variedad.especie.nombre_comun
        
        # Add current state if exists
        estado = self.estado_actual
        if estado:
            d['estado'] = estado.estado
            d['ubicacion'] = estado.ubicacion
            
        return d


class PajaroGenetica(BaseModel):
    """Genetics storage - mutations and expressions for a bird"""
    __tablename__ = 'pajaros_genetica'
    
    uuid = db.Column(db.String, primary_key=True)
    bird_uuid = db.Column(db.String, db.ForeignKey('pajaros.uuid'), nullable=False, index=True)
    mutacion_uuid = db.Column(db.String, db.ForeignKey('mutaciones.uuid'), nullable=False)
    expresion = db.Column(db.String)  # 'Visual', 'Portador', 'Posible'
    genotipo = db.Column(db.String)   # Detailed genotype string
    
    # Relationship to mutation
    mutacion = db.relationship('Mutacion')
    
    def to_dict(self):
        d = {
            'uuid': self.uuid,
            'bird_uuid': self.bird_uuid,
            'mutacion_uuid': self.mutacion_uuid,
            'expresion': self.expresion,
            'genotipo': self.genotipo
        }
        if self.mutacion:
            d['mutacion_nombre'] = self.mutacion.nombre
        return d


class PajaroEstado(BaseModel):
    """State history for a bird - tracks status changes over time"""
    __tablename__ = 'pajaros_estado'
    
    uuid = db.Column(db.String, primary_key=True)
    bird_uuid = db.Column(db.String, db.ForeignKey('pajaros.uuid'), nullable=False, index=True)
    estado = db.Column(db.String)  # 'Activo', 'Vendido', 'Cedido', 'Baja', etc.
    ubicacion = db.Column(db.String)
    observaciones = db.Column(db.String)
    fecha_estado = db.Column(db.String, default=lambda: datetime.utcnow().isoformat())
    
    def to_dict(self):
        return {
            'uuid': self.uuid,
            'bird_uuid': self.bird_uuid,
            'estado': self.estado,
            'ubicacion': self.ubicacion,
            'observaciones': self.observaciones,
            'fecha_estado': self.fecha_estado
        }


class PajaroEvento(BaseModel):
    """Events for a bird - sales, transfers, deaths, etc."""
    __tablename__ = 'movimientos'
    
    id_movimiento = db.Column(db.Integer, primary_key=True, autoincrement=True)
    bird_uuid = db.Column(db.String, db.ForeignKey('pajaros.uuid'), nullable=False)
    
    # TODO: Add bird_uuid column for full UUID migration
    # bird_uuid = db.Column(db.String, db.ForeignKey('pajaros.uuid'))
    
    tipo_evento = db.Column(db.String, nullable=False)
    fecha = db.Column(db.Date, default=datetime.utcnow)
    id_contacto = db.Column(db.Integer, db.ForeignKey('contactos.id_contacto'))
    precio = db.Column(db.Float, default=0.0)
    gastos_asociados = db.Column(db.Float, default=0.0)
    detalles = db.Column(db.String)
    
    contacto = db.relationship('Contacto')
    
    def to_dict(self):
        d = {
            'id_movimiento': self.id_movimiento,
            'bird_uuid': self.bird_uuid,
            'tipo_evento': self.tipo_evento,
            'fecha': self.fecha.isoformat() if self.fecha else None,
            'precio': self.precio,
            'detalles': self.detalles
        }
        if self.contacto:
            d['contacto_nombre'] = self.contacto.nombre_razon_social
        return d


class BirdPhoto(BaseModel, TimestampMixin, SoftDeleteMixin):
    __tablename__ = 'bird_photos'
    
    id_photo = db.Column(db.Integer, primary_key=True, autoincrement=True)
    bird_uuid = db.Column(db.String, db.ForeignKey('pajaros.uuid'))
    file_path = db.Column(db.String)
