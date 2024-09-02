class InvalidTypeException(Exception):
    pass


class InvalidLengthException(Exception):
    pass


class InvalidRangeException(Exception):
    pass


class KeyExistenceException(Exception):
    pass


class Validation:
    """
    A set of generic validation methods.
    All exposed methods return nothing. If something is wrong then an exception is thrown.
    """

    def __validate_from_dict(self, object_to_validate, validations: dict):
        """
        Validates provided object against the specified validations.
        Note that argument types are not validated here. That's the caller's job.
        :param object_to_validate: An object of any type, to be validated.
        :param validations: A dict containing Validation method names (i.e. "type") as keys
        and dicts of parameters as their respective method arguments, not including "object_to_validate",
        as every item will be passed in its place.
        """
        for method_name, method_arguments in validations.items():
            getattr(self, method_name)(object_to_validate, **method_arguments)

    def type(self, object_to_validate, expected_type: type, reversed_validation: bool = False):
        """
        Checks the object type against the provided type.
        :param object_to_validate: An object of any type, to be validated.
        :param expected_type: The type that is expected.
        :param reversed_validation: If this is a truthy value, the validation is reversed.
        """
        validation_result = isinstance(object_to_validate, expected_type)

        if not reversed_validation and not validation_result:
            raise InvalidTypeException(f'Object must be of type: {expected_type.__name__}.')
        if reversed_validation and validation_result:
            raise InvalidTypeException(f'Object must NOT be of type: {expected_type.__name__}.')

    def length(self, object_to_validate, expected_range: tuple):
        """
        Checks the length of the object against the expected range.
        :param object_to_validate: An object of any type, to be validated.
        :param expected_range: A tuple in the form [from, to); None means no limit in that direction.
        """
        self.type(expected_range, tuple)
        if len(expected_range) != 2:
            raise InvalidLengthException(
                f'The expected_range parameter should be a tuple containing [from, to); None means no limit in that direction.'
            )

        object_length = len(object_to_validate)
        min_length = expected_range[0]
        max_length = expected_range[1]

        if min_length is not None and max_length is not None:
            self.type(min_length, int)
            self.type(max_length, int)
            if min_length >= max_length:
                raise InvalidRangeException(
                    f'The minimum value provided ({min_length}) must be lower than the maximum value provided ({max_length}).'
                )

        if min_length is not None:
            self.type(min_length, int)
            if object_length < min_length:
                raise InvalidLengthException(
                    f'Object length ({object_length}) is below the minimum expected ({min_length}).'
                )

        if max_length is not None:
            self.type(max_length, int)
            if object_length >= max_length:
                raise InvalidLengthException(
                    f'Object length ({object_length}) is above the maximum expected ({max_length}).'
                )

    def recursive_validation(self, objects, validations: dict):
        """
        Checks specified validations against each item in objects.
        :param objects: An iterable of objects to be validated.
        :param validations: A dict containing Validation method names (i.e. "type") as keys
        and dicts of parameters as their respective method arguments, not including "object_to_validate",
        as every item will be passed in its place.
        """
        self.type(validations, dict)
        for object_to_validate in objects:
            self.__validate_from_dict(object_to_validate, validations)

    def key_existence(
            self, object_to_validate: dict, key_name: str, validations: dict = {}, reversed_validation: bool = False
    ):
        """
        Checks that the specified key exists in the provided dictionary.
        :param object_to_validate: An object of any type, to be validated.
        :param key_name: The name of the dictionary key to validate.
        :param validations: A dict containing Validation method names (i.e. "type") as keys
        and dicts of parameters as their respective method arguments, not including "object_to_validate",
        as every item will be passed in its place.
        :param reversed_validation: If this is a truthy value, the validation is reversed,
        i.e. key_name is NOT expected to be found.
        """
        self.type(object_to_validate, dict)
        self.type(key_name, str)
        self.length(key_name, (1, None))
        self.type(validations, dict)
        self.type(reversed_validation, bool)

        validation_result = key_name in object_to_validate

        if not reversed_validation and not validation_result:
            raise KeyExistenceException(f'Compulsory key \"{key_name}\" not found.')
        if reversed_validation and validation_result:
            raise KeyExistenceException(f'Unexpected key \"{key_name}\" was found.')

        if not reversed_validation and validation_result:
            self.__validate_from_dict(object_to_validate[key_name], validations)
