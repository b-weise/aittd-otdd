
from collections.abc import Iterable, Sized
from types import UnionType
from typing import Any


class ForbiddenTypeException(Exception):
    pass


class MandatoryTypeException(Exception):
    pass


class MinimumLengthException(Exception):
    pass


class MaximumLengthException(Exception):
    pass


class InvalidRangeLengthException(Exception):
    pass


class InvalidRangeValuesException(Exception):
    pass


class ForbiddenKeyException(Exception):
    pass


class MandatoryKeyException(Exception):
    pass


class Validation:
    """
    A set of generic validation methods.
    All exposed methods return nothing. If something is wrong then an exception is thrown.
    """

    def __from_dict(self, object_to_validate: Any, validations: dict):
        """
        Validates the provided object against the specified validations.
        Note that argument types are not validated here. That's the caller's job.
        :param object_to_validate: An object of any type, to be validated.
        :param validations: A dict containing Validation method names (i.e. "type") as keys
        and dictionaries of parameters as their respective method arguments, not including "object_to_validate",
        as every item will be passed in its place.
        """
        for method_name, method_arguments in validations.items():
            getattr(self, method_name)(object_to_validate, **method_arguments)

    def __type(self, object_to_validate: Any, expected_type: type | UnionType, reversed_validation: bool = False):
        """
        Internal usage only.
        Checks the object type against the provided types.
        :param object_to_validate: An object of any type, to be validated.
        :param expected_type: The type that is expected, or a UnionType of them.
        :param reversed_validation: If True, the validation is reversed.
        """
        object_is_instance = isinstance(object_to_validate, expected_type)

        if not reversed_validation and not object_is_instance:  # plain (non-reversed) validation failure
            raise MandatoryTypeException(f'Object must be of type: {expected_type}.')
        if reversed_validation and object_is_instance:  # reversed validation failure
            raise ForbiddenTypeException(f'Object must not be of type: {expected_type}.')

    def type(self, object_to_validate: Any, expected_type: type | UnionType, reversed_validation: bool = False):
        """
        Checks the object type against the provided type.
        :param object_to_validate: An object of any type, to be validated.
        :param expected_type: The type that is expected, or a UnionType of them.
        :param reversed_validation: If True, the validation is reversed.
        """
        self.__type(expected_type, type | UnionType)
        self.__type(reversed_validation, bool)
        self.__type(object_to_validate, expected_type, reversed_validation)

    def length(self, object_to_validate: Sized, expected_range: tuple):
        """
        Checks the length of the object against the expected range.
        :param object_to_validate: A Sized object which length is to be validated.
        :param expected_range: A tuple in the form [from, to); None means no limit in that direction.
        """
        self.__type(object_to_validate, Sized)
        self.__type(expected_range, tuple)
        if len(expected_range) != 2:
            raise InvalidRangeLengthException(
                f'The expected_range parameter should be a tuple containing [from, to); None means no limit in that direction.'
            )

        object_length = len(object_to_validate)
        min_length = expected_range[0]
        max_length = expected_range[1]

        if min_length is not None and max_length is not None:
            self.__type(min_length, int)
            self.__type(max_length, int)
            if min_length >= max_length:
                raise InvalidRangeValuesException(
                    f'The minimum value provided ({min_length}) must be lower than the maximum value provided ({max_length}).'
                )

        if min_length is not None:
            self.__type(min_length, int)
            if object_length < min_length:
                raise MinimumLengthException(
                    f'Object length ({object_length}) is below the minimum expected ({min_length}).'
                )

        if max_length is not None:
            self.__type(max_length, int)
            if object_length >= max_length:
                raise MaximumLengthException(
                    f'Object length ({object_length}) is above the maximum expected ({max_length}).'
                )

    def iterate(self, objects: Iterable, validations: dict):
        """
        Checks specified validations against each item in objects.
        :param objects: An Iterable of objects to be validated.
        :param validations: A dict containing Validation method names (i.e. "type") as keys
        and dicts of parameters as their respective method arguments, not including "object_to_validate",
        as every item will be passed in its place.
        """
        self.__type(objects, Iterable)
        self.__type(validations, dict)
        for object_to_validate in objects:
            self.__from_dict(object_to_validate, validations)

    def key_existence(self, object_to_validate: dict, key_name: str, validations: dict = {},
                      reversed_validation: bool = False):
        """
        Checks that the specified key exists in the provided dictionary.
        :param object_to_validate: A dictionary which keys are to be validated.
        :param key_name: The name of the dictionary key to validate.
        :param validations: A dict containing Validation method names (i.e. "type") as keys
        and dicts of parameters as their respective method arguments, not including "object_to_validate",
        as every item will be passed in its place.
        :param reversed_validation: If True, the validation is reversed,
        i.e. key_name is NOT expected to be found.
        """
        self.__type(object_to_validate, dict)
        self.__type(key_name, str)
        self.length(key_name, (1, None))
        self.__type(validations, dict)
        self.__type(reversed_validation, bool)

        key_is_present = key_name in object_to_validate

        if not reversed_validation:
            if key_is_present:  # plain (non-reversed) validation success
                self.__from_dict(object_to_validate[key_name], validations)
            else:  # plain (non-reversed) validation failure
                raise MandatoryKeyException(f'Mandatory key \"{key_name}\" was not found.')
        if reversed_validation and key_is_present:  # reversed validation failure
            raise ForbiddenKeyException(f'Forbidden key \"{key_name}\" was found.')
