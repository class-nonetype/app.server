import fastapi
import fastapi.security

from src.core.utils import API_PREFIX
from src.api.v1.routers.modules import (
    authentication
)

# Mapeo: prefijo: [router].
API_ROUTERS = {
    'AUTHENTICATION': [
        authentication.router
    ]
}


router = fastapi.APIRouter()

# Itera sobre el diccionario y agrega los routers correspondientes.
for key, values in API_ROUTERS.items():
    for value in values:
        router.include_router(
            router=value,
            prefix=API_PREFIX[key]
        )