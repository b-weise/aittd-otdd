
class InvalidConfigsException(Exception):
    pass


class UnavailableNameException(Exception):
    pass


class MultiRotatingLogger:
    def __init__(self, configs):
        self.__configs = configs
        self.__validate_configs()

    def __validate_configs(self):
        if type(self.__configs) is not list:
            raise InvalidConfigsException('Configs must be a list.')
        if len(self.__configs) == 0:
            raise InvalidConfigsException('Configs is empty.')
        if any(map(lambda config: (type(config) is not dict), self.__configs)):
            raise InvalidConfigsException('Configs must be a populated with one or more dicts.')
        if any(map(lambda config: (type(config.get('name', None)) is not str or len(config['name']) == 0), self.__configs)):
            raise InvalidConfigsException('Every config must have at least a "name" property specified as a non empty string.')
