import sqlalchemy
import uuid

from src.core.database.base import base as Base


from src.core.database.models.modules import Modules
from src.core.database.models.resources import Resources
from src.core.database.models.user_actions import UserActions
from src.core.database.models.user_roles import UserRoles

class ViewsControlAccess(Base):
    __tablename__ = 'views_control_access'

    id = sqlalchemy.Column(sqlalchemy.dialects.postgresql.UUID(as_uuid=True), primary_key=True, default=uuid.uuid4, unique=True, nullable=False)

    module_id = sqlalchemy.Column(sqlalchemy.dialects.postgresql.UUID(as_uuid=True), sqlalchemy.ForeignKey(Modules.id), nullable=True)
    user_role_id = sqlalchemy.Column(sqlalchemy.dialects.postgresql.UUID(as_uuid=True), sqlalchemy.ForeignKey(UserRoles.id), nullable=True)
    resource_id = sqlalchemy.Column(sqlalchemy.dialects.postgresql.UUID(as_uuid=True), sqlalchemy.ForeignKey(Resources.id), nullable=True)
    action_id = sqlalchemy.Column(sqlalchemy.dialects.postgresql.UUID(as_uuid=True), sqlalchemy.ForeignKey(UserActions.id), nullable=True)

    module_relation = sqlalchemy.orm.relationship('Modules', backref='module_view', uselist=False, foreign_keys=[module_id])
    user_role_relation = sqlalchemy.orm.relationship('UserRoles', backref='user_role_view', uselist=False, foreign_keys=[user_role_id])
    resource_relation = sqlalchemy.orm.relationship('Resources', backref='resource_view', uselist=False, foreign_keys=[resource_id])
    action_relation = sqlalchemy.orm.relationship('UserActions', backref='user_action_view', uselist=False, foreign_keys=[action_id])
