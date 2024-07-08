import sqlalchemy.orm
import uuid

from src.core.utils import get_datetime
from src.core.log import log

from src.core.database.models.user_actions import UserActions
from src.core.database.models.user_accounts import UserAccounts
from src.core.database.models.user_roles import UserRoles
from src.core.database.models.user_profiles import UserProfiles

from src.core.schemas.user import CreateUser


def select_action_description_by_action_id(session: sqlalchemy.orm.Session, action_id: uuid.UUID):
    try:
        action = session.query(UserActions.name).filter(UserActions.id==action_id).first()
        return action[0]

    except IndexError:
        pass

    except Exception as exception:
        log.exception(msg=exception)

def select_user_full_name_by_id(session: sqlalchemy.orm.Session, account_id: uuid.UUID) -> str:
    user = session.query(UserProfiles).join(UserAccounts, UserProfiles.id == UserAccounts.profile_id).filter(UserAccounts.id == account_id).first()
    return user.full_name if user else None


def select_action_name_by_action_id(session: sqlalchemy.orm.Session, action_id: uuid.UUID):
    return session.query(UserActions.name).filter(UserActions.id == action_id).first()


def select_user_role_name_by_user_role_id(session: sqlalchemy.orm.Session, role_id: uuid.UUID) -> str:
    user_role = session.query(UserRoles.name).filter(UserRoles.id == role_id).first()
    return user_role[0] if user_role else None



def select_user_by_username(session: sqlalchemy.orm.Session, username: str):
    return session.query(UserAccounts).filter(UserAccounts.username==username).first()


def select_user_by_id(session: sqlalchemy.orm.Session, id: uuid.UUID) -> UserAccounts:
    return session.query(UserAccounts).filter(UserAccounts.id==id).first()


def validate_user_authentication(session: sqlalchemy.orm.Session, username: str, password: str):
    q = select_user_by_username(session, username)

    if not q:
        return False
    
    if not q.verify_password(password):
        return False

    if not q.active:
        return False

    return q



def update_last_login_date(session: sqlalchemy.orm.Session, user_id: uuid.UUID) -> None:
    session.query(UserAccounts).filter(UserAccounts.id == user_id).\
        update(
            {'last_login_date': get_datetime()}
        )

    return session.commit()