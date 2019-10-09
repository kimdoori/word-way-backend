""":mod:`word_way.app` --- web app
~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~
"""
from flask import Flask
from typeguard import typechecked

from .api import api
from .config import config

__all__ = 'create_app',


@typechecked
def create_app(config_name: str):
    app = Flask(__name__)
    app.register_blueprint(api)
    app.config.from_object(config[config_name])
    return app
