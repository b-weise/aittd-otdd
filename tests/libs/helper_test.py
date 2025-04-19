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
    GFQNameMethTC(id='builtin functions',
                  input_value=divmod, expected_output='builtins.divmod'),
    GFQNameMethTC(input_value=min, expected_output='builtins.min'),
    GFQNameMethTC(id='installed classes',
                  input_value=pandas.DataFrame, expected_output='pandas.core.frame.DataFrame'),
    GFQNameMethTC(input_value=pandas.Series, expected_output='pandas.core.series.Series'),
    GFQNameMethTC(id='custom classes',
                  input_value=BaseTestCase, expected_output='source.libs.baseTestCase.BaseTestCase'),
    GFQNameMethTC(input_value=Helper, expected_output='source.libs.helper.Helper'),
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
    GMCallableMethTC(id='builtin functions',
                     input_value='builtins.divmod', expected_output=divmod),
    GMCallableMethTC(input_value='builtins.min', expected_output=min),
    GMCallableMethTC(id='installed classes',
                     input_value='pandas.core.frame.DataFrame', expected_output=pandas.DataFrame),
    GMCallableMethTC(input_value='pandas.core.series.Series', expected_output=pandas.Series),
    GMCallableMethTC(id='custom classes',
                     input_value='source.libs.baseTestCase.BaseTestCase', expected_output=BaseTestCase),
    GMCallableMethTC(input_value='source.libs.helper.Helper', expected_output=Helper),
    GMCallableMethTC(id='installed modules',
                     input_value='pandas', expected_output=None),
    GMCallableMethTC(input_value='pytest', expected_output=None),
    GMCallableMethTC(id='non-installed modules',
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
    SObjectsMethTC(id='single values',
                   input_value=divmod, expected_output='builtins.divmod'),
    SObjectsMethTC(input_value=123, expected_output=123),
    SObjectsMethTC(input_value='aaa', expected_output='aaa'),
    SObjectsMethTC(input_value=Path('aaa'), expected_output='aaa'),
    SObjectsMethTC(input_value=datetime(2025, 12, 1, 00, 00, 00),
                   expected_output='2025-12-01 00:00:00'),
    SObjectsMethTC(id='flat sequences',
                   input_value=['aaa'], expected_output=['aaa']),
    SObjectsMethTC(input_value=[], expected_output=[]),
    SObjectsMethTC(input_value=['a', 'b', 'c'], expected_output=['a', 'b', 'c']),
    SObjectsMethTC(input_value=['a', 1, divmod], expected_output=['a', 1, 'builtins.divmod']),
    SObjectsMethTC(id='flat dicts',
                   input_value={'aaa': 'abcdef'}, expected_output={'aaa': 'abcdef'}),
    SObjectsMethTC(input_value={}, expected_output={}),
    SObjectsMethTC(input_value={'aaa': 1}, expected_output={'aaa': 1}),
    SObjectsMethTC(input_value={'aaa': divmod}, expected_output={'aaa': 'builtins.divmod'}),
    SObjectsMethTC(input_value={'aaa': 'abcdef', 'bbb': 123, 'ccc': divmod},
                   expected_output={'aaa': 'abcdef', 'bbb': 123, 'ccc': 'builtins.divmod'}),
    SObjectsMethTC(id='composed sequences',
                   input_value=[('a', 'b', 'c')], expected_output=[['a', 'b', 'c']]),
    SObjectsMethTC(input_value=[1, (1, [1])], expected_output=[1, [1, [1]]]),
    SObjectsMethTC(input_value=[('a', 1, {'a': divmod})], expected_output=[['a', 1, {'a': 'builtins.divmod'}]]),
    SObjectsMethTC(id='composed dicts',
                   input_value={'aaa': divmod, 'bbb': [(1, min), (2, max)]},
                   expected_output={'aaa': 'builtins.divmod', 'bbb': [[1, 'builtins.min'], [2, 'builtins.max']]}),
    SObjectsMethTC(input_value={'a': {'a': {'a': 'a'}}}, expected_output={'a': {'a': {'a': 'a'}}}),
    SObjectsMethTC(input_value={'a': {'a': {'a': min}}}, expected_output={'a': {'a': {'a': 'builtins.min'}}}),
    SObjectsMethTC(input_value={'aaa': divmod, 'bbb': [(datetime(2025, 12, 1), min),
                                                       (Path('zxcv'), max)]},
                   expected_output={'aaa': 'builtins.divmod', 'bbb': [['2025-12-01 00:00:00', 'builtins.min'],
                                                                      ['zxcv', 'builtins.max']]}),
]])
def test_stringify_objects_success(test_case: StringifyObjectsMethodTestCase):
    computed_output = Helper.stringify_objects(test_case.input_value)
    assert computed_output == test_case.expected_output


@dataclass
class GenerateHashMethodTestCase(BaseTestCase):
    input_value: Any
    expected_output: str


GHashMethTC = GenerateHashMethodTestCase


@pytest.mark.parametrize('test_case', [pytest.param(test_case, id=test_case.id) for test_case in [
    GHashMethTC(id='single values',
                input_value=1, expected_output='c4ca4238a0b923820dcc509a6f75849b'),
    GHashMethTC(input_value='aaa', expected_output='47bce5c74f589f4867dbd57e9ca9f808'),
    GHashMethTC(input_value=divmod, expected_output='62075ad595011ae3be48e3ba87dbd420'),
    GHashMethTC(input_value=Path('zxcv'), expected_output='fd2cc6c54239c40495a0d3a93b6380eb'),
    GHashMethTC(input_value=datetime(2025, 12, 1),
                expected_output='1b265553d8a80a08c00d05c0ca492190'),
    GHashMethTC(id='empty containers',
                input_value=[], expected_output='d41d8cd98f00b204e9800998ecf8427e'),
    GHashMethTC(input_value=tuple(), expected_output='d41d8cd98f00b204e9800998ecf8427e'),
    GHashMethTC(input_value={}, expected_output='d41d8cd98f00b204e9800998ecf8427e'),
    GHashMethTC(id='flat containers',
                input_value=['aaa', 1], expected_output='8a90ab46ccc884f407709753cea8619d'),
    GHashMethTC(input_value={'aaa': 1}, expected_output='d12d1b9751066cbd862bd6f430b0f27b'),
    GHashMethTC(input_value=['aaa', divmod], expected_output='70dcd2bf52d9f38c26b3e84d372fad6a'),
    GHashMethTC(input_value={'aaa': divmod}, expected_output='aeb4251352a3d82646a14cb88fd25be1'),
    GHashMethTC(id='composed containers',
                input_value=[['aaa', 1]], expected_output='8a90ab46ccc884f407709753cea8619d'),
    GHashMethTC(input_value={'aaa': {'aaa': 1}}, expected_output='10a5fb55ee790622df2806b66b541e4c'),
    GHashMethTC(input_value=[['aaa', divmod]], expected_output='70dcd2bf52d9f38c26b3e84d372fad6a'),
    GHashMethTC(input_value={'aaa': {'aaa': divmod}}, expected_output='9457b4d45c928d098c4dc99410817ec7'),
    GHashMethTC(input_value=['a', ['b', ['c', 1]]], expected_output='fa62943ab85bdd68ff3326c5205b6ab0'),
    GHashMethTC(id='flat containers, same items, different top order',
                input_value=['a', 'b', 'c'], expected_output='a44c56c8177e32d3613988f4dba7962e'),
    GHashMethTC(input_value=['c', 'a', 'b'], expected_output='a44c56c8177e32d3613988f4dba7962e'),
    GHashMethTC(input_value=['b', 'c', 'a'], expected_output='a44c56c8177e32d3613988f4dba7962e'),
    GHashMethTC(input_value={'a': 111, 'b': 222}, expected_output='e615702983954eb9581a7a7b48fc0b83'),
    GHashMethTC(input_value={'b': 222, 'a': 111}, expected_output='e615702983954eb9581a7a7b48fc0b83'),
    GHashMethTC(input_value={0: 'aaa', 1: 'bbb'}, expected_output='8520111418b0c399d274a4a300708efa'),
    GHashMethTC(input_value={1: 'bbb', 0: 'aaa'}, expected_output='8520111418b0c399d274a4a300708efa'),
    GHashMethTC(id='composed containers, same items, different top order',
                input_value={'a': Path('zxcv'),
                             'b': [111, 222],
                             'c': {0: ('aaa', max), 1: ('bbb', min)}},
                expected_output='7dabfd61c0280fba729895415e99b90c'),
    GHashMethTC(input_value={'c': {0: ('aaa', max), 1: ('bbb', min)},
                             'a': Path('zxcv'),
                             'b': [111, 222]},
                expected_output='7dabfd61c0280fba729895415e99b90c'),
    GHashMethTC(input_value={'b': [111, 222],
                             'c': {0: ('aaa', max), 1: ('bbb', min)},
                             'a': Path('zxcv')},
                expected_output='7dabfd61c0280fba729895415e99b90c'),
    GHashMethTC(id='composed containers, same items, different bottom order',
                input_value={'a': Path('zxcv'),
                             'b': [111, 222],
                             'c': {0: (max, 'aaa'), 1: (min, 'bbb')}},
                expected_output='7dabfd61c0280fba729895415e99b90c'),
    GHashMethTC(input_value={'a': Path('zxcv'),
                             'b': [111, 222],
                             'c': {1: (min, 'bbb'), 0: (max, 'aaa')}},
                expected_output='7dabfd61c0280fba729895415e99b90c'),
    GHashMethTC(input_value={'a': Path('zxcv'),
                             'b': [222, 111],
                             'c': {1: (min, 'bbb'), 0: (max, 'aaa')}},
                expected_output='7dabfd61c0280fba729895415e99b90c'),
]])
def test_generate_hash_success(test_case: GenerateHashMethodTestCase):
    computed_output = Helper.generate_hash(test_case.input_value)
    assert computed_output == test_case.expected_output
