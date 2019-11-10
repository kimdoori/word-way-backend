import typing

from sqlalchemy.engine import Engine, create_engine as create_engine_
from sqlalchemy.ext.declarative import declarative_base
from sqlalchemy.ext.declarative.api import DeclarativeMeta
from sqlalchemy.orm.session import Session as _Session, sessionmaker

__all__ = 'Base', 'Session', 'create_engine'

Base: DeclarativeMeta = declarative_base()
Session: _Session = sessionmaker()


def create_engine(config: typing.Mapping) -> Engine:
    assert config['DATABASE']['URL'], "config['DATABASE']['URL'] required."
    return create_engine_(config['DATABASE']['URL'])
