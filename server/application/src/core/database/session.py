import sqlalchemy.orm

import sqlalchemy.orm
from src.core.log import log
from src.core.database.engine import engine






# Construye un generador de sesiones SQLAlchemy con configuraciones específicas.
#   - autocommit      Desactiva la confirmación automática de transacciones.
#   - autoflush       Desactiva la actualización automática de objetos en la sesión.
#   - bind            Asocia el motor creado anteriormente con las sesiones.
session = sqlalchemy.orm.sessionmaker(autocommit=False, autoflush=False, bind=engine)



async def database():
    database: sqlalchemy.orm.Session = session()

    try:
        yield database

    except Exception as exception:
        log.exception(exception)

    finally:
        database.close()