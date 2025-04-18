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

        def walk_objects(input_obj: Any, callback: Callable) -> Any:
            """
            Recursively traverses the given object in a depth-first fashion,
            invoking the callback on each plain value encountered.
            :param input_obj: The object to traverse.
            :param callback: A callback used to process plain values.
            :return: Either, a dictionary or list with every value processed by the callback,
            or the output of the callback itself.
            """
            if isinstance(input_obj, dict):
                return {key: (walk_objects(value, callback))
                        for key, value in zip(input_obj.keys(), input_obj.values())}
            elif isinstance(input_obj, Sequence) and not isinstance(input_obj, str):
                return list(map(lambda item: (walk_objects(item, callback)), input_obj))
            else:
                return callback(input_obj)

        def stringify(value: Any) -> Any:
            """
            Converts the given object to its string representation.
            :param value: The object to be stringified.
            :return: A stringified version of the object if applicable; otherwise, the original object.
            """
            if isinstance(value, Path | datetime):
                return str(value)
            elif isinstance(value, Callable):
                return Helper.get_fully_qualified_name(value)
            else:
                return value

        return walk_objects(raw_input, stringify)
