import pytest
from m3t_MultiRotatingLogger import MultiRotatingLogger, InvalidConfigsException, UnavailableNameException


@pytest.fixture
def new_instance():
    return MultiRotatingLogger()


@pytest.mark.parametrize('configs,expected_exception', [
    ([], InvalidConfigsException()),
    ('aaa', InvalidConfigsException()),
    (123, InvalidConfigsException()),
    ({}, InvalidConfigsException()),
    ({'name': 'asdf'}, InvalidConfigsException()),
    (['aaa'], InvalidConfigsException()),
    ([123], InvalidConfigsException()),
    ([{}], InvalidConfigsException()),
    ([{}, 1234], InvalidConfigsException()),
    ([{}, 'asdf'], InvalidConfigsException()),
    ([{}, {}], InvalidConfigsException()),
    ([{'name': 1234}], InvalidConfigsException()),
    ([{'name': {}}], InvalidConfigsException()),
    ([{'name': [1, 2, 3]}], InvalidConfigsException()),
    ([{}, {'name': 'asdf'}], InvalidConfigsException()),
    ([{'name': 'asdf'}, {'name': ['a', 's', 'd']}], InvalidConfigsException()),
])
def test_instantiation_failure(configs, expected_exception):
    """Test that the expected exceptions are thrown."""
    try:
        MultiRotatingLogger(configs)
    except (InvalidConfigsException) as current_exception:
        assert isinstance(current_exception, type(expected_exception))
    else:
        pytest.fail(f'Exception \"{type(expected_exception).__name__}\" was expected, but found none')


@pytest.mark.parametrize('configs', [
    ([{'name': 'name_test_000'}]),
    ([{'name': 'name_test_000'}, {'name': 'name_test_001'}]),
])
def test_instantiation_success(configs):
    """Test successful instantiation."""
    MultiRotatingLogger(configs)
