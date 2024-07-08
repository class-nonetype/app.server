import fastapi
import fastapi.security
import sqlalchemy.orm
import starlette.status
import uuid

from src.core.log import log
from src.core.jwt.jwt import decode_access_token

from src.core.database.models.modules import Modules
from src.core.database.models.resources import Resources
from src.core.database.models.views_control_access import ViewsControlAccess

from src.core.database.queries.user import select_action_name_by_action_id, select_user_by_id







def select_resources(session: sqlalchemy.orm.Session):
    resources: dict = {}

    for resource in session.query(Resources).all():
        resources[resource.name] = resource.id

    return resources


def select_resource_name_by_resource_id(session: sqlalchemy.orm.Session, resource_id: uuid.UUID):
    return session.query(Resources.name).filter(Resources.id == resource_id).first()


def validate_resource_access(session: sqlalchemy.orm.Session, user_role_id: uuid.UUID, resource_id: uuid.UUID):
    try:
        roles = []
        actions = {}
        resources = []
        
        views_control_access = session.query(ViewsControlAccess).filter(
            sqlalchemy.and_(
                ViewsControlAccess.user_role_id == user_role_id,
                ViewsControlAccess.resource_id == resource_id
            )
        ).all()


        for view in views_control_access:
            if view.role_id not in roles:
                roles.append(view.role_id)

            if view.resource_id not in resources:
                resources.append(view.resource_id)

            action_id = view.action_id
            action_name = select_action_name_by_action_id(session=session, action_id=action_id)
            actions.update({action_name: action_id})
            
        identifier = {
            "roles": roles,
            "actions": actions,
            "resources": resources
        }
        return identifier
    except Exception as exception:
        log.exception(msg=exception)


def validate_module_access(session: sqlalchemy.orm.Session, token: str, resource_id: uuid.UUID, action: str):
    decoded_token = decode_access_token(token=token)
    if decoded_token:
        user_role_id = uuid.UUID(decoded_token['user_role_id'])

        resource_access = validate_resource_access(session=session, user_role_id=user_role_id, resource_id=resource_id)
        
        if (resource_access is None
            or len(resource_access['roles']) == 0
            and len(resource_access['resources']) == 0
            and len(resource_access['actions']) == 0):
            return False

        if user_role_id in resource_access['roles']:
            if resource_id in resource_access['resources']:
                if any(resource_access['actions']):
                    try:
                        if resource_access['actions'][action]:
                            print(f'{resource_access["actions"][action]}')
                            return True
                    except KeyError:
                        pass
        return False


def select_module_name_by_module_id(session: sqlalchemy.orm.Session, module_id: uuid.UUID):
    return session.query(Modules.name).filter(Modules.id == module_id).first()


def select_views_control_access_by_user_role_id(session: sqlalchemy.orm.Session, user_role_id: uuid.UUID) -> list:
    views_control_access = (
        session.query(ViewsControlAccess)
        .join(ViewsControlAccess.resource_relation)
        .join(ViewsControlAccess.action_relation)
        .filter(ViewsControlAccess.user_role_id == user_role_id)
        .options(sqlalchemy.orm.joinedload(ViewsControlAccess.resource_relation))
        .all()
    )

    views = []

    for view_control in views_control_access:
        module_name = select_module_name_by_module_id(session=session, module_id=view_control.module_id)[0]
        resource_name = view_control.resource_relation.name
        action_name = view_control.action_relation.name
        modules = next((module for module in views if module['module'] == module_name), None)

        if modules:
            resources = next((resource for resource in modules['resources'] if resource['name'] == resource_name), None)
            if resources:
                resources['actions'].append(action_name)

            else:
                modules['resources'].append({'name': resource_name, 'actions': [action_name]})
        else:
            views.append({
                'module': module_name,
                'resources': [
                    {
                        'name': resource_name,
                        'actions': [action_name]
                    }
                ]
            })

    return views


def select_views_by_user_id(session: sqlalchemy.orm.Session, user_id: uuid.UUID):
    user = select_user_by_id(session=session, id=user_id)

    views_control_access: list = select_views_control_access_by_user_role_id(
        session=session,
        user_role_id=user.role_id
    )

    if not views_control_access or len(views_control_access) == 0:
        content = {'message': 'Permiso denegado.'}

        return fastapi.responses.JSONResponse(status_code=starlette.status.HTTP_403_FORBIDDEN, content=content)

    return views_control_access



