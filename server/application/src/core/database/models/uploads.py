import sqlalchemy
import uuid
from src.core.utils import get_datetime
from src.core.database.base import base as Base

from src.core.database.models.user_accounts import UserAccounts


class Uploads(Base):
    __tablename__ = 'uploads'

    id = sqlalchemy.Column(sqlalchemy.dialects.postgresql.UUID(as_uuid=True), primary_key=True, default=uuid.uuid4, unique=True, nullable=False)

    user_id = sqlalchemy.Column(sqlalchemy.dialects.postgresql.UUID(as_uuid=True), sqlalchemy.ForeignKey(UserAccounts.id), nullable=False)

    
    file_path = sqlalchemy.Column(sqlalchemy.Text, nullable=True)
    file_url = sqlalchemy.Column(sqlalchemy.Text, nullable=True)
    file_size = sqlalchemy.Column(sqlalchemy.String, nullable=True)
    file_name = sqlalchemy.Column(sqlalchemy.String, nullable=True)
    file_uuid_name = sqlalchemy.Column(sqlalchemy.String, nullable=True)
    
    active = sqlalchemy.Column(sqlalchemy.Boolean, default=True, nullable=False)

    created_at = sqlalchemy.Column(sqlalchemy.DateTime, default=get_datetime())
    updated_at = sqlalchemy.Column(sqlalchemy.DateTime, nullable=True, default=get_datetime())

    user_account_relation = sqlalchemy.orm.relationship('UserAccounts', backref='user_media', uselist=False, foreign_keys=[user_id])
