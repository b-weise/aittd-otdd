
class InvalidTypeException(Exception):
    pass


class Validation:

    def type(self, object_to_validate, expected_type: type):
        if not isinstance(object_to_validate, expected_type):
            raise InvalidTypeException(f'Object must be of type: {expected_type.__name__}.')
