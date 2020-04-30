import typing

from celery import current_task
from flask import request, has_request_context
from werkzeug.local import LocalProxy

from word_way.config import current_config
from word_way.orm import Session, create_engine


def current_context():
    if has_request_context():
        return request._get_current_object()
    else:
        return current_task


@LocalProxy
def session() -> Session:
    ctx = current_context()
    try:
        session = ctx._current_session
    except AttributeError:
        ctx._current_session = session = create_session(current_config())
    finally:
        return session


def create_session(config: typing.Mapping) -> Session:
    return Session(bind=create_engine(config))
