import pytest
from m3t_MultiRotatingLogger import MultiRotatingLogger, InvalidConfigsException, UnavailableNameException


@pytest.fixture
def new_instance():
    return MultiRotatingLogger()


@pytest.mark.parametrize('configs,expected_exception', [
    ([], InvalidConfigsException()),
])
def test_instantiation_bad_input(configs, expected_exception):
    """Test that the expected exceptions are thrown."""
    try:
        MultiRotatingLogger(configs)
    except (InvalidConfigsException) as current_exception:
        assert isinstance(current_exception, type(expected_exception))
    else:
        pytest.fail(f'Exception \"{type(expected_exception).__name__}\" was expected, but found none')


@pytest.mark.parametrize('configs', [
    ([{'name': 'name_test_000'}]),
])
def test_instantiation_success(configs):
    """Test successful instantiation."""
    MultiRotatingLogger(configs)
