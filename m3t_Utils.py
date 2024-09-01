
class InvalidTypeException(Exception):
    pass


class InvalidLengthException(Exception):
    pass


class InvalidRangeException(Exception):
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

    def length(self, object_to_validate, expected_range: tuple):
        """
        Checks the length of the object against the expected range.
        :param object_to_validate: An object of any type, to be validated.
        :param expected_range: A tuple in the form [from, to); None means no limit in that direction.
        """
        self.type(expected_range, tuple)
        if len(expected_range) != 2:
            raise InvalidLengthException(f'The expected_range parameter should be a tuple containing [from, to); None means no limit in that direction.')

        object_length = len(object_to_validate)
        min_length = expected_range[0]
        max_length = expected_range[1]

        if min_length is not None and max_length is not None:
            self.type(min_length, int)
            self.type(max_length, int)
            if min_length >= max_length:
                raise InvalidRangeException(f'The minimum value provided ({min_length}) must be lower than the maximum value provided ({max_length}).')

        if min_length is not None:
            self.type(min_length, int)
            if object_length < min_length:
                raise InvalidLengthException(f'Object length ({object_length}) is below the minimum expected ({min_length}).')

        if max_length is not None:
            self.type(max_length, int)
            if object_length >= max_length:
                raise InvalidLengthException(f'Object length ({object_length}) is above the maximum expected ({max_length}).')
