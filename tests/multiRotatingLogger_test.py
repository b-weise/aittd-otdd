import logging
import sys
import dataclasses
from dataclasses import dataclass
import pytest

from typing import Any
from BaseTestCase import BaseTestCase
from MultiRotatingLogger import MultiRotatingLogger, UnavailableNameException, EmptyNameException
from Utils import MandatoryTypeException

from dacite.exceptions import MissingValueError, WrongTypeError


def get_existent_loggers() -> list[str]:
    """
    Generates a list of names corresponding to the loggers present in the current runtime.
    :return: A list of logger names.
    """
    return [name for name in logging.root.manager.loggerDict.keys()]


@dataclass
class InstantiationTestCase(BaseTestCase):
    configs: Any = None


InstTC = InstantiationTestCase


@pytest.mark.parametrize('test_case', [pytest.param(test_case, id=test_case.id) for test_case in [
    InstTC(id='wrong configs type',
           configs='aaa', expected_exception=MandatoryTypeException),
    InstTC(configs={'name': 'asdf'}, expected_exception=MandatoryTypeException),
    InstTC(configs=['aaa'], expected_exception=MandatoryTypeException),
    InstTC(id='no mandatory keys',
           configs=[{}], expected_exception=MissingValueError),
    InstTC(configs=[{}, {}], expected_exception=MissingValueError),
    InstTC(configs=[{'aaa': 111}, {'bbb': 222}], expected_exception=MissingValueError),
    InstTC(configs=[{'name': 'qwer'}, {'aaa': 'zxcv'}], expected_exception=MissingValueError),
    InstTC(id='wrong mandatory key value type',
           configs=[{'name': 1234}], expected_exception=WrongTypeError),
    InstTC(configs=[{'name': 'asdf'}, {'name': ['a', 's', 'd']}], expected_exception=WrongTypeError),
    InstTC(id='empty name',
           configs=[{'name': ''}], expected_exception=EmptyNameException),
]])
def test_instantiation_failure(test_case: InstantiationTestCase):
    try:
        MultiRotatingLogger(test_case.configs)
    except:
        assert isinstance(sys.exception(), test_case.expected_exception)
    else:
        pytest.fail(f'Exception \"{test_case.expected_exception.__name__}\" was expected, but found none')


@pytest.mark.parametrize('test_case', [pytest.param(test_case, id=test_case.id) for test_case in [
    InstTC(configs=[{'name': 'a'}]),
    InstTC(configs=[{'name': 'aaa'}, {'name': 'bbb'}]),
]])
def test_instantiation_success(test_case: InstantiationTestCase):
    MultiRotatingLogger(test_case.configs)
    for name in map(lambda config: config['name'], test_case.configs):
        assert name in get_existent_loggers()


@pytest.mark.parametrize('test_case', [pytest.param(test_case, id=test_case.id) for test_case in [
    InstTC(configs=[{'name': 'aaa111'}], expected_exception=UnavailableNameException),
    InstTC(configs=[{'name': 'bbb_222'}], expected_exception=UnavailableNameException),
    InstTC(configs=[{'name': 'ccc.333'}], expected_exception=UnavailableNameException),
]])
def test_logger_override_exception(test_case: InstantiationTestCase):
    try:
        logging.getLogger(test_case.configs[0]['name'])
        MultiRotatingLogger(test_case.configs)
    except:
        assert isinstance(sys.exception(), test_case.expected_exception)
    else:
        pytest.fail(f'Exception \"{test_case.expected_exception.__name__}\" was expected, but found none')
