import logging

import pytest

from m3t_MultiRotatingLogger import MultiRotatingLogger, UnavailableNameException
from m3t_Utils import ExpectedTypeException, ExpectedKeyException, MinimumLengthException


def get_existent_loggers():
    return [name for name in logging.root.manager.loggerDict.keys()]


@pytest.mark.parametrize('configs,expected_exception', [
    ('aaa', ExpectedTypeException()),
    ({'name': 'asdf'}, ExpectedTypeException()),
    (['aaa'], ExpectedTypeException()),
    ([{}], ExpectedKeyException()),
    ([{}, {}], ExpectedKeyException()),
    ([{'name': 1234}], ExpectedTypeException()),
    ([{}, {'name': 'asdf'}], ExpectedKeyException()),
    ([{'name': ''}, {'name': 'asdf'}], MinimumLengthException()),
    ([{'name': 'asdf'}, {'name': ['a', 's', 'd']}], ExpectedTypeException()),
])
def test_instantiation_failure(configs, expected_exception):
    try:
        MultiRotatingLogger(configs)
    except (ExpectedTypeException, ExpectedKeyException, MinimumLengthException) as current_exception:
        assert isinstance(current_exception, type(expected_exception))
    else:
        pytest.fail(f'Exception \"{type(expected_exception).__name__}\" was expected, but found none')


@pytest.mark.parametrize('logger_names', [
    (['a']),
    (['aa']),
    (['aaa', 'b']),
    (('aaaa', 'bb')),
])
def test_instantiation_success(logger_names):
    MultiRotatingLogger([{'name': name} for name in logger_names])
    for name in logger_names:
        assert name in get_existent_loggers()


@pytest.mark.parametrize('logger_name', [
    ('a111'),
    ('b_2_2_2'),
    ('c.3.3.3'),
])
def test_logger_override_exception(logger_name):
    try:
        logging.getLogger(logger_name)
        MultiRotatingLogger([{'name': logger_name}])
    except UnavailableNameException as current_exception:
        assert isinstance(current_exception, type(UnavailableNameException()))
    else:
        pytest.fail(f'Exception \"{type(UnavailableNameException()).__name__}\" was expected, but found none')
