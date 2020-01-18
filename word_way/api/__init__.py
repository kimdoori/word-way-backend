""":mod:`word_way.api` --- Word Way API
~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~
"""
from flask import Blueprint

__all__ = 'api', 'ping',


api = Blueprint('api', __name__)


@api.route('/ping/', methods=['GET'])
def ping():
    return 'pong'
