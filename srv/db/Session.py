from sqlalchemy import create_engine
from sqlalchemy.orm import sessionmaker
import db.ConfigParser_db as ConfigParser_db

import contextlib
import functools



config = ConfigParser_db.ConfigMachine_db('conf.ini')
config.parse_conf()

engine = None
SessionClass = None


def initialize():
    global engine
    global SessionClass

    engine = create_engine('sqlite:///:memory:',echo=True)
    SessionClass = sessionmaker(bind=engine, expire_on_commit=False)


def get_new_session():
    return SessionClass()


@contextlib.contextmanager
def get_temp_session():
    try:
        session = get_new_session()
        yield session
    finally:
        session.commit()
        session.close()


def ensure_session(f):
    @functools.wraps(f)
    def wrapper(*args, **kwargs):
        session = kwargs.pop('session', None)
        if not session:
            with get_temp_session() as session:
                kwargs['session'] = session
                return f(*args, **kwargs)
        else:
            kwargs['session'] = session
            return f(*args, **kwargs)
    return wrapper
