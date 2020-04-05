import typing

from flask import request
from werkzeug.local import LocalProxy

from word_way.config import current_config
from word_way.orm import Session, create_engine


@LocalProxy
def session() -> Session:
    ctx = request._get_current_object()
    try:
        session = ctx._current_session
    except AttributeError:
        ctx._current_session = session = create_session(current_config())
    finally:
        return session


def create_session(config: typing.Mapping) -> Session:
    return Session(bind=create_engine(config))
