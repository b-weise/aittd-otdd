
class InvalidConfigsException(Exception):
    pass


class UnavailableNameException(Exception):
    pass


class MultiRotatingLogger:
    def __init__(self, configs):
        self.__configs = configs
        self.__validate_configs()

    def __validate_configs(self):
        if len(self.__configs) == 0:
            raise InvalidConfigsException('Configs is empty.')
