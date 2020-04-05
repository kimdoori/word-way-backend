import ast
import os
import warnings

from celery import Celery
from celery.loaders.base import BaseLoader
from flask import has_app_context

from word_way.config import current_config, load_config


__all__ = 'Loader', 'celery',


celery = Celery(__name__, loader=f'{__name__}:Loader')


class Loader(BaseLoader):

    def read_configuration(self, env='CELERY_CONFIG_MODULE'):
        if has_app_context():
            config = current_config()
        else:
            config_name = os.environ.get(env)
            if config_name is not None:
                config = load_config(config_name)
            else:
                config = None

        try:
            worker_config = config['WORKER']
        except Exception:
            warnings.warn("--config seems not provided; isn't it missing?")
            return
        celery_config = {
            'CELERY_ACCEPT_CONTENT': ['json'],
            'CELERY_TASK_SERIALIZER': 'json',
            'CELERY_IMPORTS': ast.literal_eval(
                worker_config['celery_imports']
            ),
        }
        celery_config.update(worker_config)
        celery_config['APP_CONFIG'] = config

        return celery_config
