import dataclasses
from typing import Optional, Type


@dataclasses.dataclass
class BaseTestCase:
    """Base class for test cases."""
    id: Optional[str] = dataclasses.field(default=None)
    __id: str = dataclasses.field(init=False, repr=False)
    expected_exception: Optional[Type[Exception]] = None

    @property
    def id(self) -> str | None:
        """
        Getter of the "id" property.
        :return: A string formatted in such a way it's easily recognized in pytest logs.
        """
        if isinstance(self.__id, str):
            return f'--- {self.__id} ---'.upper()
        else:
            return None

    @id.setter
    def id(self, provided_id: str):
        self.__id = provided_id
