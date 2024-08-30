import pytest
from m3t_MultiRotatingLogger import MultiRotatingLogger, InvalidConfigsException, UnavailableNameException


@pytest.fixture
def new_instance():
    return MultiRotatingLogger()


@pytest.mark.parametrize('configs,expected_exception', [
    ({}, InvalidConfigsException()),
])
def test_create(configs, expected_exception):
    try:
        MultiRotatingLogger(configs)
    except (InvalidConfigsException) as current_exception:
        assert isinstance(current_exception, type(expected_exception))
    else:
        pytest.fail(f'Exception \"{type(expected_exception).__name__}\" was expected, but found none')
