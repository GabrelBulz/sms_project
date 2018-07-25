"""
    This module defines and initialize a Engine
    and a Session for the DB
"""

import contextlib
import functools
from sqlalchemy import create_engine
from sqlalchemy.orm import sessionmaker
import server_sms_proj.db.ConfigParser_db as ConfigParser_db


CONFIG = ConfigParser_db.ConfigMachine_db('conf.ini')
CONFIG.parse_conf()

ENGINE = None
SESSIONCLASS = None


def initialize():
    """ initialize engine and a new session"""

    global ENGINE
    global SESSIONCLASS

    ENGINE = create_engine(CONFIG.url, echo=True)
    SESSIONCLASS = sessionmaker(bind=ENGINE, expire_on_commit=False)


def get_new_session():
    """ return a new session"""
    return SESSIONCLASS()


@contextlib.contextmanager
def get_temp_session():
    """retrun a new session and close it after an operation id done"""

    try:
        session = get_new_session()
        yield session
    finally:
        session.commit()
        session.close()


def ensure_session(func):
    """ensures a session for add and get functions"""

    @functools.wraps(func)
    def wrapper(*args, **kwargs):
        session = kwargs.pop('session', None)
        if not session:
            with get_temp_session() as session:
                kwargs['session'] = session
                return func(*args, **kwargs)
        else:
            kwargs['session'] = session
            return func(*args, **kwargs)
    return wrapper
