import sqlalchemy
import uuid

from src.core.database.base import base as Base


class UserRoles(Base):
    __tablename__ = 'user_roles'

    id = sqlalchemy.Column(sqlalchemy.dialects.postgresql.UUID(as_uuid=True), primary_key=True, default=uuid.uuid4, unique=True, nullable=False)
    name = sqlalchemy.Column(sqlalchemy.String, unique=True, nullable=False)
