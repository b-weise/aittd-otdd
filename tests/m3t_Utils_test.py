import pytest
from m3t_Utils import Validation, InvalidTypeException


@pytest.fixture
def new_instance():
    return Validation()


@pytest.mark.parametrize('object_to_validate,expected_type,reversed_validation,expected_exception', [
    ({}, list, None, InvalidTypeException()),
    ({}, int, None, InvalidTypeException()),
    ({}, str, None, InvalidTypeException()),
    ('', dict, None, InvalidTypeException()),
    ('', list, None, InvalidTypeException()),
    (0, float, None, InvalidTypeException()),
    (0.0, int, None, InvalidTypeException()),
    (0, int, True, InvalidTypeException()),
    (0.0, float, 1, InvalidTypeException()),
])
def test_type_failure(new_instance, object_to_validate, expected_type, reversed_validation, expected_exception):
    try:
        new_instance.type(object_to_validate, expected_type, reversed_validation)
    except InvalidTypeException as current_exception:
        assert isinstance(current_exception, type(expected_exception))
    else:
        pytest.fail(f'Exception \"{type(expected_exception).__name__}\" was expected, but found none')


@pytest.mark.parametrize('object_to_validate,expected_type,reversed_validation', [
    ({}, dict, None),
    (0, int, None),
    (0.0, float, None),
    (0.0, float, False),
    (0.0, float, 0),
    (0, float, 1),
    ('aaa', dict, True),
])
def test_type_success(new_instance, object_to_validate, reversed_validation, expected_type):
    new_instance.type(object_to_validate, expected_type, reversed_validation)
