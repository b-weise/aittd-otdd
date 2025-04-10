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
    GFQNameMethTC(input_value=divmod,
                  expected_output='builtins.divmod'),
    GFQNameMethTC(input_value=min,
                  expected_output='builtins.min'),
    GFQNameMethTC(input_value=BaseTestCase,
                  expected_output='source.libs.baseTestCase.BaseTestCase'),
    GFQNameMethTC(input_value=Helper,
                  expected_output='source.libs.helper.Helper'),
    GFQNameMethTC(input_value=pandas.DataFrame,
                  expected_output='pandas.core.frame.DataFrame'),
    GFQNameMethTC(input_value=pandas.Series,
                  expected_output='pandas.core.series.Series'),
]])
def test_get_fully_qualified_name_success(test_case: GetFullyQualifiedNameMethodTestCase):
    computed_output = Helper.get_fully_qualified_name(test_case.input_value)
    assert computed_output == test_case.expected_output
