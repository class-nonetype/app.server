import sqlalchemy
import uuid
from src.core.utils import get_datetime
from src.core.database.base import base as Base

from src.core.database.models.user_accounts import UserAccounts
from src.core.database.models.uploads import Uploads
from src.core.database.models.comments import Comments


class UserPosts(Base):
    __tablename__ = 'user_posts'

    id = sqlalchemy.Column(sqlalchemy.dialects.postgresql.UUID(as_uuid=True), primary_key=True, default=uuid.uuid4, unique=True, nullable=False)

    user_id = sqlalchemy.Column(sqlalchemy.dialects.postgresql.UUID(as_uuid=True), sqlalchemy.ForeignKey(UserAccounts.id), nullable=False)
    upload_id = sqlalchemy.Column(sqlalchemy.dialects.postgresql.UUID(as_uuid=True), sqlalchemy.ForeignKey(Uploads.id), nullable=False)
    comment_id = sqlalchemy.Column(sqlalchemy.dialects.postgresql.UUID(as_uuid=True), sqlalchemy.ForeignKey(Comments.id), nullable=False)

    title = sqlalchemy.Column(sqlalchemy.Text, nullable=True)
    description = sqlalchemy.Column(sqlalchemy.Text, nullable=True)

    
    active = sqlalchemy.Column(sqlalchemy.Boolean, default=True, nullable=False)

    created_at = sqlalchemy.Column(sqlalchemy.DateTime, default=get_datetime())
    updated_at = sqlalchemy.Column(sqlalchemy.DateTime, nullable=True, default=get_datetime())

    user_account_relation = sqlalchemy.orm.relationship('UserAccounts', backref='user_account', uselist=False, foreign_keys=[user_id])
    user_upload_relation = sqlalchemy.orm.relationship('Uploads', backref='user_upload', uselist=False, foreign_keys=[upload_id])
    user_comment_relation = sqlalchemy.orm.relationship('Comments', backref='user_comment', uselist=False, foreign_keys=[comment_id])
