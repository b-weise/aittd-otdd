import pytest

from m3t_MultiRotatingLogger import MultiRotatingLogger
from m3t_Utils import ExpectedTypeException, ExpectedKeyException, MinimumLengthException


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


@pytest.mark.parametrize('configs', [
    ([{'name': 'a'}]),
    ([{'name': 'name_test_000'}]),
    ([{'name': 'name_test_000'}, {'name': 'name_test_001'}]),
    (({'name': 'name_test_000'}, {'name': 'name_test_001'})),
])
def test_instantiation_success(configs):
    MultiRotatingLogger(configs)
