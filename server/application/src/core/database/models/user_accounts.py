import sqlalchemy
import uuid

from src.core.utils import get_datetime
from src.core.database.base import base as Base



import sqlalchemy.orm
import bcrypt

from src.core.database.models.user_roles import UserRoles
from src.core.database.models.user_profiles import UserProfiles




class UserAccounts(Base):
    __tablename__ = 'user_accounts'

    id = sqlalchemy.Column(sqlalchemy.dialects.postgresql.UUID(as_uuid=True), primary_key=True, default=uuid.uuid4, unique=True, nullable=False)
    role_id = sqlalchemy.Column(sqlalchemy.dialects.postgresql.UUID(as_uuid=True), sqlalchemy.ForeignKey(UserRoles.id), nullable=False)
    profile_id = sqlalchemy.Column(sqlalchemy.dialects.postgresql.UUID(as_uuid=True), sqlalchemy.ForeignKey(UserProfiles.id), unique=True, nullable=False)

    username = sqlalchemy.Column(sqlalchemy.String, nullable=False)
    password = sqlalchemy.Column(sqlalchemy.String, nullable=False)

    created_at = sqlalchemy.Column(sqlalchemy.DateTime, default=get_datetime())
    updated_at = sqlalchemy.Column(sqlalchemy.DateTime, nullable=True, default=get_datetime())
    last_login_date = sqlalchemy.Column(sqlalchemy.DateTime, nullable=True)

    user_role_relation = sqlalchemy.orm.relationship('UserRoles', backref='role_relation', uselist=False)
    user_profile_relation = sqlalchemy.orm.relationship('UserProfiles', backref='profile_relation', uselist=False)

    active = sqlalchemy.Column(sqlalchemy.Boolean, default=True, nullable=False)

    
    def verify_password(self, password: str) -> bool:
        return bcrypt.checkpw(
            password=password.encode('utf-8'),
            hashed_password=self.password.encode('utf-8')
        )
    

    def get_id(self) -> str:
        return str(self.id)

    def get_username(self) -> str:
        return self.username
