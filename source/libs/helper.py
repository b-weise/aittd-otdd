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
