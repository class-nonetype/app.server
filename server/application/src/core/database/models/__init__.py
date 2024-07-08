from src.core.log import log

from src.core.database.base import base as Base
from src.core.database.engine import engine as Engine
from src.core.database.session import session as Session

from src.core.database.models.user_roles import UserRoles
from src.core.database.models.user_profiles import UserProfiles
from src.core.database.models.user_accounts import UserAccounts
from src.core.database.models.comments import Comments
from src.core.database.models.uploads import Uploads
from src.core.database.models.modules import Modules
from src.core.database.models.user_actions import UserActions
from src.core.database.models.resources import Resources
from src.core.database.models.views_control_access import ViewsControlAccess



from sqlalchemy import inspect
from sqlalchemy.orm import clear_mappers


try:
    Base.metadata.create_all(bind=Engine)
    # database.Base.metadata.drop_all(bind=database.engine)
except Exception as exception:
    log.exception(msg=exception)



try:
    models = {}
    session = Session()
    inspector = inspect(Engine)
    
    log.info(msg='%s\t<%s>' % (True, inspector.__class__.__name__)) if inspector else log.warning(msg='%s\t<%s>' % (False, inspector.__name__))
    
    for model in [
        UserRoles,
        UserProfiles,
        UserAccounts,
        Comments,
        Uploads,
        Modules,
        UserActions,
        Resources,
        ViewsControlAccess
    ]:
        if inspector.has_table(model.__table__.name):
            models[model.__name__] = True
            log.info(msg='%s\t<%s>' % (models[model.__name__], model.__name__))

        else:
            models[model.__name__] = False
            log.error(msg='%s\t<%s>' % (models[model.__name__], model.__name__))

    del inspector
    del models

except Exception as exception:
    log.exception(msg=exception)

