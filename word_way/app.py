""":mod:`word_way.app` --- web app
~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~
"""
from flask import Flask
from typeguard import typechecked

from .api import api
from .api.word import word
from .config import load_config

__all__ = 'create_app',


@typechecked
def create_app(config_name: str) -> Flask:
    app = Flask(__name__)
    app.register_blueprint(api)
    app.register_blueprint(word)
    config = load_config(config_name)
    app.config.update(config['WEB'])
    app.config['APP_CONFIG'] = config
    return app
