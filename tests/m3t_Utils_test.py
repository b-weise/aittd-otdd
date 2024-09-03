import pytest

from m3t_Utils import (Validation, UnexpectedTypeException, ExpectedTypeException, MinimumLengthException,
                       MaximumLengthException, InvalidRangeLengthException, InvalidRangeValuesException,
                       UnexpectedKeyException, ExpectedKeyException)


@pytest.fixture
def new_instance():
    return Validation()


@pytest.mark.parametrize('object_to_validate,expected_type,reversed_validation,expected_exception', [
    pytest.param({}, list, False, ExpectedTypeException(), id='--- PLAIN (NON-REVERSED) MISMATCHING TYPES ---'),
    pytest.param({}, int, False, ExpectedTypeException()),
    pytest.param({}, str, False, ExpectedTypeException()),
    pytest.param('', dict, False, ExpectedTypeException()),
    pytest.param('', list, False, ExpectedTypeException()),
    pytest.param(0, float, False, ExpectedTypeException()),
    pytest.param(0.0, int, False, ExpectedTypeException()),
    pytest.param(0, int, True, UnexpectedTypeException(), id='--- REVERSED MATCHING TYPES ---'),
    pytest.param({}, dict, True, UnexpectedTypeException()),
    pytest.param('', float, 0, ExpectedTypeException(), id='--- REVERSED AS INT ---'),
    pytest.param(0.0, float, 1, UnexpectedTypeException()),
])
def test_type_failure(new_instance, object_to_validate, expected_type, reversed_validation, expected_exception):
    try:
        new_instance.type(object_to_validate, expected_type, reversed_validation)
    except (ExpectedTypeException, UnexpectedTypeException) as current_exception:
        assert isinstance(current_exception, type(expected_exception))
    else:
        pytest.fail(f'Exception \"{type(expected_exception).__name__}\" was expected, but found none')


@pytest.mark.parametrize('object_to_validate,expected_type,reversed_validation', [
    pytest.param({}, dict, False, id='--- PLAIN (NON-REVERSED) MATCHING TYPES ---'),
    pytest.param(0, int, False),
    pytest.param(0.0, float, False),
    pytest.param('', str, False),
    pytest.param('aaa', dict, True, id='--- REVERSED MISMATCHING TYPES ---'),
    pytest.param([], str, True),
    pytest.param(0.0, float, 0, id='--- REVERSED AS INT ---'),
    pytest.param('', float, 1),
])
def test_type_success(new_instance, object_to_validate, reversed_validation, expected_type):
    new_instance.type(object_to_validate, expected_type, reversed_validation)


@pytest.mark.parametrize('object_to_validate,expected_range,expected_exception', [
    pytest.param(1, (4, None), TypeError(), id='--- WRONG OBJECT TYPE ---'),
    pytest.param(True, (4, None), TypeError()),
    pytest.param([], 2, ExpectedTypeException(), id='--- WRONG RANGE TYPE ---'),
    pytest.param([], {}, ExpectedTypeException()),
    pytest.param([], 'asdf', ExpectedTypeException()),
    pytest.param([], [], ExpectedTypeException()),
    pytest.param('asdf', ('', None), ExpectedTypeException(), id='--- WRONG RANGE ELEMENT TYPE ---'),
    pytest.param('asdf', (3, {}), ExpectedTypeException()),
    pytest.param([], (), InvalidRangeLengthException(), id='--- WRONG RANGE LENGTH ---'),
    pytest.param('asdf', (1, 2, 3), InvalidRangeLengthException()),
    pytest.param([1, 2, 3], (1, 3), MaximumLengthException(), id='--- OBJECT TOO LONG ---'),
    pytest.param([1, 2, 3], (None, 3), MaximumLengthException()),
    pytest.param([1, 2, 3], (0, 2), MaximumLengthException()),
    pytest.param([1, 2, 3], (4, None), MinimumLengthException(), id='--- OBJECT TOO SHORT ---'),
    pytest.param({}, (4, None), MinimumLengthException()),
    pytest.param('asdf', (3, 3), InvalidRangeValuesException(), id='--- INVALID RANGE LIMITS ---'),
    pytest.param('asdf', (4, 3), InvalidRangeValuesException()),
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
    pytest.param({}, (None, None), id='--- NO RANGE ---'),
    pytest.param('asdf', (None, None)),
    pytest.param([1, 2, 3], (2, 5), id='--- BOTH LIMITS ARE SPECIFIED ---'),
    pytest.param([1, 2, 3], (3, 5)),
    pytest.param([1, 2, 3], (3, 4)),
    pytest.param([1, 2, 3], (1, 4)),
    pytest.param([1, 2, 3], (None, 4), id='--- ONLY ONE LIMIT IS SPECIFIED ---'),
    pytest.param('asdf', (3, None)),
    pytest.param('asdf', (None, 9)),
])
def test_length_success(new_instance, object_to_validate, expected_range):
    new_instance.length(object_to_validate, expected_range)


@pytest.mark.parametrize('objects,validations,expected_exception', [
    pytest.param(1, {}, TypeError(), id='--- WRONG OBJECT TYPE ---'),
    pytest.param(True, {}, TypeError()),
    pytest.param([], 1, ExpectedTypeException(), id='--- WRONG VALIDATIONS TYPE ---'),
    pytest.param([], False, ExpectedTypeException()),
    pytest.param([1, {}], {
        'type': {'expected_type': int}
    }, ExpectedTypeException(), id='--- TYPE VALIDATION NOT PASSED ---'),
    pytest.param(['asdf'], {
        'type': {'expected_type': dict}
    }, ExpectedTypeException()),
    pytest.param(['asdf'], {
        'length': {'expected_range': (None, 3)}
    }, MaximumLengthException(), id='--- LENGTH VALIDATION NOT PASSED ---'),
    pytest.param(['asdf', 'asd', 'asdfgh'], {
        'length': {'expected_range': (3, 6)}
    }, MaximumLengthException()),
    pytest.param(['asdf', 'asd', 'asdfgh'], {
        'type': {'expected_type': str},
        'length': {'expected_range': (3, 6)},
    }, MaximumLengthException(), id='--- MULTIPLE VALIDATIONS ---'),
    pytest.param(['asdf', 'asd', 'asdfgh', [1, 2, 3]], {
        'type': {'expected_type': str},
        'length': {'expected_range': (3, 7)},
    }, ExpectedTypeException()),
    pytest.param(['asdf', 'asd', 'asdfgh', [1, 2, 3]], {
        'length': {'expected_range': (3, 7)},
        'type': {'expected_type': str},
    }, ExpectedTypeException(), id='--- VALIDATING LENGTH FIRST ---'),
    pytest.param(['asdf', 'asd', 'asdfgh', 1], {
        'length': {'expected_range': (3, 7)},
        'type': {'expected_type': str},
    }, TypeError()),
    pytest.param([{'aaa': 111, 'bbb': 222, 'ccc': 333}], {
        'type': {'expected_type': dict},
        'key_existence': {'key_name': 'ddd'},
    }, ExpectedKeyException(), id='--- INCLUDING KEY_EXISTENCE VALIDATION ---'),
    pytest.param([{'aaa': 111}, {'bbb': 222}, {'ccc': 333}], {
        'type': {'expected_type': dict},
        'key_existence': {'key_name': 'bbb'},
    }, ExpectedKeyException()),
    pytest.param([{'aaa': 111, 'bbb': 222, 'ccc': 333}], {
        'type': {'expected_type': dict},
        'key_existence': {'key_name': 'bbb', 'reversed_validation': True},
    }, UnexpectedKeyException(), id='--- REVERSING KEY_EXISTENCE VALIDATION ---'),
    pytest.param([{'aaa': 111}, {'bbb': 222}, {'ccc': 333}], {
        'type': {'expected_type': dict},
        'key_existence': {'key_name': 'bbb', 'reversed_validation': True},
    }, UnexpectedKeyException()),
    pytest.param([{'aaa': 111}, {'aaa': 222}, {'aaa': [3]}], {
        'type': {'expected_type': dict},
        'key_existence': {'key_name': 'aaa', 'validations': {'type': {'expected_type': int}}},
    }, ExpectedTypeException(), id='--- INCLUDING RECURSIVE VALIDATIONS ---'),
    pytest.param([{'aaa': [1, 1, 1, 1, 1]}, {'aaa': [2, 2, 2, 2, 2, 2]}, {'aaa': [3, 3, 3]}], {
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
    pytest.param([], {}, id='--- EMPTY PARAMS ---'),
    pytest.param([1, 2], {'type': {'expected_type': int}}, id='--- MATCHING TYPES ---'),
    pytest.param(['asdf', 'asd', 'asdfgh'], {
        'length': {'expected_range': (3, 7)}
    }, id='--- MATCHING LENGTHS ---'),
    pytest.param(['asdf', 'asd', 'asdfgh'], {
        'type': {'expected_type': str}, 'length': {'expected_range': (3, 7)}
    }, id='--- MATCHING MULTIPLE VALIDATIONS ---'),
    pytest.param([{'aaa': 111}, {'aaa': 222}, {'aaa': 333}], {
        'type': {'expected_type': dict},
        'key_existence': {'key_name': 'aaa', 'reversed_validation': False},
    }, id='--- MATCHING KEY_EXISTENCE ---'),
    pytest.param([{'aaa': 111}, {'aaa': 222}, {'aaa': 333}], {
        'type': {'expected_type': dict},
        'key_existence': {'key_name': 'bbb', 'reversed_validation': True},
    }, id='--- MATCHING REVERSED KEY_EXISTENCE ---'),
    pytest.param(({'aaa': 111}, {'aaa': 222}, {'aaa': 333}), {
        'type': {'expected_type': dict},
        'key_existence': {'key_name': 'aaa', 'reversed_validation': False},
    }, id='--- OBJECT AS TUPLE ---'),
])
def test_recursive_validation_success(new_instance, objects, validations):
    new_instance.recursive_validation(objects, validations)


@pytest.mark.parametrize('object_to_validate,key_name,validations,reversed_validation,expected_exception', [
    pytest.param(1, 'asdf', {}, False, ExpectedTypeException(), id='--- WRONG OBJECT TYPE ---'),
    pytest.param({}, 1, {}, False, ExpectedTypeException(), id='--- WRONG KEY TYPE ---'),
    pytest.param({}, 'asdf', [], False, ExpectedTypeException(), id='--- WRONG VALIDATIONS TYPE ---'),
    pytest.param({}, 'asdf', {}, 1, ExpectedTypeException(), id='--- WRONG REVERSED TYPE ---'),
    pytest.param({}, '', {}, False, MinimumLengthException(), id='--- EMPTY KEY STRING ---'),
    pytest.param({}, 'asdf', {}, False, ExpectedKeyException(), id='--- PLAIN (NON-REVERSED) VALIDATION ---'),
    pytest.param({'zxcv': None}, 'asdf', {}, False, ExpectedKeyException()),
    pytest.param({'asdf': None}, 'asdf', {}, True, UnexpectedKeyException(), id='--- REVERSED VALIDATION ---'),
    pytest.param({'asdf': 123}, 'asdf', {
        'type': {'expected_type': str}
    }, False, ExpectedTypeException(), id='--- INCLUDING RECURSIVE VALIDATIONS ---'),
    pytest.param({'asdf': 123}, 'asdf', {
        'type': {'expected_type': int, 'reversed_validation': True}
    }, False, UnexpectedTypeException(), id='--- RECURSIVE VALIDATIONS ARE REVERSED ---'),
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
    pytest.param({'asdf': None}, 'asdf', {}, False, id='--- PLAIN (NON-REVERSED) VALIDATION ---'),
    pytest.param({'zxcv': None}, 'asdf', {}, True, id='--- REVERSED VALIDATION ---'),
    pytest.param({}, 'asdf', {}, True),
    pytest.param({'asdf': 123}, 'asdf', {
        'type': {'expected_type': int}
    }, False, id='--- INCLUDING RECURSIVE VALIDATIONS ---'),
    pytest.param({'asdf': 123}, 'asdf', {
        'type': {'expected_type': dict, 'reversed_validation': True}
    }, False, id='--- RECURSIVE VALIDATIONS ARE REVERSED ---'),
])
def test_key_existence_success(
        new_instance, object_to_validate, key_name, validations, reversed_validation
):
    new_instance.key_existence(object_to_validate, key_name, validations, reversed_validation)
