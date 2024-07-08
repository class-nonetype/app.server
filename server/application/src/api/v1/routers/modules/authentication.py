import fastapi
import fastapi.security
import sqlalchemy.orm
import starlette.status

from src.core.log import log

from src.core.database.session import database
from src.core.database.queries.user import (
    validate_user_authentication,
    update_last_login_date,
    select_user_full_name_by_id,
    select_user_role_name_by_user_role_id
)
from src.core.database.queries.views import (
    select_views_by_user_id
)

from src.core.schemas.user import CreateUser, UserAccount
from src.core.jwt.jwt import (
    create_access_token, verify_access_token,
    JWTBearer
)




router = fastapi.APIRouter()
authentication_schema = fastapi.security.HTTPBearer()





# Inicio de sesión.
@router.post(
    path='/sign-in',
    tags=['Autenticación'],
)
async def sign_in(UserAccount: UserAccount, request: fastapi.Request, session: sqlalchemy.orm.Session = fastapi.Depends(database)):
    
    user_authentication = validate_user_authentication(
        session=session,
        username=UserAccount.username,
        password=UserAccount.password,
    )
    if not user_authentication:
        return fastapi.responses.JSONResponse(
            status_code=starlette.status.HTTP_401_UNAUTHORIZED,
            content={'message': 'Autenticación fallida.'}
        )
    user_credential = {
        'user_id': str(user_authentication.id),
        'user_role_id': str(user_authentication.role_id),
        'username': str(user_authentication.username),
    }
    user_access_token = create_access_token(credential=user_credential)
    user_views_control_access = select_views_by_user_id(session=session, user_id=user_credential.id)
    update_last_login_date(session=session, user_id=user_authentication.id)

    if (not user_views_control_access
            or len(user_views_control_access) == 0
        ):
        return fastapi.Response(status_code=starlette.status.HTTP_403_FORBIDDEN, content={'message': 'Permiso denegado.'})
    
    user_session = {
        'client': request.client.host,
        'user_full_name': select_user_full_name_by_id(session=session, id=user_authentication.id),
        'user_id': user_authentication.id,
        'user_role_name': select_user_role_name_by_user_role_id(session=session, role_id=user_authentication.role_id),
        'access_token': user_access_token,
        'views_control_access': user_views_control_access
    }

    
    return user_session


# Creación de cuenta de usuario.
@router.post(
    path='/sign-up',
    status_code=starlette.status.HTTP_201_CREATED,
    tags=['Autenticación'],
)
async def sign_up(User: CreateUser, session: sqlalchemy.orm.Session = fastapi.Depends(database)):
    return



# Validador de sesión.
@router.post(
    path='/verify/session',
    tags=['Autenticación'],
    dependencies=[fastapi.Depends(JWTBearer())]
)
async def validate_session(Authorization: str, request: fastapi.Request, session: sqlalchemy.orm.Session = fastapi.Depends(database)):
    return


