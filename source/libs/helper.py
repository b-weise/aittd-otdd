import sys
from collections.abc import Callable


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
