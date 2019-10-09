""":mod:`word_way.config` --- Word Way application configuration
~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~
"""
__all__ = 'config',


class Configuration:
    DEBUG = False


class DevConfiguration(Configuration):
    DEBUG = True


class TestConfiguration(Configuration):
    DEBUG = True
    TESTING = True


class ProdConfiguration(Configuration):
    DEBUG = False
    name = 'prod'


config = dict(
    dev=DevConfiguration,
    test=TestConfiguration,
    prod=ProdConfiguration,
)
