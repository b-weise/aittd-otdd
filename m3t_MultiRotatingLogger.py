from m3t_Utils import Validation


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
                'key_name': 'name',
                'validations': {
                    'type': {'expected_type': str},
                    'length': {'expected_range': (1, None)},
                }
            },
        })

        self.__configs = configs
