import os
from pathlib import Path

os.chdir(path=Path(__file__).parent.absolute())

import fastapi
import fastapi.middleware.cors
import fastapi.staticfiles

from src.core.utils import (
    ALL,
    ALLOWED,
    API_PREFIX,
    API_TITLE,
    API_DESCRIPTION,
    API_VERSION,
    API_HOST,
    API_PORT,
    API_TIMEZONE,
    API_STATIC_NAME,
    STATIC_DIRECTORY
)
from src.api.v1.routers import application




# Inicialización de la aplicación
app = fastapi.FastAPI(
    title=API_TITLE,
    description=API_DESCRIPTION,
    version=API_VERSION
)
app.timezone = API_TIMEZONE
app.include_router(router=application.router)


# Se verifica si el directorio existe y si es así, 
# se monta la ruta '/api/static' para 
# contener los anexos que serán subidos/cargados en los módulos de 
# conformidades y capacitaciones.
if STATIC_DIRECTORY.exists():
    app.mount(
        path=API_PREFIX['STATIC'],
        app=fastapi.staticfiles.StaticFiles(directory=STATIC_DIRECTORY),
        name=API_STATIC_NAME
    )

# Agrega el middleware CORS para permitir solicitudes desde cualquier origen ('*').
# También se permite el uso de credenciales, todos los métodos y headers.
app.add_middleware(
    middleware_class = fastapi.middleware.cors.CORSMiddleware,
    allow_origins = ALL,
    allow_credentials = ALLOWED,
    allow_methods = ALL,
    allow_headers = ALL
) 




# Punto de entrada principal
if __name__ == '__main__':
    # Se importa la libreria 'uvicorn' con la finalidad de instanciar un servidor utilizando 
    # la aplicación FastAPI definida previamente.
    import uvicorn

    # host -> 0.0.0.0
    # port ->      80
    uvicorn.run(app=app, host=API_HOST, port=API_PORT)
    
    
    # Docker
    #
    # Levantamiento
    # -------------
    # docker compose up --build -d
    #
    # Eliminar todas las imagenes de manera forzada
    # docker rmi -f $(docker images -q) --force
    #
    # Acceso a los contenedores3
    # --------------------------
    # docker exec -it backend.api.container sh
    # docker exec -it postgresql.container sh
    #   psql -U postgres -d storage
    #
    #   Listar bases de datos                           \l
    #   Conectar a una base de datos específica         \c <database>
    #   Listar tablas en la base de datos actual        \dt
    #   Ejecutar una consulta SQL                       SELECT * FROM <table_name>;
    #   Salir de psql                                   \q

