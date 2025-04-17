import sys
from collections.abc import Callable, Sequence
from datetime import datetime
from pathlib import Path
from typing import Any


class Helper:
    """
    A static utility class intended to hold generic, frequently used methods.
    """

    @staticmethod
    def get_fully_qualified_name(obj: Callable) -> str:
        """
        Returns the fully qualified name of the given callable, including its module name.
        :param obj: A callable object to retrieve the qualified name from.
        :return: A string representing the fully qualified name.
        """
        return f'{obj.__module__}.{obj.__qualname__}'

    @staticmethod
    def get_module_callable(fully_qualified_name: str) -> Callable | None:
        """
        Resolves an object by its fully qualified name.
        :param fully_qualified_name: The fully qualified name of the target object.
        :return: The resolved object if found; otherwise, None.
        """
        subpaths = fully_qualified_name.split('.')
        module_name = subpaths.pop(0)
        callable_object = None
        if module_name in sys.modules:
            module_obj = sys.modules[module_name]
            for subpath in subpaths:
                callable_object = getattr(callable_object or module_obj, subpath, None)
        return callable_object

    @staticmethod
    def stringify_objects(raw_input: Any) -> Any:
        """
        Stringifies the given object or a container of objects.
        :param raw_input: The object to be stringified, or a container that will be traversed recursively.
        :return: A stringified version of the input if applicable; otherwise, the original input.
        """

        def is_container(value: Any) -> bool:
            """
            Determines whether the given object is considered a container.
            In this context, a 'container' refers to dictionaries and Sequences, excluding strings.
            :param value: The object to evaluate.
            :return: True if the object is a container; False otherwise.
            """
            return isinstance(value, Sequence | dict) and type(value) is not str

        def stringify(value: Any) -> Any:
            """
            Converts the given object to its string representation.
            If the object is considered a container, it is processed by stringify_objects.
            :param value: The object to be stringified.
            :return: A stringified version of the object if applicable; otherwise, the original object.
            """
            if is_container(value):
                return Helper.stringify_objects(value)
            elif isinstance(value, Path | datetime):
                return str(value)
            elif isinstance(value, Callable):
                return Helper.get_fully_qualified_name(value)
            else:
                return value

        if type(raw_input) is dict:
            return {key: (stringify(value))
                    for key, value in zip(raw_input.keys(), raw_input.values())}
        elif is_container(raw_input):
            return list(map(lambda item: (stringify(item)), raw_input))
        else:
            return stringify(raw_input)
