import logging
from dataclasses import dataclass

from m3t_Utils import Validation


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
        """
        :param configs: A list containing a dictionary of configurations for each logger to be created.
        """
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

        self.__loggers = []
        for config in configs:
            self.__build_logger(config)

    def __get_existent_loggers(self) -> list[str]:
        """
        Generates a list of names corresponding to the loggers present in the current runtime.
        :return: A list of logger names.
        """
        return [name for name in logging.root.manager.loggerDict.keys()]

    def __build_logger(self, config: dict):
        """
        Creates a logger based on the provided configurations.
        :param config: A dictionary of configurations for the logger to be created.
        """
        if config[ConfigKeyNames.NAME] in self.__get_existent_loggers():
            raise UnavailableNameException(f'A logger named \"{config[ConfigKeyNames.NAME]}\" already exists.')
        logger = logging.getLogger(config[ConfigKeyNames.NAME])
        self.__loggers.append(logger)
