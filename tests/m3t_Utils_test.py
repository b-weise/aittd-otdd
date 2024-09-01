import pytest
from m3t_Utils import Validation, InvalidTypeException, InvalidLengthException, InvalidRangeException


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


@pytest.mark.parametrize('object_to_validate,expected_range,expected_exception', [
    ([], 2, InvalidTypeException()),
    ([], {}, InvalidTypeException()),
    ([], 'asdf', InvalidTypeException()),
    ([], [], InvalidTypeException()),
    ([], (), InvalidLengthException()),
    ([1, 2, 3], (1, 3), InvalidLengthException()),
    ([1, 2, 3], (None, 3), InvalidLengthException()),
    ([1, 2, 3], (0, 2), InvalidLengthException()),
    ([1, 2, 3], (4, None), InvalidLengthException()),
    ({}, (4, None), InvalidLengthException()),
    (1, (4, None), TypeError()),
    (True, (4, None), TypeError()),
    ('asdf', ('', None), InvalidTypeException()),
    ('asdf', (3, {}), InvalidTypeException()),
    ('asdf', (3, 3), InvalidRangeException()),
    ('asdf', (4, 3), InvalidRangeException()),
])
def test_length_failure(new_instance, object_to_validate, expected_range, expected_exception):
    try:
        new_instance.length(object_to_validate, expected_range)
    except (InvalidTypeException, InvalidLengthException, TypeError, InvalidRangeException) as current_exception:
        assert isinstance(current_exception, type(expected_exception))
    else:
        pytest.fail(f'Exception \"{type(expected_exception).__name__}\" was expected, but found none')


@pytest.mark.parametrize('object_to_validate,expected_range', [
    ({}, (None, None)),
    ('asdf', (None, None)),
    ([1, 2, 3], (2, 5)),
    ([1, 2, 3], (3, 5)),
    ([1, 2, 3], (None, 4)),
    ([1, 2, 3], (3, 4)),
    ('asdf', (3, None)),
    ('asdf', (None, 9)),
])
def test_length_success(new_instance, object_to_validate, expected_range):
    new_instance.length(object_to_validate, expected_range)
