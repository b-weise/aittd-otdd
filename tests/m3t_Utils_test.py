import pytest

from m3t_Utils import (Validation, UnexpectedTypeException, ExpectedTypeException, MinimumLengthException,
                       MaximumLengthException, InvalidRangeLengthException, InvalidRangeValuesException,
                       UnexpectedKeyException, ExpectedKeyException)


@pytest.fixture
def new_instance():
    return Validation()


@pytest.mark.parametrize('object_to_validate,expected_type,reversed_validation,expected_exception', [
    ({}, list, False, ExpectedTypeException()),
    ({}, int, False, ExpectedTypeException()),
    ({}, str, False, ExpectedTypeException()),
    ('', dict, False, ExpectedTypeException()),
    ('', list, False, ExpectedTypeException()),
    (0, float, False, ExpectedTypeException()),
    (0.0, int, False, ExpectedTypeException()),
    (0, int, True, UnexpectedTypeException()),
    (0.0, float, 1, UnexpectedTypeException()),
])
def test_type_failure(new_instance, object_to_validate, expected_type, reversed_validation, expected_exception):
    try:
        new_instance.type(object_to_validate, expected_type, reversed_validation)
    except (ExpectedTypeException, UnexpectedTypeException) as current_exception:
        assert isinstance(current_exception, type(expected_exception))
    else:
        pytest.fail(f'Exception \"{type(expected_exception).__name__}\" was expected, but found none')


@pytest.mark.parametrize('object_to_validate,expected_type,reversed_validation', [
    ({}, dict, False),
    (0, int, False),
    (0.0, float, False),
    (0.0, float, False),
    (0.0, float, 0),
    (0, float, 1),
    ('aaa', dict, True),
])
def test_type_success(new_instance, object_to_validate, reversed_validation, expected_type):
    new_instance.type(object_to_validate, expected_type, reversed_validation)


@pytest.mark.parametrize('object_to_validate,expected_range,expected_exception', [
    ([], 2, ExpectedTypeException()),
    ([], {}, ExpectedTypeException()),
    ([], 'asdf', ExpectedTypeException()),
    ([], [], ExpectedTypeException()),
    ([], (), InvalidRangeLengthException()),
    ([1, 2, 3], (1, 3), MaximumLengthException()),
    ([1, 2, 3], (None, 3), MaximumLengthException()),
    ([1, 2, 3], (0, 2), MaximumLengthException()),
    ([1, 2, 3], (4, None), MinimumLengthException()),
    ({}, (4, None), MinimumLengthException()),
    (1, (4, None), TypeError()),
    (True, (4, None), TypeError()),
    ('asdf', ('', None), ExpectedTypeException()),
    ('asdf', (3, {}), ExpectedTypeException()),
    ('asdf', (3, 3), InvalidRangeValuesException()),
    ('asdf', (4, 3), InvalidRangeValuesException()),
    ('asdf', (1, 2, 3), InvalidRangeLengthException()),
])
def test_length_failure(new_instance, object_to_validate, expected_range, expected_exception):
    try:
        new_instance.length(object_to_validate, expected_range)
    except (ExpectedTypeException, MinimumLengthException, MaximumLengthException, TypeError,
            InvalidRangeValuesException, InvalidRangeLengthException) as current_exception:
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


@pytest.mark.parametrize('objects,validations,expected_exception', [
    (1, {}, TypeError()),
    (True, {}, TypeError()),
    ([], 1, ExpectedTypeException()),
    ([], False, ExpectedTypeException()),
    ([1, {}], {'type': {'expected_type': int}}, ExpectedTypeException()),
    (['asdf'], {'type': {'expected_type': dict}}, ExpectedTypeException()),
    (['asdf'], {'length': {'expected_range': (None, 3)}}, MaximumLengthException()),
    (['asdf', 'asd', 'asdfgh'], {'length': {'expected_range': (3, 6)}}, MaximumLengthException()),
    (['asdf', 'asd', 'asdfgh'], {
        'type': {'expected_type': str},
        'length': {'expected_range': (3, 6)},
    }, MaximumLengthException()),
    (['asdf', 'asd', 'asdfgh', [1, 2, 3]], {
        'type': {'expected_type': str},
        'length': {'expected_range': (3, 7)},
    }, ExpectedTypeException()),
    (['asdf', 'asd', 'asdfgh', [1, 2, 3]], {
        'length': {'expected_range': (3, 7)},
        'type': {'expected_type': str},
    }, ExpectedTypeException()),
    (['asdf', 'asd', 'asdfgh', 1], {
        'length': {'expected_range': (3, 7)},
        'type': {'expected_type': str},
    }, TypeError()),
    ([{'aaa': 111, 'bbb': 222, 'ccc': 333}], {
        'type': {'expected_type': dict},
        'key_existence': {'key_name': 'bbb', 'reversed_validation': True},
    }, UnexpectedKeyException()),
    ([{'aaa': 111}, {'bbb': 222}, {'ccc': 333}], {
        'type': {'expected_type': dict},
        'key_existence': {'key_name': 'bbb', 'reversed_validation': True},
    }, UnexpectedKeyException()),
    ([{'aaa': 111}, {'bbb': 222}, {'ccc': 333}], {
        'type': {'expected_type': dict},
        'key_existence': {'key_name': 'bbb'},
    }, ExpectedKeyException()),
    ([{'aaa': 111}, {'aaa': 222}, {'aaa': [3]}], {
        'type': {'expected_type': dict},
        'key_existence': {'key_name': 'aaa', 'validations': {'type': {'expected_type': int}}},
    }, ExpectedTypeException()),
    ([{'aaa': [1, 1, 1, 1, 1]}, {'aaa': [2, 2, 2, 2, 2, 2]}, {'aaa': [3, 3, 3]}], {
        'type': {'expected_type': dict},
        'key_existence': {'key_name': 'aaa', 'validations': {'length': {'expected_range': (5, None)}}},
    }, MinimumLengthException()),
])
def test_recursive_validation_failure(new_instance, objects, validations, expected_exception):
    try:
        new_instance.recursive_validation(objects, validations)
    except (TypeError, ExpectedTypeException, MinimumLengthException, MaximumLengthException,
            UnexpectedKeyException, ExpectedKeyException) as current_exception:
        assert isinstance(current_exception, type(expected_exception))
    else:
        pytest.fail(f'Exception \"{type(expected_exception).__name__}\" was expected, but found none')


@pytest.mark.parametrize('objects,validations', [
    ([], {}),
    ([1, 2], {'type': {'expected_type': int}}),
    (['asdf', 'asd', 'asdfgh'], {'length': {'expected_range': (3, 7)}}),
    (['asdf', 'asd', 'asdfgh'], {'type': {'expected_type': str}, 'length': {'expected_range': (3, 7)}}),
    ([{'aaa': 111}, {'aaa': 222}, {'aaa': 333}], {
        'type': {'expected_type': dict},
        'key_existence': {'key_name': 'aaa', 'reversed_validation': False},
    }),
    (({'aaa': 111}, {'aaa': 222}, {'aaa': 333}), {
        'type': {'expected_type': dict},
        'key_existence': {'key_name': 'aaa', 'reversed_validation': False},
    }),
])
def test_recursive_validation_success(new_instance, objects, validations):
    new_instance.recursive_validation(objects, validations)


@pytest.mark.parametrize('object_to_validate,key_name,validations,reversed_validation,expected_exception', [
    (1, 'asdf', {}, False, ExpectedTypeException()),
    ({}, 1, {}, False, ExpectedTypeException()),
    ({}, 'asdf', [], False, ExpectedTypeException()),
    ({}, 'asdf', {}, 1, ExpectedTypeException()),
    ({}, '', {}, False, MinimumLengthException()),
    ({}, 'asdf', {}, False, ExpectedKeyException()),
    ({'zxcv': None}, 'asdf', {}, False, ExpectedKeyException()),
    ({'asdf': None}, 'asdf', {}, True, UnexpectedKeyException()),
    ({'asdf': 123}, 'asdf', {'type': {'expected_type': str}}, False, ExpectedTypeException()),
    ({'asdf': 123}, 'asdf', {'type': {'expected_type': int, 'reversed_validation': True}}, False,
     UnexpectedTypeException()),
])
def test_key_existence_failure(
        new_instance, object_to_validate, key_name, validations, reversed_validation, expected_exception
):
    try:
        new_instance.key_existence(object_to_validate, key_name, validations, reversed_validation)
    except (ExpectedTypeException, UnexpectedTypeException, MinimumLengthException, UnexpectedKeyException,
            ExpectedKeyException) as current_exception:
        assert isinstance(current_exception, type(expected_exception))
    else:
        pytest.fail(f'Exception \"{type(expected_exception).__name__}\" was expected, but found none')


@pytest.mark.parametrize('object_to_validate,key_name,validations,reversed_validation', [
    ({'asdf': None}, 'asdf', {}, False),
    ({'zxcv': None}, 'asdf', {}, True),
    ({}, 'asdf', {}, True),
    ({'asdf': 123}, 'asdf', {'type': {'expected_type': int}}, False),
    ({'asdf': 123}, 'asdf', {'type': {'expected_type': int, 'reversed_validation': False}}, False),
])
def test_key_existence_success(
        new_instance, object_to_validate, key_name, validations, reversed_validation
):
    new_instance.key_existence(object_to_validate, key_name, validations, reversed_validation)
