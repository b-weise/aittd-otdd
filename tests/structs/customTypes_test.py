from dataclasses import dataclass
from datetime import datetime, UTC
from typing import Optional
from zoneinfo import ZoneInfo

import pytest

from source.libs.baseTestCase import BaseTestCase
from source.structs.customTypes import DateRange, InvalidRange


@dataclass
class DateRangeTestCase(BaseTestCase):
    input_from: Optional[datetime] = None
    input_to: Optional[datetime] = None


DRangeTC = DateRangeTestCase


@pytest.mark.parametrize('test_case', [pytest.param(test_case, id=test_case.id) for test_case in [
    DRangeTC(id='no values'),
    DRangeTC(id='"from" value only, offset-naive datetimes',
             input_from=datetime(2025, 1, 1)),
    DRangeTC(input_from=datetime(2025, 1, 1, 23, 0, 0)),
    DRangeTC(id='"from" value only, offset-aware datetimes',
             input_from=datetime(2025, 1, 1, tzinfo=UTC)),
    DRangeTC(input_from=datetime(2025, 1, 1, 23, 0, 0, tzinfo=UTC)),
    DRangeTC(id='"to" value only, offset-naive datetimes',
             input_to=datetime(2025, 1, 1)),
    DRangeTC(input_to=datetime(2025, 1, 1, 23, 0, 0)),
    DRangeTC(id='"to" value only, offset-aware datetimes',
             input_to=datetime(2025, 1, 1, tzinfo=UTC)),
    DRangeTC(input_to=datetime(2025, 1, 1, 23, 0, 0, tzinfo=UTC)),
    DRangeTC(id='both values, offset-naive datetimes',
             input_from=datetime(2025, 1, 1),
             input_to=datetime(2025, 1, 1)),
    DRangeTC(input_from=datetime(2025, 1, 1),
             input_to=datetime(2025, 1, 2)),
    DRangeTC(input_from=datetime(2025, 1, 1),
             input_to=datetime(2025, 2, 1)),
    DRangeTC(input_from=datetime(2025, 1, 1),
             input_to=datetime(2026, 1, 1)),
    DRangeTC(input_from=datetime(2025, 1, 1, 23, 0, 0),
             input_to=datetime(2026, 1, 1, 23, 0, 0)),
    DRangeTC(input_from=datetime(2025, 1, 1, 22, 0, 0),
             input_to=datetime(2025, 1, 1, 23, 0, 0)),
    DRangeTC(id='both values, offset-aware datetimes',
             input_from=datetime(2025, 1, 1, tzinfo=UTC),
             input_to=datetime(2025, 1, 1, tzinfo=UTC)),
    DRangeTC(input_from=datetime(2025, 1, 1, tzinfo=UTC),
             input_to=datetime(2025, 1, 2, tzinfo=UTC)),
    DRangeTC(input_from=datetime(2025, 1, 1, tzinfo=UTC),
             input_to=datetime(2025, 2, 1, tzinfo=UTC)),
    DRangeTC(input_from=datetime(2025, 1, 1, tzinfo=UTC),
             input_to=datetime(2026, 1, 1, tzinfo=UTC)),
    DRangeTC(input_from=datetime(2025, 1, 1, 23, 0, 0, tzinfo=UTC),
             input_to=datetime(2026, 1, 1, 23, 0, 0, tzinfo=UTC)),
    DRangeTC(input_from=datetime(2025, 1, 1, 22, 0, 0, tzinfo=UTC),
             input_to=datetime(2025, 1, 1, 23, 0, 0, tzinfo=UTC)),
    DRangeTC(id='both values, different timezones',
             input_from=datetime(2025, 1, 1, tzinfo=UTC),
             input_to=datetime(2025, 1, 1, tzinfo=ZoneInfo('America/Argentina/Buenos_Aires'))),
    DRangeTC(input_from=datetime(2025, 1, 1, 23, 0, 0, tzinfo=UTC),
             input_to=datetime(2025, 1, 1, 23, 0, 0, tzinfo=ZoneInfo('America/Argentina/Buenos_Aires'))),
    DRangeTC(input_from=datetime(2025, 1, 1, 19, 0, 0, tzinfo=ZoneInfo('America/Argentina/Buenos_Aires')),
             input_to=datetime(2025, 1, 1, 23, 0, 0, tzinfo=UTC)),
]])
def test_instantiation_success(test_case: DateRangeTestCase):
    computed_output = DateRange(fm=test_case.input_from, to=test_case.input_to)
    assert computed_output.fm == test_case.input_from
    assert computed_output.to == test_case.input_to
    if None not in [computed_output.fm, computed_output.to]:
        assert computed_output.fm <= computed_output.to


@pytest.mark.parametrize('test_case', [pytest.param(test_case, id=test_case.id) for test_case in [
    DRangeTC(id='invalid range (inverted), offset-naive datetimes',
             input_from=datetime(2025, 1, 2),
             input_to=datetime(2025, 1, 1), expected_exception=InvalidRange),
    DRangeTC(input_from=datetime(2025, 2, 1),
             input_to=datetime(2025, 1, 1), expected_exception=InvalidRange),
    DRangeTC(input_from=datetime(2026, 1, 1),
             input_to=datetime(2025, 1, 1), expected_exception=InvalidRange),
    DRangeTC(input_from=datetime(2026, 1, 1, 23, 0, 0),
             input_to=datetime(2025, 1, 1, 23, 0, 0),
             expected_exception=InvalidRange),
    DRangeTC(input_from=datetime(2025, 1, 1, 23, 0, 0),
             input_to=datetime(2025, 1, 1, 22, 0, 0),
             expected_exception=InvalidRange),
    DRangeTC(id='invalid range (inverted), offset-aware datetimes',
             input_from=datetime(2025, 1, 2, tzinfo=UTC),
             input_to=datetime(2025, 1, 1, tzinfo=UTC), expected_exception=InvalidRange),
    DRangeTC(input_from=datetime(2025, 2, 1, tzinfo=UTC),
             input_to=datetime(2025, 1, 1, tzinfo=UTC), expected_exception=InvalidRange),
    DRangeTC(input_from=datetime(2026, 1, 1, tzinfo=UTC),
             input_to=datetime(2025, 1, 1, tzinfo=UTC), expected_exception=InvalidRange),
    DRangeTC(input_from=datetime(2025, 1, 1, tzinfo=ZoneInfo('America/Argentina/Buenos_Aires')),
             input_to=datetime(2025, 1, 1, tzinfo=UTC), expected_exception=InvalidRange),
    DRangeTC(input_from=datetime(2026, 1, 1, 23, 0, 0, tzinfo=UTC),
             input_to=datetime(2025, 1, 1, 23, 0, 0, tzinfo=UTC),
             expected_exception=InvalidRange),
    DRangeTC(input_from=datetime(2025, 1, 1, 23, 0, 0, tzinfo=UTC),
             input_to=datetime(2025, 1, 1, 22, 0, 0, tzinfo=UTC),
             expected_exception=InvalidRange),
    DRangeTC(input_from=datetime(2025, 1, 1, 23, 0, 0, tzinfo=ZoneInfo('America/Argentina/Buenos_Aires')),
             input_to=datetime(2025, 1, 1, 23, 0, 0, tzinfo=UTC),
             expected_exception=InvalidRange),
    DRangeTC(id='mixing datetime offsets',
             input_from=datetime(2025, 1, 2, tzinfo=UTC),
             input_to=datetime(2025, 1, 1), expected_exception=TypeError),
    DRangeTC(input_from=datetime(2025, 2, 1),
             input_to=datetime(2025, 1, 1, tzinfo=UTC), expected_exception=TypeError),
]])
def test_instantiation_failure(test_case: DateRangeTestCase):
    with pytest.raises(test_case.expected_exception):
        DateRange(fm=test_case.input_from, to=test_case.input_to)


@dataclass
class ReprDateRangeTestCase(BaseTestCase):
    expected_output: str
    input_from: Optional[datetime] = None
    input_to: Optional[datetime] = None


RDRangeTC = ReprDateRangeTestCase


@pytest.mark.parametrize('test_case', [pytest.param(test_case, id=test_case.id) for test_case in [
    RDRangeTC(id='no values',
              expected_output='DateRange(fm=None, to=None)'),
    RDRangeTC(id='"from" value only, offset-naive datetimes',
              input_from=datetime(2025, 1, 1),
              expected_output=f'DateRange(fm={datetime(2025, 1, 1)}, to=None)'),
    RDRangeTC(input_from=datetime(2025, 1, 1, 23, 0, 0),
              expected_output=f'DateRange(fm={datetime(2025, 1, 1, 23, 0, 0)}, to=None)'),
    RDRangeTC(id='"from" value only, offset-aware datetimes',
              input_from=datetime(2025, 1, 1, tzinfo=UTC),
              expected_output=f'DateRange(fm={datetime(2025, 1, 1, tzinfo=UTC)}, to=None)'),
    RDRangeTC(input_from=datetime(2025, 1, 1, 23, 0, 0, tzinfo=UTC),
              expected_output=f'DateRange(fm={datetime(2025, 1, 1, 23, 0, 0, tzinfo=UTC)}, to=None)'),
    RDRangeTC(id='"to" value only, offset-naive datetimes',
              input_to=datetime(2025, 1, 1),
              expected_output=f'DateRange(fm=None, to={datetime(2025, 1, 1)})'),
    RDRangeTC(input_to=datetime(2025, 1, 1, 23, 0, 0),
              expected_output=f'DateRange(fm=None, to={datetime(2025, 1, 1, 23, 0, 0)})'),
    RDRangeTC(id='"to" value only, offset-aware datetimes',
              input_to=datetime(2025, 1, 1, tzinfo=UTC),
              expected_output=f'DateRange(fm=None, to={datetime(2025, 1, 1, tzinfo=UTC)})'),
    RDRangeTC(input_to=datetime(2025, 1, 1, 23, 0, 0, tzinfo=UTC),
              expected_output=f'DateRange(fm=None, to={datetime(2025, 1, 1, 23, 0, 0, tzinfo=UTC)})'),
    RDRangeTC(id='both values, offset-naive datetimes',
              input_from=datetime(2025, 1, 1), input_to=datetime(2025, 1, 2),
              expected_output=f'DateRange(fm={datetime(2025, 1, 1)}, to={datetime(2025, 1, 2)})'),
    RDRangeTC(input_from=datetime(2025, 1, 1, 22, 0, 0),
              input_to=datetime(2025, 1, 1, 23, 0, 0),
              expected_output=f'DateRange(fm={datetime(2025, 1, 1, 22, 0, 0)}, to={datetime(2025, 1, 1, 23, 0, 0)})'),
    RDRangeTC(id='both values, offset-aware datetimes',
              input_from=datetime(2025, 1, 1, tzinfo=UTC),
              input_to=datetime(2025, 1, 2, tzinfo=UTC),
              expected_output=f'DateRange(fm={datetime(2025, 1, 1, tzinfo=UTC)}, to={datetime(2025, 1, 2, tzinfo=UTC)})'),
    RDRangeTC(input_from=datetime(2025, 1, 1, 22, 0, 0, tzinfo=UTC),
              input_to=datetime(2025, 1, 1, 23, 0, 0, tzinfo=UTC),
              expected_output=f'DateRange(fm={datetime(2025, 1, 1, 22, 0, 0, tzinfo=UTC)}, to={datetime(2025, 1, 1, 23, 0, 0, tzinfo=UTC)})'),
]])
def test_repr_success(test_case: ReprDateRangeTestCase):
    computed_output = DateRange(fm=test_case.input_from, to=test_case.input_to)
    assert str(computed_output) == test_case.expected_output


@dataclass
class CmpDateRangeTestCase(BaseTestCase):
    first_input: DateRange
    second_input: DateRange


CDRangeTC = CmpDateRangeTestCase


@pytest.mark.parametrize('test_case', [pytest.param(test_case, id=test_case.id) for test_case in [
    CDRangeTC(id='no values',
              first_input=DateRange(), second_input=DateRange()),
    CDRangeTC(first_input=DateRange(fm=None), second_input=DateRange()),
    CDRangeTC(first_input=DateRange(to=None), second_input=DateRange()),
    CDRangeTC(first_input=DateRange(fm=None, to=None), second_input=DateRange()),
    CDRangeTC(id='"from" value only, offset-naive datetimes',
              first_input=DateRange(fm=datetime(2025, 1, 1)),
              second_input=DateRange(fm=datetime(2025, 1, 1))),
    CDRangeTC(first_input=DateRange(fm=datetime(2025, 1, 1), to=None),
              second_input=DateRange(fm=datetime(2025, 1, 1))),
    CDRangeTC(id='"from" value only, offset-aware datetimes',
              first_input=DateRange(fm=datetime(2025, 1, 1, tzinfo=UTC)),
              second_input=DateRange(fm=datetime(2025, 1, 1, tzinfo=UTC))),
    CDRangeTC(first_input=DateRange(fm=datetime(2025, 1, 1, tzinfo=UTC), to=None),
              second_input=DateRange(fm=datetime(2025, 1, 1, tzinfo=UTC))),
    CDRangeTC(id='"to" value only, offset-naive datetimes',
              first_input=DateRange(to=datetime(2025, 1, 1)),
              second_input=DateRange(to=datetime(2025, 1, 1))),
    CDRangeTC(first_input=DateRange(fm=None, to=datetime(2025, 1, 1)),
              second_input=DateRange(to=datetime(2025, 1, 1))),
    CDRangeTC(id='"to" value only, offset-aware datetimes',
              first_input=DateRange(to=datetime(2025, 1, 1, tzinfo=UTC)),
              second_input=DateRange(to=datetime(2025, 1, 1, tzinfo=UTC))),
    CDRangeTC(first_input=DateRange(fm=None, to=datetime(2025, 1, 1, tzinfo=UTC)),
              second_input=DateRange(to=datetime(2025, 1, 1, tzinfo=UTC))),
    CDRangeTC(id='both values, offset-naive datetimes',
              first_input=DateRange(fm=datetime(2025, 1, 1),
                                    to=datetime(2025, 1, 1)),
              second_input=DateRange(fm=datetime(2025, 1, 1),
                                     to=datetime(2025, 1, 1))),
    CDRangeTC(first_input=DateRange(fm=datetime(2025, 1, 1),
                                    to=datetime(2025, 1, 2)),
              second_input=DateRange(fm=datetime(2025, 1, 1),
                                     to=datetime(2025, 1, 2))),
    CDRangeTC(id='both values, offset-aware datetimes',
              first_input=DateRange(fm=datetime(2025, 1, 1, tzinfo=UTC),
                                    to=datetime(2025, 1, 1, tzinfo=UTC)),
              second_input=DateRange(fm=datetime(2025, 1, 1, tzinfo=UTC),
                                     to=datetime(2025, 1, 1, tzinfo=UTC))),
    CDRangeTC(first_input=DateRange(fm=datetime(2025, 1, 1, tzinfo=UTC),
                                    to=datetime(2025, 1, 2, tzinfo=UTC)),
              second_input=DateRange(fm=datetime(2025, 1, 1, tzinfo=UTC),
                                     to=datetime(2025, 1, 2, tzinfo=UTC))),
    CDRangeTC(id='both values, different timezones',
              first_input=DateRange(fm=datetime(2025, 1, 1, 20, 0, 0, tzinfo=ZoneInfo('America/Argentina/Buenos_Aires')),
                                    to=datetime(2025, 1, 1, 23, 0, 0, tzinfo=UTC)),
              second_input=DateRange(fm=datetime(2025, 1, 1, 23, 0, 0, tzinfo=UTC),
                                     to=datetime(2025, 1, 1, 23, 0, 0, tzinfo=UTC))),
    CDRangeTC(first_input=DateRange(fm=datetime(2025, 1, 1, 20, 0, 0, tzinfo=ZoneInfo('America/Argentina/Buenos_Aires')),
                                    to=datetime(2025, 1, 1, 20, 0, 0, tzinfo=ZoneInfo('America/Argentina/Buenos_Aires'))),
              second_input=DateRange(fm=datetime(2025, 1, 1, 23, 0, 0, tzinfo=UTC),
                                     to=datetime(2025, 1, 1, 23, 0, 0, tzinfo=UTC))),
]])
def test_cmp_success(test_case: CmpDateRangeTestCase):
    assert test_case.first_input == test_case.second_input
