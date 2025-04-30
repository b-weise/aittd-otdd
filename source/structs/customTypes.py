from datetime import datetime
from typing import Optional


class InvalidRange(Exception):
    pass


class DateRange:
    """
    A simple data container that stores a range of dates, accessed through the "fm" and "to" properties.
    Either or both properties can be None.
    """

    def __init__(self, fm: Optional[datetime] = None, to: Optional[datetime] = None):
        self.__to = None
        self.__fm = None
        self.to = to
        self.fm = fm

    def __repr__(self) -> str:
        """
        Generates a string that describes this object and its attributes.
        :return: A string representation of this object.
        """
        return f'{self.__class__.__name__}(fm={self.fm}, to={self.to})'

    def __eq__(self, other) -> bool:
        """
        Evaluates if this object is equal to the provided one.
        :param other: The object to compare against.
        :return: True if both objects are considered equal; False otherwise.
        """
        return self.fm == other.fm and self.to == other.to

    @property
    def fm(self) -> datetime:
        return self.__fm

    @fm.setter
    def fm(self, value: Optional[datetime] = None):
        """
        Sets the "fm" property.
        Validates the relation between "to" and the provided value if both are not None.
        Raises InvalidRange if the relation is invalid.
        If either is None, no validation is performed and the value is set.
        :param value: The value to be set.
        """
        if None not in [self.to, value] and value > self.to:
            raise InvalidRange(f'"from" value ({value}) must be earlier than "to" ({self.to})')
        self.__fm = value

    @property
    def to(self) -> datetime:
        return self.__to

    @to.setter
    def to(self, value: Optional[datetime] = None):
        """
        Sets the "to" property.
        Validates the relation between "fm" and the provided value if both are not None.
        Raises InvalidRange if the relation is invalid.
        If either is None, no validation is performed and the value is set.
        :param value: The value to be set.
        """
        if None not in [self.fm, value] and value < self.fm:
            raise InvalidRange(f'"to" value ({value}) must be later than "from" ({self.fm})')
        else:
            self.__to = value
