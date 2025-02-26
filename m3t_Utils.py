"""
This was the starting point of a tool designed to build objects out of dictionaries. This way, project settings
could be stored in JSON files, and loaded into objects that define each setting's specification.
Then I discovered Dacite, which accomplishes exactly that.
Nonetheless, it served to establish the guidelines I'd follow while migrating the rest of the code using TDD.
"""

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
    A collection of generic validation methods.
    All exposed methods return nothing. If validation fails, an exception is raised.
    """

    def __from_dict(self, object_to_validate: Any, validations: dict[str, dict[str, Any]]):
        """
        Checks object against the specified validations.
        Argument types are not validated here; the caller's responsible for that.
        :param object_to_validate: The object to be validated.
        :param validations: A dictionary where keys are names of Validation methods (i.e. "type"),
        and values are dictionaries containing method arguments, excluding "object_to_validate",
        which is provided separately.
        """
        for method_name, method_arguments in validations.items():
            getattr(self, method_name)(object_to_validate, **method_arguments)

    def __type(self, object_to_validate: Any, expected_type: type | UnionType, reversed_validation: bool = False):
        """
        For internal use only.
        Validates whether the object matches the expected type.
        :param object_to_validate: The object to be validated.
        :param expected_type: The expected type or UnionType.
        :param reversed_validation: If True, validation is reversed.
        """
        object_is_instance = isinstance(object_to_validate, expected_type)

        if not reversed_validation and not object_is_instance:  # plain (non-reversed) validation failure
            raise MandatoryTypeException(f'Object must be of type: {expected_type}.')
        if reversed_validation and object_is_instance:  # reversed validation failure
            raise ForbiddenTypeException(f'Object must not be of type: {expected_type}.')

    def type(self, object_to_validate: Any, expected_type: type | UnionType, reversed_validation: bool = False):
        """
        Validates whether the object matches the expected type.
        :param object_to_validate: The object to be validated.
        :param expected_type: The expected type or UnionType.
        :param reversed_validation: If True, validation is reversed.
        """
        self.__type(expected_type, type | UnionType)
        self.__type(reversed_validation, bool)
        self.__type(object_to_validate, expected_type, reversed_validation)

    def length(self, object_to_validate: Sized, expected_range: tuple):
        """
        Checks whether the object's length falls within the expected range.
        :param object_to_validate: A Sized object whose length is to be validated.
        :param expected_range: A tuple in the form [from, to); Use None to indicate no limit in that direction.
        """
        self.__type(object_to_validate, Sized)
        self.__type(expected_range, tuple)
        if len(expected_range) != 2:
            raise InvalidRangeLengthException(
                f'The expected_range parameter must be a tuple in the form [from, to); Use None to indicate no limit in that direction.'
            )

        object_length = len(object_to_validate)
        min_length = expected_range[0]
        max_length = expected_range[1]

        if min_length is not None and max_length is not None:
            self.__type(min_length, int)
            self.__type(max_length, int)
            if min_length >= max_length:
                raise InvalidRangeValuesException(
                    f'The minimum value ({min_length}) must be lower than the maximum value ({max_length}).'
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

    def iterate(self, objects: Iterable, validations: dict[str, dict[str, Any]]):
        """
        Checks each item in objects against the specified validations.
        :param objects: An Iterable of objects to be validated.
        :param validations: A dictionary where keys are names of Validation methods (i.e. "type"),
        and values are dictionaries containing method arguments, excluding "object_to_validate",
        which is provided separately.
        """
        self.__type(objects, Iterable)
        self.__type(validations, dict)
        for object_to_validate in objects:
            self.__from_dict(object_to_validate, validations)

    def key_existence(self, object_to_validate: dict[str, Any], key_name: str,
                      validations: dict[str, dict[str, Any]] = {}, reversed_validation: bool = False):
        """
        Checks whether the specified key is present in the dictionary.
        :param object_to_validate: A dictionary whose keys are to be validated.
        :param key_name: The dictionary key to search for.
        :param validations: A dictionary where keys are names of Validation methods (i.e. "type"),
        and values are dictionaries containing method arguments, excluding "object_to_validate",
        which is provided separately.
        :param reversed_validation: If True, validation is reversed, i.e., key is NOT expected to be found.
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
