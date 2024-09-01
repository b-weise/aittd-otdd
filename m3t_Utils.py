
class InvalidTypeException(Exception):
    pass


class InvalidLengthException(Exception):
    pass


class Validation:
    """
    A set of generic validation methods.
    All exposed methods return nothing. If something is wrong then an exception is thrown.
    """

    def type(self, object_to_validate, expected_type: type, reversed_validation: bool = False):
        """
        Checks the object type against the type provided.
        :param object_to_validate: An object of any type, to be validated.
        :param expected_type: The type that is expected.
        :param reversed_validation: If this is a truthy value, the validation is reversed.
        """
        validation_result = isinstance(object_to_validate, expected_type)
        if reversed_validation:
            validation_result = not validation_result
        if not validation_result:
            raise InvalidTypeException(f'Object must be of type: {expected_type.__name__}.')
