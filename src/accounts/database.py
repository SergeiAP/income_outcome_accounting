# pylint: disable=missing-module-docstring
from sqlalchemy import create_engine
from sqlalchemy.orm import sessionmaker

from .settings import settings


# For a first run: Base.metadata.create_all(engine)
engine = create_engine(
    settings.database_url,
    # To have one query - one session
    connect_args={'check_same_thread': False},
)

Session = sessionmaker(
    engine,
    autocommit=False,  # better to make manually
    autoflush=False,
)


def get_session():
    """Session handler"""
    session = Session()
    try:
        yield session
        session.commit()
    except:
        session.rollback()
        raise      
    finally:
        session.close()
