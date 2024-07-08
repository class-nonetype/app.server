import sqlalchemy

from src.core.utils import TZ, DATABASE_URL

engine = sqlalchemy.create_engine(
    url=DATABASE_URL,
    connect_args={
        'options': '-c timezone={0}'.format(TZ)
    }
)