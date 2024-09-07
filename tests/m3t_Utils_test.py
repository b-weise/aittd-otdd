import dataclasses
import sys
from dataclasses import dataclass
from typing import Any

import pytest

from m3t_BaseTestCase import BaseTestCase
from m3t_Utils import (Validation, ForbiddenTypeException, MandatoryTypeException, MinimumLengthException,
                       MaximumLengthException, InvalidRangeLengthException, InvalidRangeValuesException,
                       ForbiddenKeyException, MandatoryKeyException)


@pytest.fixture
def new_instance():
    return Validation()


@dataclass
class TypeMethodTestCase(BaseTestCase):
    object_to_validate: Any = None
    expected_type: Any = None
    reversed_validation: Any = False


TypeMethTC = TypeMethodTestCase


@pytest.mark.parametrize('test_case', [pytest.param(test_case, id=test_case.id) for test_case in [
    TypeMethTC(id='wrong expected_type type',
               object_to_validate={}, expected_type=111, expected_exception=MandatoryTypeException),
    TypeMethTC(object_to_validate=[], expected_type='', expected_exception=MandatoryTypeException),
    TypeMethTC(id='wrong reversed_validation type',
               object_to_validate=0.0, expected_type=float, reversed_validation=111,
               expected_exception=MandatoryTypeException),
    TypeMethTC(object_to_validate=0, expected_type=int, reversed_validation='',
               expected_exception=MandatoryTypeException),
    TypeMethTC(id='plain (non-reversed) mismatching types',
               object_to_validate=(), expected_type=set, expected_exception=MandatoryTypeException),
    TypeMethTC(object_to_validate='', expected_type=list, expected_exception=MandatoryTypeException),
    TypeMethTC(object_to_validate={}, expected_type=str, expected_exception=MandatoryTypeException),
    TypeMethTC(object_to_validate=0, expected_type=float, expected_exception=MandatoryTypeException),
    TypeMethTC(object_to_validate=0.0, expected_type=int, expected_exception=MandatoryTypeException),
    TypeMethTC(id='reversed matching types',
               object_to_validate=0, expected_type=int, reversed_validation=True,
               expected_exception=ForbiddenTypeException),
    TypeMethTC(object_to_validate=0.0, expected_type=float, reversed_validation=True,
               expected_exception=ForbiddenTypeException),
    TypeMethTC(id='specifing multiple types',
               object_to_validate='', expected_type=int | float, expected_exception=MandatoryTypeException),
    TypeMethTC(object_to_validate={}, expected_type=set | list, expected_exception=MandatoryTypeException),
    TypeMethTC(id='specifing multiple types, reversed',
               object_to_validate='', expected_type=str | list, reversed_validation=True, expected_exception=ForbiddenTypeException),
    TypeMethTC(object_to_validate=True, expected_type=list | bool, reversed_validation=True, expected_exception=ForbiddenTypeException),
]])
def test_type_failure(new_instance, test_case: TypeMethodTestCase):
    try:
        new_instance.type(test_case.object_to_validate, test_case.expected_type, test_case.reversed_validation)
    except:
        assert isinstance(sys.exception(), test_case.expected_exception)
    else:
        pytest.fail(f'Exception \"{test_case.expected_exception.__name__}\" was expected, but found none')


@pytest.mark.parametrize('test_case', [pytest.param(test_case, id=test_case.id) for test_case in [
    TypeMethTC(id='plain (non-reversed) matching types',
               object_to_validate={}, expected_type=dict),
    TypeMethTC(object_to_validate=0, expected_type=int),
    TypeMethTC(object_to_validate=0.0, expected_type=float),
    TypeMethTC(object_to_validate='', expected_type=str),
    TypeMethTC(id='reversed mismatching types',
               object_to_validate='aaa', expected_type=dict, reversed_validation=True),
    TypeMethTC(object_to_validate=[], expected_type=int, reversed_validation=True),
    TypeMethTC(id='specifing multiple types',
               object_to_validate='', expected_type=int | str),
    TypeMethTC(object_to_validate={}, expected_type=dict | list),
    TypeMethTC(id='specifing multiple types, reversed',
               object_to_validate=1, expected_type=dict | list, reversed_validation=True),
    TypeMethTC(object_to_validate='', expected_type=int | float, reversed_validation=True),
]])
def test_type_success(new_instance, test_case: TypeMethodTestCase):
    new_instance.type(test_case.object_to_validate, test_case.expected_type, test_case.reversed_validation)


@dataclass
class LengthMethodTestCase(BaseTestCase):
    object_to_validate: Any = None
    expected_range: Any = None


LengthMethTC = LengthMethodTestCase


@pytest.mark.parametrize('test_case', [pytest.param(test_case, id=test_case.id) for test_case in [
    LengthMethTC(id='wrong object type',
                 object_to_validate=1, expected_range=(4, None), expected_exception=MandatoryTypeException),
    LengthMethTC(object_to_validate=True, expected_range=(4, None), expected_exception=MandatoryTypeException),
    LengthMethTC(id='wrong range type',
                 object_to_validate=[], expected_range=2, expected_exception=MandatoryTypeException),
    LengthMethTC(object_to_validate=[], expected_range={}, expected_exception=MandatoryTypeException),
    LengthMethTC(object_to_validate=[], expected_range='asdf', expected_exception=MandatoryTypeException),
    LengthMethTC(object_to_validate=[], expected_range=[], expected_exception=MandatoryTypeException),
    LengthMethTC(id='wrong range element type',
                 object_to_validate='asdf', expected_range=('', None), expected_exception=MandatoryTypeException),
    LengthMethTC(object_to_validate='asdf', expected_range=(3, {}), expected_exception=MandatoryTypeException),
    LengthMethTC(id='wrong range length',
                 object_to_validate=[], expected_range=(), expected_exception=InvalidRangeLengthException),
    LengthMethTC(object_to_validate='asdf', expected_range=(1, 2, 3), expected_exception=InvalidRangeLengthException),
    LengthMethTC(id='object too long',
                 object_to_validate=[1, 2, 3], expected_range=(1, 3), expected_exception=MaximumLengthException),
    LengthMethTC(object_to_validate=[1, 2, 3], expected_range=(None, 3), expected_exception=MaximumLengthException),
    LengthMethTC(object_to_validate=[1, 2, 3], expected_range=(0, 2), expected_exception=MaximumLengthException),
    LengthMethTC(id='object too short',
                 object_to_validate=[1, 2, 3], expected_range=(4, None), expected_exception=MinimumLengthException),
    LengthMethTC(object_to_validate={}, expected_range=(4, None), expected_exception=MinimumLengthException),
    LengthMethTC(id='invalid range limits',
                 object_to_validate='asdf', expected_range=(3, 3), expected_exception=InvalidRangeValuesException),
    LengthMethTC(object_to_validate='asdf', expected_range=(4, 3), expected_exception=InvalidRangeValuesException),
]])
def test_length_failure(new_instance, test_case: LengthMethodTestCase):
    try:
        new_instance.length(test_case.object_to_validate, test_case.expected_range)
    except:
        assert isinstance(sys.exception(), test_case.expected_exception)
    else:
        pytest.fail(f'Exception \"{test_case.expected_exception.__name__}\" was expected, but found none')


@pytest.mark.parametrize('test_case', [pytest.param(test_case, id=test_case.id) for test_case in [
    LengthMethTC(id='no range',
                 object_to_validate={}, expected_range=(None, None)),
    LengthMethTC(object_to_validate='asdf', expected_range=(None, None)),
    LengthMethTC(id='both limits are specified',
                 object_to_validate=[1, 2, 3], expected_range=(2, 5)),
    LengthMethTC(object_to_validate=[1, 2, 3], expected_range=(3, 5)),
    LengthMethTC(object_to_validate=[1, 2, 3], expected_range=(3, 4)),
    LengthMethTC(object_to_validate=[1, 2, 3], expected_range=(1, 4)),
    LengthMethTC(object_to_validate=[1], expected_range=(1, 2)),
    LengthMethTC(object_to_validate=[1], expected_range=(0, 2)),
    LengthMethTC(id='only one limit is specified',
                 object_to_validate=[1, 2, 3], expected_range=(None, 4)),
    LengthMethTC(object_to_validate=[1], expected_range=(None, 3)),
    LengthMethTC(object_to_validate='asdf', expected_range=(1, None)),
    LengthMethTC(object_to_validate='asdf', expected_range=(4, None)),
]])
def test_length_success(new_instance, test_case: LengthMethodTestCase):
    new_instance.length(test_case.object_to_validate, test_case.expected_range)


@dataclass
class IterateMethodTestCase(BaseTestCase):
    objects: Any = None
    validations: Any = None


ItMethTC = IterateMethodTestCase


@pytest.mark.parametrize('test_case', [pytest.param(test_case, id=test_case.id) for test_case in [
    ItMethTC(id='wrong object type',
             objects=1, validations={}, expected_exception=MandatoryTypeException),
    ItMethTC(objects=True, validations={}, expected_exception=MandatoryTypeException),
    ItMethTC(id='wrong validations type',
             objects=[], validations=1, expected_exception=MandatoryTypeException),
    ItMethTC(objects=[], validations=False, expected_exception=MandatoryTypeException),
    ItMethTC(id='type validation not passed',
             objects=[1, {}], validations={'type': {'expected_type': int}},
             expected_exception=MandatoryTypeException),
    ItMethTC(objects=['asdf'], validations={'type': {'expected_type': dict}},
             expected_exception=MandatoryTypeException),
    ItMethTC(id='length validation not passed',
             objects=['asdf'], validations={'length': {'expected_range': (None, 4)}},
             expected_exception=MaximumLengthException),
    ItMethTC(objects=['asd', 'asdfgh', 'as'], validations={'length': {'expected_range': (3, 7)}},
             expected_exception=MinimumLengthException),
    ItMethTC(id='multiple validations',
             objects=['asdf', 'asd', 'asdfgh'],
             validations={
                 'type': {'expected_type': str},
                 'length': {'expected_range': (3, 6)},
             }, expected_exception=MaximumLengthException),
    ItMethTC(objects=['asdf', 'asd', 'asdfgh', ['a', 's', 'd']],
             validations={
                 'type': {'expected_type': str},
                 'length': {'expected_range': (3, 7)},
             }, expected_exception=MandatoryTypeException),
    ItMethTC(id='validating length first',
             objects=['asdf', 'asd', 'asdfgh', ['a', 's', 'd']],
             validations={
                 'length': {'expected_range': (3, 7)},
                 'type': {'expected_type': str},
             }, expected_exception=MandatoryTypeException),
    ItMethTC(objects=['asdf', 'asd', 'asdfgh', 1],
             validations={
                 'length': {'expected_range': (3, 7)},
                 'type': {'expected_type': str},
             }, expected_exception=MandatoryTypeException),
    ItMethTC(id='including key_existence validation',
             objects=[{'aaa': 111, 'bbb': 222, 'ccc': 333}],
             validations={
                 'type': {'expected_type': dict},
                 'key_existence': {'key_name': 'ddd'},
             }, expected_exception=MandatoryKeyException),
    ItMethTC(objects=[{'aaa': 111}, {'bbb': 222}, {'ccc': 333}],
             validations={
                 'key_existence': {'key_name': 'bbb'},
             }, expected_exception=MandatoryKeyException),
    ItMethTC(id='reversing key_existence validation',
             objects=[{'aaa': 111, 'bbb': 222, 'ccc': 333}],
             validations={
                 'key_existence': {'key_name': 'bbb', 'reversed_validation': True},
             }, expected_exception=ForbiddenKeyException),
    ItMethTC(objects=[{'aaa': 111}, {'bbb': 222}, {'ccc': 333}],
             validations={
                 'key_existence': {'key_name': 'bbb', 'reversed_validation': True},
             }, expected_exception=ForbiddenKeyException),
    ItMethTC(id='including iterative validations',
             objects=[{'aaa': 111}, {'aaa': 222}, {'aaa': [3]}],
             validations={
                 'key_existence': {'key_name': 'aaa', 'validations': {'type': {'expected_type': int}}},
             }, expected_exception=MandatoryTypeException),
    ItMethTC(objects=[{'aaa': [1, 1, 1, 1, 1]}, {'aaa': [2, 2, 2, 2, 2, 2]}, {'aaa': [3, 3, 3]}],
             validations={
                 'key_existence': {'key_name': 'aaa', 'validations': {
                     'type': {'expected_type': list},
                     'length': {'expected_range': (5, None)},
                 }},
             }, expected_exception=MinimumLengthException),
]])
def test_iterate_failure(new_instance, test_case: IterateMethodTestCase):
    try:
        new_instance.iterate(test_case.objects, test_case.validations)
    except:
        assert isinstance(sys.exception(), test_case.expected_exception)
    else:
        pytest.fail(f'Exception \"{test_case.expected_exception.__name__}\" was expected, but found none')


@pytest.mark.parametrize('test_case', [pytest.param(test_case, id=test_case.id) for test_case in [
    ItMethTC(id='empty params',
             objects=[], validations={}),
    ItMethTC(id='matching types',
             objects=[1, 2], validations={'type': {'expected_type': int}}),
    ItMethTC(id='matching lengths',
             objects=['asdf', 'asd', 'asdfgh'], validations={'length': {'expected_range': (3, 7)}}),
    ItMethTC(id='matching multiple validations',
             objects=['asdf', 'asd', 'asdfgh'],
             validations={
                 'type': {'expected_type': str},
                 'length': {'expected_range': (3, 7)}
             }),
    ItMethTC(id='matching key_existence',
             objects=[{'aaa': 111}, {'aaa': 222}, {'aaa': 333}],
             validations={
                 'type': {'expected_type': dict},
                 'key_existence': {'key_name': 'aaa'},
             }),
    ItMethTC(id='matching reversed key_existence',
             objects=[{'aaa': 111}, {'aaa': 222}, {'aaa': 333}],
             validations={
                 'type': {'expected_type': dict},
                 'key_existence': {'key_name': 'bbb', 'reversed_validation': True},
             }),
    ItMethTC(id='object as tuple',
             objects=({'aaa': 111}, {'aaa': 222}, {'aaa': 333}),
             validations={
                 'type': {'expected_type': dict},
                 'key_existence': {'key_name': 'aaa'},
             }),
]])
def test_iterate_success(new_instance, test_case: IterateMethodTestCase):
    new_instance.iterate(test_case.objects, test_case.validations)


@dataclass
class KeyExistenceMethodTestCase(BaseTestCase):
    object_to_validate: Any = None
    key_name: Any = None
    validations: Any = dataclasses.field(default_factory=dict)
    reversed_validation: Any = False


KeyExMethTC = KeyExistenceMethodTestCase


@pytest.mark.parametrize('test_case', [pytest.param(test_case, id=test_case.id) for test_case in [
    KeyExMethTC(id='wrong object type',
                object_to_validate=1, key_name='asdf', expected_exception=MandatoryTypeException),
    KeyExMethTC(id='wrong key type',
                object_to_validate={}, key_name=1, expected_exception=MandatoryTypeException),
    KeyExMethTC(id='wrong validations type',
                object_to_validate={}, key_name='asdf', validations=[], expected_exception=MandatoryTypeException),
    KeyExMethTC(id='wrong reversed_validation type',
                object_to_validate={}, key_name='asdf', reversed_validation=1, expected_exception=MandatoryTypeException),
    KeyExMethTC(id='empty key string',
                object_to_validate={}, key_name='', expected_exception=MinimumLengthException),
    KeyExMethTC(id='plain (non-reversed) validation',
                object_to_validate={}, key_name='asdf', expected_exception=MandatoryKeyException),
    KeyExMethTC(object_to_validate={'zxcv': None}, key_name='asdf', expected_exception=MandatoryKeyException),
    KeyExMethTC(id='reversed validation',
                object_to_validate={'asdf': None}, key_name='asdf', reversed_validation=True,
                expected_exception=ForbiddenKeyException),
    KeyExMethTC(id='including iterative validations',
                object_to_validate={'asdf': 123}, key_name='asdf',
                validations={
                    'type': {'expected_type': str},
                }, expected_exception=MandatoryTypeException),
    KeyExMethTC(id='including iterative validations',
                object_to_validate={'asdf': 123}, key_name='asdf',
                validations={
                    'type': {'expected_type': str},
                }, expected_exception=MandatoryTypeException),
    KeyExMethTC(id='iterative validations are reversed',
                object_to_validate={'asdf': 123}, key_name='asdf',
                validations={
                    'type': {'expected_type': int, 'reversed_validation': True}
                }, expected_exception=ForbiddenTypeException),
]])
def test_key_existence_failure(new_instance, test_case: KeyExistenceMethodTestCase):
    try:
        new_instance.key_existence(test_case.object_to_validate, test_case.key_name, test_case.validations,
                                   test_case.reversed_validation)
    except:
        assert isinstance(sys.exception(), test_case.expected_exception)
    else:
        pytest.fail(f'Exception \"{test_case.expected_exception.__name__}\" was expected, but found none')


@pytest.mark.parametrize('test_case', [pytest.param(test_case, id=test_case.id) for test_case in [
    KeyExMethTC(id='plain (non-reversed) validation',
                object_to_validate={'asdf': None}, key_name='asdf'),
    KeyExMethTC(id='reversed validation',
                object_to_validate={'zxcv': None}, key_name='asdf', reversed_validation=True),
    KeyExMethTC(object_to_validate={}, key_name='asdf', reversed_validation=True),
    KeyExMethTC(id='including iterative validations',
                object_to_validate={'asdf': 123}, key_name='asdf',
                validations={
                    'type': {'expected_type': int}
                }),
    KeyExMethTC(id='iterative validations are reversed',
                object_to_validate={'asdf': 123}, key_name='asdf',
                validations={
                    'type': {'expected_type': dict, 'reversed_validation': True}
                }),
]])
def test_key_existence_success(new_instance, test_case: KeyExistenceMethodTestCase):
    new_instance.key_existence(test_case.object_to_validate, test_case.key_name, test_case.validations,
                               test_case.reversed_validation)
