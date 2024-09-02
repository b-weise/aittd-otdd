from m3t_Utils import Validation
from dataclasses import dataclass


@dataclass(frozen=True)
class ConfigKeyNames:
    NAME: str = 'name'
    FILENAME: str = 'filename'
    LEVEL: str = 'level'
    MAX_BYTES: str = 'max_bytes'
    BACKUP_COUNT: str = 'backup_count'
    FORMATTER_STRING: str = 'formatter_string'
    TRACE_MESSAGE_SEPARATOR: str = 'trace_message_separator'
    TRACE_SEPARATOR: str = 'trace_separator'
    BASE_SCOPE_SKIP_LIST: str = 'base_scope_skip_list'


class UnavailableNameException(Exception):
    pass


class MultiRotatingLogger:
    """
    Builds a logger for each set of specified configs.
    The loggers will have their unique RotatingFileHandler attached.
    Each exposed method will accept a logger index. If none is provided,
    then the message will be sent to all loggers by default.
    """

    def __init__(self, configs: list[dict]):
        self.__validation = Validation()

        self.__validation.recursive_validation(configs, validations={
            'type': {'expected_type': dict},
            'key_existence': {
                'key_name': ConfigKeyNames.NAME,
                'validations': {
                    'type': {'expected_type': str},
                    'length': {'expected_range': (1, None)},
                }
            },
        })

        self.__configs = configs
