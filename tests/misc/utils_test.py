import copy
import dataclasses
from collections.abc import Iterable, Callable
from dataclasses import dataclass
from functools import partial
from types import UnionType
from typing import Any

import pytest

from source.libs.baseTestCase import BaseTestCase
from source.misc.utils import (Validation, ForbiddenTypeException, MandatoryTypeException, MinimumLengthException,
                               MaximumLengthException, InvalidRangeLengthException, InvalidRangeValuesException,
                               ForbiddenKeyException, MandatoryKeyException)

STRS = ['', 'aaa', 'abcdefghijklmnopqrstuvwxyz', '0123456789', ',.;:<>()[]{}']
INTS = [0, 1, 111, 222, 9999999]
FLOATS = [0.0, 0.5, 1.0, 1.5, 9.9, 9999999.9]
BOOLS = [True, False]
DICTS = [{}, {'a': 0}, {'b': ''}, {'c': []}, {'d': True}, {'a': 0, 'b': '', 'c': [], 'd': True}]
SETS = [set(), {0}, {''}, {True}, {0, '', True}]
LISTS = [[], [0], [''], [[]], [True], [0, '', [], True]]
TUPLES = [(), (0,), ('',), ([],), (True,), (0, '', [], True)]
RANGES = [range(0), range(9), range(11, 22), range(11, 99, 11)]
LAMBDAS = [lambda a: a, lambda a, b: (a, b)]
TYPES = [str, int, float, bool, dict, set, list, tuple, range, Callable, type, UnionType, Iterable]
UNIONTYPES = [str | int, int | float, float | bool, bool | dict, dict | set, set | list, list | tuple, tuple | range,
              range | Callable, Callable | type, type | UnionType, UnionType | str]
ITERABLES = STRS + DICTS + SETS + LISTS + TUPLES + RANGES
CALLABLES = LAMBDAS + TYPES
LITERALS = STRS + INTS + FLOATS + BOOLS + DICTS + SETS + LISTS + TUPLES + RANGES + LAMBDAS + TYPES + UNIONTYPES
TYPES_LITERALS_ZIP = [TYPES,
                      [STRS, INTS, FLOATS, BOOLS, DICTS, SETS, LISTS, TUPLES, RANGES, CALLABLES, TYPES, UNIONTYPES,
                       ITERABLES]]
UNIONTYPES_LITERALS_ZIP = [UNIONTYPES,
                           [STRS + INTS, INTS + FLOATS, FLOATS + BOOLS, BOOLS + DICTS, DICTS + SETS, SETS + LISTS,
                            LISTS + TUPLES, TUPLES + RANGES, RANGES + LAMBDAS, LAMBDAS + TYPES, TYPES + UNIONTYPES,
                            UNIONTYPES + STRS]]


def diff(list_a: list, list_b: list) -> list:
    """
    Subtracts list_b from list_a.
    :param list_a: The minuend.
    :param list_b: The subtrahend.
    :return: The result.
    """
    return list(filter(lambda item: (item not in list_b), list_a))


@pytest.fixture
def new_instance():
    return Validation()


@dataclass
class TypeMethodTestCase(BaseTestCase):
    object_to_validate: Any = None
    expected_type: Any = None
    reversed_validation: Any = False


def generate_match_related_test_cases(test_case_builder: Callable,
                                      match_types: bool,
                                      **kwargs):
    """
    Generates a test case for every single combination of a given type (or UnionType) and its respective literals,
    ensuring that either all or none of them match.
    :param test_case_builder: A builder used to generate each individual test case.
    :param match_types: A flag indicating whether each type (or UnionType) should match all of its respective literals,
    or none of them.
    :return: A list containing all generated test cases.
    """
    cases_list = []
    for zipped_lists in [TYPES_LITERALS_ZIP, UNIONTYPES_LITERALS_ZIP]:
        local_zipped_lists = copy.deepcopy(zipped_lists)
        if not match_types:
            types_list, literals_lists = local_zipped_lists
            offset = 2
            # An offset of 2 ensures that no types (or UnionTypes) are paired with compatible literals.
            for iteration in range(offset):
                last_list = literals_lists.pop()
                literals_lists.insert(0, last_list)
            local_zipped_lists = [types_list, literals_lists]
        for type_item, literals_list in zip(*local_zipped_lists):
            for literal_item in literals_list:
                cases_list.append(test_case_builder(literal_item, type_item, **kwargs))
    return cases_list


TypeMethTC = TypeMethodTestCase

generate_match_TypeMethTCs = partial(generate_match_related_test_cases,
                                     lambda literal_val, type_val, **kwargs: (
                                         TypeMethTC(object_to_validate=literal_val,
                                                    expected_type=type_val,
                                                    reversed_validation=kwargs.get('reversed_validation', False),
                                                    expected_exception=kwargs.get('expected_exception', None))
                                     ))


@pytest.mark.parametrize('test_case', [pytest.param(test_case, id=test_case.id) for test_case in [
    TypeMethTC(id='wrong expected_type type',
               object_to_validate='', expected_type='', expected_exception=MandatoryTypeException),
    *[TypeMethTC(object_to_validate='', expected_type=non_type_literal, expected_exception=MandatoryTypeException)
      for non_type_literal in diff(LITERALS, TYPES + UNIONTYPES)],
    TypeMethTC(id='wrong reversed_validation type',
               object_to_validate='', expected_type=str, reversed_validation='',
               expected_exception=MandatoryTypeException),
    *[TypeMethTC(object_to_validate='', expected_type=str, reversed_validation=non_bool_literal,
                 expected_exception=MandatoryTypeException)
      for non_bool_literal in diff(LITERALS, BOOLS)],
    TypeMethTC(id='plain (non-reversed) mismatching types',
               object_to_validate='', expected_type=int, expected_exception=MandatoryTypeException),
    *generate_match_TypeMethTCs(False, expected_exception=MandatoryTypeException),
    TypeMethTC(id='reversed matching types',
               object_to_validate='', expected_type=str, reversed_validation=True,
               expected_exception=ForbiddenTypeException),
    *generate_match_TypeMethTCs(True, reversed_validation=True, expected_exception=ForbiddenTypeException),
    TypeMethTC(id='specifing multiple types',
               object_to_validate='', expected_type=int | float, expected_exception=MandatoryTypeException),
    *[TypeMethTC(object_to_validate=non_float_callable_literal, expected_type=float | Callable,
                 expected_exception=MandatoryTypeException)
      for non_float_callable_literal in diff(LITERALS, FLOATS + CALLABLES)],
    *[TypeMethTC(object_to_validate=non_dict_list_literal, expected_type=dict | list,
                 expected_exception=MandatoryTypeException)
      for non_dict_list_literal in diff(LITERALS, DICTS + LISTS)],
    *[TypeMethTC(object_to_validate=non_iterable_bool_literal, expected_type=Iterable | bool,
                 expected_exception=MandatoryTypeException)
      for non_iterable_bool_literal in diff(LITERALS, ITERABLES + BOOLS)],
    TypeMethTC(id='specifing multiple types, reversed',
               object_to_validate='', expected_type=str | list, reversed_validation=True,
               expected_exception=ForbiddenTypeException),
    *[TypeMethTC(object_to_validate=set_uniontype_literal, expected_type=set | UnionType, reversed_validation=True,
                 expected_exception=ForbiddenTypeException)
      for set_uniontype_literal in SETS + UNIONTYPES],
    *[TypeMethTC(object_to_validate=str_bool_literal, expected_type=str | bool, reversed_validation=True,
                 expected_exception=ForbiddenTypeException)
      for str_bool_literal in STRS + BOOLS],
    *[TypeMethTC(object_to_validate=callable_iterable_literal, expected_type=Callable | Iterable,
                 reversed_validation=True,
                 expected_exception=ForbiddenTypeException)
      for callable_iterable_literal in CALLABLES + ITERABLES],
]])
def test_type_failure(new_instance, test_case: TypeMethodTestCase):
    with pytest.raises(test_case.expected_exception):
        new_instance.type(test_case.object_to_validate, test_case.expected_type, test_case.reversed_validation)


@pytest.mark.parametrize('test_case', [pytest.param(test_case, id=test_case.id) for test_case in [
    TypeMethTC(id='plain (non-reversed) matching types',
               object_to_validate={}, expected_type=dict),
    TypeMethTC(object_to_validate=True, expected_type=int),  # WATCH OUT: bool is a subclass of int
    TypeMethTC(object_to_validate=type, expected_type=Callable),  # WATCH OUT: types are callables
    *generate_match_TypeMethTCs(True),
    TypeMethTC(id='reversed mismatching types',
               object_to_validate='aaa', expected_type=dict, reversed_validation=True),
    *generate_match_TypeMethTCs(False, reversed_validation=True),
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
    *[LengthMethTC(object_to_validate=non_iterable_literal, expected_range=(4, None),
                   expected_exception=MandatoryTypeException)
      for non_iterable_literal in diff(LITERALS, ITERABLES)],
    LengthMethTC(id='wrong range type',
                 object_to_validate=[], expected_range=2, expected_exception=MandatoryTypeException),
    *[LengthMethTC(object_to_validate=[], expected_range=non_tuple_literal, expected_exception=MandatoryTypeException)
      for non_tuple_literal in diff(LITERALS, TUPLES)],
    LengthMethTC(id='wrong range element type',
                 object_to_validate='asdf', expected_range=('', None), expected_exception=MandatoryTypeException),
    *[LengthMethTC(object_to_validate='asdf', expected_range=(non_int_literal, None),
                   expected_exception=MandatoryTypeException)
      for non_int_literal in diff(LITERALS, INTS)],
    *[LengthMethTC(object_to_validate='asdf', expected_range=(None, non_int_literal),
                   expected_exception=MandatoryTypeException)
      for non_int_literal in diff(LITERALS, INTS)],
    LengthMethTC(id='wrong range length',
                 object_to_validate=[], expected_range=(), expected_exception=InvalidRangeLengthException),
    *[LengthMethTC(object_to_validate='asdf', expected_range=wrong_length_tuple,
                   expected_exception=InvalidRangeLengthException)
      for wrong_length_tuple in [(1,), (1, 2, 3), (1, 2, 3, 4), (1, 2, 3, 4, 5)]],
    LengthMethTC(id='object too long',
                 object_to_validate=[1, 2, 3], expected_range=(1, 3), expected_exception=MaximumLengthException),
    *[LengthMethTC(object_to_validate=[1, 2, 3], expected_range=low_max_length_range,
                   expected_exception=MaximumLengthException)
      for low_max_length_range in [(None, 3), (0, 1), (1, 2), (2, 3)]],
    LengthMethTC(id='object too short',
                 object_to_validate=[1, 2, 3], expected_range=(4, None), expected_exception=MinimumLengthException),
    *[LengthMethTC(object_to_validate=[1, 2, 3], expected_range=high_min_length_range,
                   expected_exception=MinimumLengthException)
      for high_min_length_range in [(4, None), (4, 5), (5, 8), (7, 8)]],
    LengthMethTC(id='invalid range values',
                 object_to_validate='asdf', expected_range=(3, 3), expected_exception=InvalidRangeValuesException),
    *[LengthMethTC(object_to_validate='asdf', expected_range=invalid_range_values,
                   expected_exception=InvalidRangeValuesException)
      for invalid_range_values in [(0, 0), (-1, -1), (1, 0), (5, 3), (8, 5)]],
]])
def test_length_failure(new_instance, test_case: LengthMethodTestCase):
    with pytest.raises(test_case.expected_exception):
        new_instance.length(test_case.object_to_validate, test_case.expected_range)


@pytest.mark.parametrize('test_case', [pytest.param(test_case, id=test_case.id) for test_case in [
    LengthMethTC(id='no range',
                 object_to_validate={}, expected_range=(None, None)),
    LengthMethTC(id='both limits are specified',
                 object_to_validate=[1, 2, 3], expected_range=(3, 4)),
    *[LengthMethTC(object_to_validate=[1, 2, 3], expected_range=both_limits_specified_range)
      for both_limits_specified_range in [(0, 4), (2, 6), (3, 8), (0, 9)]],
    *[LengthMethTC(object_to_validate=[1], expected_range=both_limits_specified_range)
      for both_limits_specified_range in [(1, 2), (0, 2), (1, 3)]],
    LengthMethTC(id='only one limit is specified',
                 object_to_validate=[1, 2, 3], expected_range=(None, 4)),
    *[LengthMethTC(object_to_validate=[1, 2, 3], expected_range=one_limit_specified_range)
      for one_limit_specified_range in [(None, 4), (None, 6), (3, None), (0, None)]],
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
    *[ItMethTC(objects=non_iterable_literal, validations={}, expected_exception=MandatoryTypeException)
      for non_iterable_literal in diff(LITERALS, ITERABLES)],
    ItMethTC(id='wrong validations type',
             objects=[], validations=1, expected_exception=MandatoryTypeException),
    *[ItMethTC(objects=[], validations=non_dict_literal, expected_exception=MandatoryTypeException)
      for non_dict_literal in diff(LITERALS, DICTS)],
    ItMethTC(id='type validation not passed',
             objects=[1, {}], validations={'type': {'expected_type': int | str}},
             expected_exception=MandatoryTypeException),
    *[ItMethTC(objects=[1, 2, 3, 4], validations={'type': {'expected_type': non_int_uniontype}},
               expected_exception=MandatoryTypeException)
      for non_int_uniontype in diff(UNIONTYPES, [str | int, int | float])],
    *[ItMethTC(objects=['a', 'b', non_str_literal, 'd'], validations={'type': {'expected_type': str}},
               expected_exception=MandatoryTypeException)
      for non_str_literal in diff(LITERALS, STRS)],
    *[ItMethTC(objects=['a', 'b', 'c', 'd'], validations={'type': {'expected_type': non_str_iterable_type}},
               expected_exception=MandatoryTypeException)
      for non_str_iterable_type in diff(TYPES, [str, Iterable])],
    ItMethTC(id='length validation not passed',
             objects=['asdf'], validations={'length': {'expected_range': (None, 4)}},
             expected_exception=MaximumLengthException),
    *[ItMethTC(objects=['asd', 'asdfgh', 'as'], validations={'length': {'expected_range': low_max_length_range}},
               expected_exception=MaximumLengthException)
      for low_max_length_range in [(None, 3), (0, 4), (0, 6), (2, 6)]],
    *[ItMethTC(objects=['asd', 'asdfgh', 'as'], validations={'length': {'expected_range': high_min_length_range}},
               expected_exception=MinimumLengthException)
      for high_min_length_range in [(5, None), (4, 7), (3, 8)]],
    ItMethTC(objects=['asd', 'asdfgh', 'as'], validations={'length': {'expected_range': (3, 7)}},
             expected_exception=MinimumLengthException),
    ItMethTC(id='multiple validations',
             objects=['asdf', 'asd', 'asdfgh'],
             validations={
                 'type': {'expected_type': str},
                 'length': {'expected_range': (3, 6)},
             }, expected_exception=MaximumLengthException),
    *[ItMethTC(objects=['asdf', 'asd', 'asdfgh'],
               validations={
                   'type': {'expected_type': str},
                   'length': {'expected_range': low_max_length_range}
               }, expected_exception=MaximumLengthException)
      for low_max_length_range in [(None, 3), (0, 4), (0, 6), (2, 6)]],
    *[ItMethTC(objects=['asdf', 'asd', 'asdfgh'],
               validations={
                   'type': {'expected_type': non_str_iterable_type},
                   'length': {'expected_range': (3, 7)}
               }, expected_exception=MandatoryTypeException)
      for non_str_iterable_type in diff(TYPES, [str, Iterable])],
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
    *[ItMethTC(objects=[non_compliant_dict], validations={'key_existence': {'key_name': 'asdf'}},
               expected_exception=MandatoryKeyException)
      for non_compliant_dict in DICTS],
    ItMethTC(id='reversing key_existence validation',
             objects=[{'bbb': 111, 'bbb': 222, 'bbb': 333}],
             validations={
                 'key_existence': {'key_name': 'bbb', 'reversed_validation': True},
             }, expected_exception=ForbiddenKeyException),
    *[ItMethTC(objects=non_compliant_dicts,
               validations={
                   'key_existence': {'key_name': 'ccc', 'reversed_validation': True}
               }, expected_exception=ForbiddenKeyException)
      for non_compliant_dicts in [
          [{'cccc': 111}, {'ccc': 111}, {'cc': 111}, {'c': 111}],
          [{'c': 111}, {'cc': 111}, {'ccc': 111}, {'cccc': 111}],
          [{'cc': 111}, {'ccc': 111}, {'cccc': 111}, {'ccccc': 111}],
      ]],
    ItMethTC(id='including iterative validations',
             objects=[{'aaa': 'zzz'}, {'aaa': 222}, {'aaa': [1, 2, 3]}],
             validations={
                 'key_existence': {'key_name': 'aaa', 'validations': {'type': {'expected_type': int}}},
             }, expected_exception=MandatoryTypeException),
    *[ItMethTC(objects=[{'aaa': 'zzz'}, {'aaa': 222}, {'aaa': [1, 2, 3]}],
               validations={
                   'key_existence': {'key_name': 'aaa', 'validations': {'type': {'expected_type': type_item}}},
               }, expected_exception=MandatoryTypeException)
      for type_item in TYPES],
    *[ItMethTC(objects=[{'aaa': [4, 4, 4, 4]}, {'aaa': [5, 5, 5, 5, 5]}, {'aaa': [3, 3, 3]}],
               validations={
                   'key_existence': {
                       'key_name': 'aaa',
                       'validations': {
                           'type': {'expected_type': Iterable},
                           'length': {'expected_range': high_min_length_range},
                       },
                   },
               }, expected_exception=MinimumLengthException)
      for high_min_length_range in [(4, None), (4, 6), (5, 7), (6, 8)]],
]])
def test_iterate_failure(new_instance, test_case: IterateMethodTestCase):
    with pytest.raises(test_case.expected_exception):
        new_instance.iterate(test_case.objects, test_case.validations)


@pytest.mark.parametrize('test_case', [pytest.param(test_case, id=test_case.id) for test_case in [
    ItMethTC(id='empty params',
             objects=[], validations={}),
    ItMethTC(id='matching types',
             objects=[1, 2], validations={'type': {'expected_type': int}}),
    *[ItMethTC(objects=matching_values, validations={'type': {'expected_type': matching_type}})
      for matching_type, matching_values in zip(*TYPES_LITERALS_ZIP)],
    *[ItMethTC(objects=matching_values, validations={'type': {'expected_type': matching_uniontype}})
      for matching_uniontype, matching_values in zip(*UNIONTYPES_LITERALS_ZIP)],
    ItMethTC(id='matching lengths',
             objects=['asdf', 'asd', 'asdfgh'], validations={'length': {'expected_range': (3, 7)}}),
    *[ItMethTC(objects=['asdf', 'asd', 'asdfgh'], validations={'length': {'expected_range': compliant_range}})
      for compliant_range in [(2, 7), (1, 7), (0, 7), (3, 8), (3, 9), (None, 7), (3, None)]],
    ItMethTC(id='matching multiple validations',
             objects=['asdf', 'asd', 'asdfgh'],
             validations={
                 'type': {'expected_type': str},
                 'length': {'expected_range': (3, 7)}
             }),
    *[ItMethTC(objects=compliant_values,
               validations={
                   'length': {'expected_range': (3, 7)}
               })
      for compliant_values in [
          [[1, 2, 3], 'asdf', [1, 2, 3, 4, 5, 6]],
          [[1, 2, 3, 4], (1, 2, 3, 4), {1, 2, 3, 4, 5}],
          [[1, 2, 3, 4, 5, 6], 'asdfgh'],
      ]],
    ItMethTC(id='matching key_existence',
             objects=[{'aaa': 111}, {'aaa': 222}, {'aaa': 333}],
             validations={
                 'key_existence': {'key_name': 'aaa'},
             }),
    *[ItMethTC(objects=compliant_values,
               validations={
                   'key_existence': {'key_name': 'aa'},
               })
      for compliant_values in [
          [{'aaa': 111, 'a': 111, 'aa': 111}, {'a': 222, 'aa': 222, 'aaa': 222}, {'aa': 333}],
          [{'aa': 111, 'aaa': 111, 'aaaa': 111}, {'cc': 222, 'aa': 222, 'bb': 222}],
      ]],
    ItMethTC(id='matching reversed key_existence',
             objects=[{'aaa': 111}, {'aaa': 222}, {'aaa': 333}],
             validations={
                 'type': {'expected_type': dict},
                 'key_existence': {'key_name': 'bbb', 'reversed_validation': True},
             }),
    *[ItMethTC(objects=compliant_values,
               validations={
                   'key_existence': {'key_name': 'aa', 'reversed_validation': True},
               })
      for compliant_values in [
          [{'aaa': 111, 'a': 111, 'aaaa': 111}, {'a': 222, 'a': 222, 'aaa': 222}, {'a': 333}],
          [{'aaa': 111, 'aaa': 111, 'aaaa': 111}, {'cc': 222, 'dd': 222, 'bb': 222}],
      ]],
    ItMethTC(id='various iterable types as objects',
             objects=({'aaa': 111}, {'aaa': 222}, {'aaa': 333}),
             validations={
                 'type': {'expected_type': dict},
                 'key_existence': {'key_name': 'aaa'},
             }),
    *[ItMethTC(objects=iterable_literals, validations={})
      for iterable_literals in ITERABLES],
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

generate_match_KeyExMethTCs = partial(generate_match_related_test_cases,
                                      lambda literal_val, type_val, **kwargs: (
                                          KeyExMethTC(
                                              object_to_validate={'aaa': literal_val},
                                              key_name='aaa',
                                              validations={'type': {
                                                  'expected_type': type_val,
                                                  'reversed_validation': kwargs.get('reversed_iterative_validation',
                                                                                    False)
                                              }},
                                              reversed_validation=kwargs.get('reversed_validation', False),
                                              expected_exception=kwargs.get('expected_exception', None))
                                      ))


@pytest.mark.parametrize('test_case', [pytest.param(test_case, id=test_case.id) for test_case in [
    KeyExMethTC(id='wrong object type',
                object_to_validate='', key_name='asdf', expected_exception=MandatoryTypeException),
    *[KeyExMethTC(object_to_validate=non_dict_literal, key_name='asdf', expected_exception=MandatoryTypeException)
      for non_dict_literal in diff(LITERALS, DICTS)],
    KeyExMethTC(id='wrong key type',
                object_to_validate={}, key_name=1, expected_exception=MandatoryTypeException),
    *[KeyExMethTC(object_to_validate={}, key_name=non_str_literal, expected_exception=MandatoryTypeException)
      for non_str_literal in diff(LITERALS, STRS)],
    KeyExMethTC(id='wrong validations type',
                object_to_validate={}, key_name='asdf', validations=[], expected_exception=MandatoryTypeException),
    *[KeyExMethTC(object_to_validate={}, key_name='asdf', validations=non_dict_literal,
                  expected_exception=MandatoryTypeException)
      for non_dict_literal in diff(LITERALS, DICTS)],
    KeyExMethTC(id='wrong reversed_validation type',
                object_to_validate={}, key_name='asdf', reversed_validation=1,
                expected_exception=MandatoryTypeException),
    *[KeyExMethTC(object_to_validate={}, key_name='asdf', reversed_validation=non_bool_literal,
                  expected_exception=MandatoryTypeException)
      for non_bool_literal in diff(LITERALS, BOOLS)],
    KeyExMethTC(id='empty key string',
                object_to_validate={}, key_name='', expected_exception=MinimumLengthException),
    KeyExMethTC(id='plain (non-reversed) validation',
                object_to_validate={}, key_name='asdf', expected_exception=MandatoryKeyException),
    *[KeyExMethTC(object_to_validate=dict_literal, key_name='asdf', expected_exception=MandatoryKeyException)
      for dict_literal in DICTS],
    KeyExMethTC(id='reversed validation',
                object_to_validate={'asdf': None}, key_name='asdf', reversed_validation=True,
                expected_exception=ForbiddenKeyException),
    *[KeyExMethTC(object_to_validate=dict_literal, key_name=str_literal, reversed_validation=True,
                  expected_exception=ForbiddenKeyException)
      for dict_literal, str_literal in [
          ({'a': 1, 'b': 2}, 'b'), ({'a': None, 'b': None, 'c': None}, 'c'),
          ({'a': 1}, 'a'), ({'a': 1, 'aa': 1, 'aaa': 1, 'aaaa': 1}, 'aaa'),
      ]],
    KeyExMethTC(id='including iterative validations',
                object_to_validate={'asdf': 123}, key_name='asdf',
                validations={
                    'type': {'expected_type': str},
                }, expected_exception=MandatoryTypeException),
    *generate_match_KeyExMethTCs(False, expected_exception=MandatoryTypeException),
    KeyExMethTC(id='iterative validations are reversed',
                object_to_validate={'asdf': 123}, key_name='asdf',
                validations={
                    'type': {'expected_type': int, 'reversed_validation': True}
                }, expected_exception=ForbiddenTypeException),
    *generate_match_KeyExMethTCs(True, reversed_iterative_validation=True,
                                 expected_exception=ForbiddenTypeException),
]])
def test_key_existence_failure(new_instance, test_case: KeyExistenceMethodTestCase):
    with pytest.raises(test_case.expected_exception):
        new_instance.key_existence(test_case.object_to_validate, test_case.key_name, test_case.validations,
                                   test_case.reversed_validation)


@pytest.mark.parametrize('test_case', [pytest.param(test_case, id=test_case.id) for test_case in [
    KeyExMethTC(id='plain (non-reversed) validation',
                object_to_validate={' ': None}, key_name=' '),  # WATCH OUT: Whitespace is allowed
    *[KeyExMethTC(object_to_validate={str_literal: None}, key_name=str_literal)
      for str_literal in ['a', 'aaa', '1234', '.', '!@#']],
    KeyExMethTC(id='reversed validation',
                object_to_validate={}, key_name='a', reversed_validation=True),
    *[KeyExMethTC(object_to_validate={str_literal: None}, key_name=f'X{str_literal}X', reversed_validation=True)
      for str_literal in ['a', 'aaa', '1234', '.', '!@#']],
    KeyExMethTC(id='including iterative validations',
                object_to_validate={'asdf': 123}, key_name='asdf',
                validations={
                    'type': {'expected_type': int}
                }),
    *generate_match_KeyExMethTCs(True),
    KeyExMethTC(id='iterative validations are reversed',
                object_to_validate={'asdf': 123}, key_name='asdf',
                validations={
                    'type': {'expected_type': dict, 'reversed_validation': True}
                }),
    *generate_match_KeyExMethTCs(False, reversed_iterative_validation=True),
]])
def test_key_existence_success(new_instance, test_case: KeyExistenceMethodTestCase):
    new_instance.key_existence(test_case.object_to_validate, test_case.key_name, test_case.validations,
                               test_case.reversed_validation)
