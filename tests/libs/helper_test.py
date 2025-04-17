from collections.abc import Callable
from dataclasses import dataclass

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
