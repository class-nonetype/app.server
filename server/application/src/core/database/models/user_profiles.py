import sqlalchemy
import uuid

from src.core.utils import get_datetime
from src.core.database.base import base as Base



# models/user_profile.py
class UserProfiles(Base):
    __tablename__ = 'user_profiles'

    id = sqlalchemy.Column(sqlalchemy.dialects.postgresql.UUID(as_uuid=True), primary_key=True, default=uuid.uuid4, unique=True, nullable=False)
    full_name = sqlalchemy.Column(sqlalchemy.String, nullable=True)
    e_mail = sqlalchemy.Column(sqlalchemy.String, nullable=False)
    created_at = sqlalchemy.Column(sqlalchemy.DateTime, default=get_datetime())
    updated_at = sqlalchemy.Column(sqlalchemy.DateTime, nullable=True, default=get_datetime())
