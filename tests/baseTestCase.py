import dataclasses
from typing import Optional, Type


@dataclasses.dataclass
class BaseTestCase:
    """
    Base class for test cases.
    """

    __id: Optional[str] = dataclasses.field(default=None, repr=False)
    id: Optional[str] = dataclasses.field(default=None)
    expected_exception: Optional[Type[Exception]] = None

    @property
    def id(self) -> str | None:
        """
        Getter of the "id" property.
        :return: If "id" is set, returns a string formatted for easy recognition in pytest logs;
        otherwise, returns None to suppress pytest's default printing.
        """
        if isinstance(self.__id, str) and self.__id != '':
            return f'--- {self.__id} ---'.upper()
        else:
            return None

    @id.setter
    def id(self, provided_id: str):
        self.__id = provided_id
