import sqlalchemy
import uuid

from src.core.database.base import base as Base

from src.core.database.models.modules import Modules

class Resources(Base):
    __tablename__ = 'resources'

    id = sqlalchemy.Column(sqlalchemy.dialects.postgresql.UUID(as_uuid=True), primary_key=True, default=uuid.uuid4, unique=True, nullable=False)
    module_id = sqlalchemy.Column(sqlalchemy.dialects.postgresql.UUID(as_uuid=True), sqlalchemy.ForeignKey(Modules.id), nullable=False)

    name = sqlalchemy.Column(sqlalchemy.String, nullable=True)

    active = sqlalchemy.Column(sqlalchemy.Boolean, default=True, nullable=False)
    
    module_relation = sqlalchemy.orm.relationship('Modules', backref='module_resource', uselist=False, foreign_keys=[module_id])
