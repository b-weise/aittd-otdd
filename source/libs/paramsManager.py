import copy
import dataclasses
from collections.abc import Sized
from dataclasses import dataclass
from functools import reduce
from typing import Any, Type

from source.libs.helper import Helper
from source.structs.params import (TrainingParamsCombinations as TrainParamsCombs,
                                   TrainingParams as TrainParams, LayerParams)


@dataclass
class FieldNames:
    Hash: str = 'Hash'
    LayerStack: str = 'LayerStack'


class ParamsManager:
    """
    A utility class that provides common functionality for parameter-related objects,
    such as TrainingParamsCombinations, LayerParamsCombinations, TrainingParams, and LayerParams.
    """

    def __init__(self, field_names: Type[FieldNames] = FieldNames):
        self.__field_name = field_names

    @staticmethod
    def __clear_empty_keys(dictionary: dict) -> dict:
        """
        Removes any key whose value is either None or an empty container.
        :param dictionary: The dict to prune.
        :return: A pruned deepcopy of the provided dict.
        """
        mutable_dict = copy.deepcopy(dictionary)
        for key, values in zip(dictionary.keys(), dictionary.values()):
            if values is None or (isinstance(values, Sized) and len(values) == 0):
                del mutable_dict[key]
        return mutable_dict

    @staticmethod
    def __generate_cartesian_product(factors: dict[str | int, list[Any]]) -> list[dict[str | int, Any]]:
        """
        Computes the Cartesian product of the provided factors, transforming a dict of value lists
        into a list of dicts, each containing one possible combination of values.
        :param factors: A dict mapping keys to lists of values.
        :return: A list of dicts, each representing a unique combination of values.
        """
        total_combs = reduce(lambda aggregation, item: (aggregation * len(item)), factors.values(), 1)
        product = []
        for counter in range(total_combs):
            quotient = counter
            element = {}
            for key, values in zip(factors.keys(), factors.values()):
                quotient, remainder = divmod(quotient, len(values))
                element[key] = values[remainder]
            product.append(element)
        return product

    @staticmethod
    def __build_stack(stack: dict[int, dict[str, Any]]) -> dict[int, LayerParams]:
        """
        Builds a stack of layer objects from their dict representations.
        :param stack: A plain stack where each key is an index and each value is a dict representing a layer.
        :return: A new dict with the same structure, where each layer has been replaced by a LayerParams object.
        """
        built_stack = {}
        for key, values in zip(stack.keys(), stack.values()):
            built_stack[key] = LayerParams(**values)
        return built_stack

    def __build_objects(self, unfolded_params: list[dict[str, Any]]) -> list[TrainParams]:
        """
        Constructs TrainParams objects from their corresponding dict representations and computes an MD5 hash for each.
        :param unfolded_params: A list of dicts representing TrainParams.
        :return: A list of TrainParams instances.
        """
        built_objects = []
        for plain_params in unfolded_params:
            plain_params[self.__field_name.Hash] = Helper.generate_hash(plain_params)
            plain_params[self.__field_name.LayerStack] = self.__build_stack(plain_params[self.__field_name.LayerStack])
            built_objects.append(TrainParams(**plain_params))
        return built_objects

    def unfold(self, training_combs: TrainParamsCombs) -> list[TrainParams]:
        """
        Expands a TrainParamsCombs instance into a Cartesian product of TrainParams combinations.
        :param training_combs: A TrainParamsCombs instance.
        :return: A list of TrainParams instances, each representing a unique combination of parameter values.
        """
        plain_combs = dataclasses.asdict(training_combs)
        mutable_combs = copy.deepcopy(plain_combs)
        for key, values in zip(plain_combs.keys(), plain_combs.values()):
            match key:
                case self.__field_name.LayerStack:
                    unfolded_stacks = []
                    for plain_stack_combs in values:
                        unfolded_layers_stack = {}
                        for layer_index in range(len(plain_stack_combs)):
                            plain_layer_combs = plain_stack_combs[layer_index]
                            sanitized_layer_combs = self.__clear_empty_keys(plain_layer_combs)
                            unfolded_layer = self.__generate_cartesian_product(sanitized_layer_combs)
                            unfolded_layers_stack[layer_index] = unfolded_layer
                        unfolded_stacks.extend(self.__generate_cartesian_product(unfolded_layers_stack))
                    mutable_combs[key] = unfolded_stacks
                    break
        unfolded_params = self.__generate_cartesian_product(mutable_combs)
        return self.__build_objects(unfolded_params)
