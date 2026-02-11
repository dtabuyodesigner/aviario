from app.extensions import db
from datetime import datetime
import uuid

class BaseModel(db.Model):
    __abstract__ = True

    def to_dict(self):
        """Converts model instance to dictionary."""
        return {
            c.name: getattr(self, c.name) for c in self.__table__.columns
        }

class TimestampMixin:
    created_at = db.Column(db.String, default=lambda: datetime.now().isoformat())
    updated_at = db.Column(db.String, default=lambda: datetime.now().isoformat(), onupdate=lambda: datetime.now().isoformat())

class SoftDeleteMixin:
    deleted_at = db.Column(db.String, nullable=True)

    def delete(self):
        self.deleted_at = datetime.now().isoformat()
        db.session.add(self)
