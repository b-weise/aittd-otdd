from collections.abc import Callable
from dataclasses import dataclass
from datetime import datetime
from pathlib import Path
from typing import Any

import pandas
import pytest

from source.libs.baseTestCase import BaseTestCase
from source.libs.helper import Helper


@dataclass
class GetFullyQualifiedNameMethodTestCase(BaseTestCase):
    input_value: Callable
    expected_output: str


GFQNameMethTC = GetFullyQualifiedNameMethodTestCase


@pytest.mark.parametrize('test_case', [pytest.param(test_case, id=test_case.id) for test_case in [
    GFQNameMethTC(input_value=divmod, expected_output='builtins.divmod'),
    GFQNameMethTC(input_value=min, expected_output='builtins.min'),
    GFQNameMethTC(input_value=BaseTestCase, expected_output='source.libs.baseTestCase.BaseTestCase'),
    GFQNameMethTC(input_value=Helper, expected_output='source.libs.helper.Helper'),
    GFQNameMethTC(input_value=pandas.DataFrame, expected_output='pandas.core.frame.DataFrame'),
    GFQNameMethTC(input_value=pandas.Series, expected_output='pandas.core.series.Series'),
]])
def test_get_fully_qualified_name_success(test_case: GetFullyQualifiedNameMethodTestCase):
    computed_output = Helper.get_fully_qualified_name(test_case.input_value)
    assert computed_output == test_case.expected_output


@dataclass
class GetModuleCallableMethodTestCase(BaseTestCase):
    input_value: str
    expected_output: Callable | None


GMCallableMethTC = GetModuleCallableMethodTestCase


@pytest.mark.parametrize('test_case', [pytest.param(test_case, id=test_case.id) for test_case in [
    GMCallableMethTC(id='found callables',
                     input_value='builtins.divmod', expected_output=divmod),
    GMCallableMethTC(input_value='builtins.min', expected_output=min),
    GMCallableMethTC(input_value='source.libs.baseTestCase.BaseTestCase', expected_output=BaseTestCase),
    GMCallableMethTC(input_value='source.libs.helper.Helper', expected_output=Helper),
    GMCallableMethTC(input_value='pandas.core.frame.DataFrame', expected_output=pandas.DataFrame),
    GMCallableMethTC(input_value='pandas.core.series.Series', expected_output=pandas.Series),
    GMCallableMethTC(id='installed module as input',
                     input_value='pandas', expected_output=None),
    GMCallableMethTC(input_value='pytest', expected_output=None),
    GMCallableMethTC(id='non-installed module as input',
                     input_value='scrapy', expected_output=None),
    GMCallableMethTC(input_value='aaaaaa', expected_output=None),
]])
def test_get_module_callable_success(test_case: GetModuleCallableMethodTestCase):
    computed_output = Helper.get_module_callable(test_case.input_value)
    assert computed_output == test_case.expected_output


@dataclass
class StringifyObjectsMethodTestCase(BaseTestCase):
    input_value: Any
    expected_output: Any


SObjectsMethTC = StringifyObjectsMethodTestCase


@pytest.mark.parametrize('test_case', [pytest.param(test_case, id=test_case.id) for test_case in [
    SObjectsMethTC(input_value=divmod, expected_output='builtins.divmod'),
    SObjectsMethTC(input_value=123, expected_output=123),
    SObjectsMethTC(input_value='aaa', expected_output='aaa'),
    SObjectsMethTC(input_value=Path('aaa'), expected_output='aaa'),
    SObjectsMethTC(input_value=datetime(2025, 12, 1, 00, 00, 00),
                   expected_output='2025-12-01 00:00:00'),
    SObjectsMethTC(input_value=['aaa'], expected_output=['aaa']),
    SObjectsMethTC(input_value=['a', 'b', 'c'], expected_output=['a', 'b', 'c']),
    SObjectsMethTC(input_value=['a', 1, divmod], expected_output=['a', 1, 'builtins.divmod']),
    SObjectsMethTC(input_value=('a', 1, divmod), expected_output=['a', 1, 'builtins.divmod']),
    SObjectsMethTC(input_value={'aaa': 'abcdef'}, expected_output={'aaa': 'abcdef'}),
    SObjectsMethTC(input_value={'aaa': 1}, expected_output={'aaa': 1}),
    SObjectsMethTC(input_value={'aaa': divmod}, expected_output={'aaa': 'builtins.divmod'}),
    SObjectsMethTC(input_value={'aaa': 'abcdef', 'bbb': 123, 'ccc': divmod},
                   expected_output={'aaa': 'abcdef', 'bbb': 123, 'ccc': 'builtins.divmod'}),
    SObjectsMethTC(input_value=[('a', 'b', 'c')], expected_output=[['a', 'b', 'c']]),
    SObjectsMethTC(input_value=[('a', 1, {'aaa': divmod})], expected_output=[['a', 1, {'aaa': 'builtins.divmod'}]]),
    SObjectsMethTC(input_value={'aaa': divmod, 'ccc': [(1, min), (2, max)]},
                   expected_output={'aaa': 'builtins.divmod', 'ccc': [[1, 'builtins.min'], [2, 'builtins.max']]}),
    SObjectsMethTC(input_value={'aaa': divmod,
                                'ccc': [(datetime(2025, 12, 1), min),
                                        (Path('zxcv'), max)],
                                },
                   expected_output={'aaa': 'builtins.divmod',
                                    'ccc': [['2025-12-01 00:00:00', 'builtins.min'],
                                            ['zxcv', 'builtins.max']],
                                    }),
]])
def test_stringify_objects_success(test_case: StringifyObjectsMethodTestCase):
    computed_output = Helper.stringify_objects(test_case.input_value)
    assert computed_output == test_case.expected_output
