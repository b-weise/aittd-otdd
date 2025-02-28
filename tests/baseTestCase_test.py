from typing import Optional, Type

import pytest

from baseTestCase import BaseTestCase


@pytest.fixture
def new_instance() -> BaseTestCase:
    return BaseTestCase()


def test_instantiation_success(new_instance: BaseTestCase):
    assert isinstance(new_instance, BaseTestCase)


def test_id_unset_success(new_instance: BaseTestCase):
    assert new_instance.id is None


def test_expected_exception_unset_success(new_instance: BaseTestCase):
    assert new_instance.expected_exception is None


@pytest.mark.parametrize('input_value,expected_output', [
    pytest.param(None, None),
    pytest.param('', None),
    pytest.param(1234, None),
    pytest.param('1234', '--- 1234 ---'),
    pytest.param('a', '--- A ---'),
    pytest.param('abcd', '--- ABCD ---'),
    pytest.param('ABCD', '--- ABCD ---'),
    pytest.param('aa bb cc', '--- AA BB CC ---'),
    pytest.param('aa-bb-cc', '--- AA-BB-CC ---'),
    pytest.param('aa.bb.cc', '--- AA.BB.CC ---'),
])
def test_id_success(input_value: Optional[str], expected_output: Optional[str]):
    instance = BaseTestCase(id=input_value)
    assert instance.id == expected_output


@pytest.mark.parametrize('input_value,expected_output', [
    pytest.param(None, None),
    pytest.param(TypeError, TypeError),
    pytest.param(FileNotFoundError, FileNotFoundError),
    pytest.param(AssertionError, AssertionError),
])
def test_expected_exception_success(input_value: Optional[Type[Exception]],
                                    expected_output: Optional[Type[Exception]]):
    instance = BaseTestCase(expected_exception=input_value)
    assert instance.expected_exception is expected_output
