import pytest
from m3t_Utils import Validation, InvalidTypeException


@pytest.fixture
def new_instance():
    return Validation()


@pytest.mark.parametrize('object_to_validate,expected_type,expected_exception', [
    ({}, list, InvalidTypeException()),
    ({}, int, InvalidTypeException()),
    ({}, str, InvalidTypeException()),
    ('', dict, InvalidTypeException()),
    ('', list, InvalidTypeException()),
    (0, float, InvalidTypeException()),
    (0.0, int, InvalidTypeException()),
])
def test_type_failure(new_instance, object_to_validate, expected_type, expected_exception):
    try:
        new_instance.type(object_to_validate, expected_type)
    except InvalidTypeException as current_exception:
        assert isinstance(current_exception, type(expected_exception))
    else:
        pytest.fail(f'Exception \"{type(expected_exception).__name__}\" was expected, but found none')


@pytest.mark.parametrize('object_to_validate,expected_type', [
    ({}, dict),
    (0, int),
    (0.0, float),
])
def test_type_success(new_instance, object_to_validate, expected_type):
    new_instance.type(object_to_validate, expected_type)
