import pytest

from m3t_Utils import Validation, InvalidTypeException, InvalidLengthException, InvalidRangeException, \
    KeyExistenceException


@pytest.fixture
def new_instance():
    return Validation()


@pytest.mark.parametrize('object_to_validate,expected_type,reversed_validation,expected_exception', [
    ({}, list, False, InvalidTypeException()),
    ({}, int, False, InvalidTypeException()),
    ({}, str, False, InvalidTypeException()),
    ('', dict, False, InvalidTypeException()),
    ('', list, False, InvalidTypeException()),
    (0, float, False, InvalidTypeException()),
    (0.0, int, False, InvalidTypeException()),
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


@pytest.mark.parametrize('objects,validations,expected_exception', [
    (1, {}, TypeError()),
    (True, {}, TypeError()),
    ([], 1, InvalidTypeException()),
    ([], False, InvalidTypeException()),
    ([1, {}], {'type': {'expected_type': int}}, InvalidTypeException()),
    (['asdf'], {'type': {'expected_type': dict}}, InvalidTypeException()),
    (['asdf'], {'length': {'expected_range': (None, 3)}}, InvalidLengthException()),
    (['asdf', 'asd', 'asdfgh'], {'length': {'expected_range': (3, 6)}}, InvalidLengthException()),
    (['asdf', 'asd', 'asdfgh'], {
        'type': {'expected_type': str},
        'length': {'expected_range': (3, 6)},
    }, InvalidLengthException()),
    (['asdf', 'asd', 'asdfgh', [1, 2, 3]], {
        'type': {'expected_type': str},
        'length': {'expected_range': (3, 7)},
    }, InvalidTypeException()),
    (['asdf', 'asd', 'asdfgh', [1, 2, 3]], {
        'length': {'expected_range': (3, 7)},
        'type': {'expected_type': str},
    }, InvalidTypeException()),
    (['asdf', 'asd', 'asdfgh', 1], {
        'length': {'expected_range': (3, 7)},
        'type': {'expected_type': str},
    }, TypeError()),
    ([{'aaa': 111, 'bbb': 222, 'ccc': 333}], {
        'type': {'expected_type': dict},
        'key_existence': {'key_name': 'bbb', 'reversed_validation': True},
    }, KeyExistenceException()),
    ([{'aaa': 111}, {'bbb': 222}, {'ccc': 333}], {
        'type': {'expected_type': dict},
        'key_existence': {'key_name': 'bbb', 'reversed_validation': True},
    }, KeyExistenceException()),
    ([{'aaa': 111}, {'bbb': 222}, {'ccc': 333}], {
        'type': {'expected_type': dict},
        'key_existence': {'key_name': 'bbb'},
    }, KeyExistenceException()),
    ([{'aaa': 111}, {'aaa': 222}, {'aaa': [3]}], {
        'type': {'expected_type': dict},
        'key_existence': {'key_name': 'aaa', 'validations': {'type': {'expected_type': int}}},
    }, InvalidTypeException()),
    ([{'aaa': [1, 1, 1, 1, 1]}, {'aaa': [2, 2, 2, 2, 2, 2]}, {'aaa': [3, 3, 3]}], {
        'type': {'expected_type': dict},
        'key_existence': {'key_name': 'aaa', 'validations': {'length': {'expected_range': (5, None)}}},
    }, InvalidLengthException()),
])
def test_recursive_validation_failure(new_instance, objects, validations, expected_exception):
    try:
        new_instance.recursive_validation(objects, validations)
    except (TypeError, InvalidTypeException, InvalidLengthException, KeyExistenceException) as current_exception:
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
    (1, 'asdf', {}, False, InvalidTypeException()),
    ({}, 1, {}, False, InvalidTypeException()),
    ({}, 'asdf', [], False, InvalidTypeException()),
    ({}, 'asdf', {}, 1, InvalidTypeException()),
    ({}, '', {}, False, InvalidLengthException()),
    ({}, 'asdf', {}, False, KeyExistenceException()),
    ({'zxcv': None}, 'asdf', {}, False, KeyExistenceException()),
    ({'asdf': None}, 'asdf', {}, True, KeyExistenceException()),
    ({'asdf': 123}, 'asdf', {'type': {'expected_type': str}}, False, InvalidTypeException()),
    ({'asdf': 123}, 'asdf', {'type': {'expected_type': int, 'reversed_validation': True}}, False, InvalidTypeException()),
])
def test_key_existence_failure(
        new_instance, object_to_validate, key_name, validations, reversed_validation, expected_exception
):
    try:
        new_instance.key_existence(object_to_validate, key_name, validations, reversed_validation)
    except (InvalidTypeException, InvalidLengthException, KeyExistenceException) as current_exception:
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
