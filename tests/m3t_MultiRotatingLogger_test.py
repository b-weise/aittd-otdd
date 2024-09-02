import pytest

from m3t_MultiRotatingLogger import MultiRotatingLogger
from m3t_Utils import InvalidTypeException, InvalidLengthException, KeyExistenceException


@pytest.mark.parametrize('configs,expected_exception', [
    ('aaa', InvalidTypeException()),
    ({'name': 'asdf'}, InvalidTypeException()),
    (['aaa'], InvalidTypeException()),
    ([{}], KeyExistenceException()),
    ([{}, {}], KeyExistenceException()),
    ([{'name': 1234}], InvalidTypeException()),
    ([{}, {'name': 'asdf'}], KeyExistenceException()),
    ([{'name': ''}, {'name': 'asdf'}], InvalidLengthException()),
    ([{'name': 'asdf'}, {'name': ['a', 's', 'd']}], InvalidTypeException()),
])
def test_instantiation_failure(configs, expected_exception):
    try:
        MultiRotatingLogger(configs)
    except (InvalidTypeException, InvalidLengthException, KeyExistenceException) as current_exception:
        assert isinstance(current_exception, type(expected_exception))
    else:
        pytest.fail(f'Exception \"{type(expected_exception).__name__}\" was expected, but found none')


@pytest.mark.parametrize('configs', [
    ([{'name': 'name_test_000'}]),
    ([{'name': 'name_test_000'}, {'name': 'name_test_001'}]),
])
def test_instantiation_success(configs):
    MultiRotatingLogger(configs)
