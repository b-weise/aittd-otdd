import logging
import dataclasses
from dataclasses import dataclass
from typing import Optional, Iterable
import dacite

from m3t_Utils import Validation


@dataclass
class Config:
    name: str
    filename: Optional[str] = 'filename'
    level: Optional[int] = logging.DEBUG
    max_bytes: Optional[int] = 1024
    backup_count: Optional[int] = 5
    formatter_string: Optional[str] = 'formatter_string'
    trace_message_separator: Optional[str] = 'trace_message_separator'
    trace_separator: Optional[str] = 'trace_separator'
    base_scope_skip_list: Optional[list] = dataclasses.field(default_factory=list)


class UnavailableNameException(Exception):
    pass


class EmptyNameException(Exception):
    pass


class MultiRotatingLogger:
    """
    Builds a logger for each set of specified configs.
    The loggers will have their unique RotatingFileHandler attached.
    Each exposed method will accept a logger index. If none is provided,
    then the message will be sent to all loggers by default.
    """

    def __init__(self, configs: Iterable[dict]):
        """
        :param configs: An Iterable containing a dictionary of configurations for each logger to be created. Check
        Config.
        """
        self.__validation = Validation()
        self.__validation.iterate(configs, validations={
            'type': {'expected_type': dict},
        })

        self.__loggers = []
        for config_dict in configs:
            config_dataclass = dacite.from_dict(Config, config_dict)
            self.__build_logger(config_dataclass)

    def __get_existent_loggers(self) -> list[str]:
        """
        Generates a list of names corresponding to the loggers present in the current runtime.
        :return: A list of logger names.
        """
        return [name for name in logging.root.manager.loggerDict.keys()]

    def __build_logger(self, config: Config):
        """
        Creates a logger based on the provided configurations.
        :param config: A Config instance containing configurations for the logger to be created. Check Config.
        """
        if len(config.name) == 0:
            raise EmptyNameException(f'The logger name can not be an empty string.')
        if config.name in self.__get_existent_loggers():
            raise UnavailableNameException(f'A logger named \"{config.name}\" already exists.')
        logger = logging.getLogger(config.name)
        self.__loggers.append(logger)
