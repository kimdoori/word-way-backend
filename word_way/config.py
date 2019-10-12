""":mod:`word_way.config` --- Word Way application configuration
~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~
"""
import configparser
from typeguard import typechecked

__all__ = 'load_config',


@typechecked
def load_config(config_name: str) -> configparser.ConfigParser:
    config = configparser.ConfigParser()
    # 옵션 이름을 case sensitive 하게 가져오기 위해서
    config.optionxform = str
    config.read(f'conf/{config_name}.conf')
    return config
