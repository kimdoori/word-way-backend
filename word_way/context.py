import typing

from flask import current_app, request
from werkzeug.local import LocalProxy

from .orm import Session, create_engine


@LocalProxy
def current_config() -> typing.Mapping:
    return current_app.config['APP_CONFIG']


@LocalProxy
def session() -> Session:
    ctx = request._get_current_object()
    try:
        session = ctx._current_session
    except AttributeError:
        ctx._current_session = session = Session(
            bind=create_engine(current_config)
        )
    finally:
        return session
