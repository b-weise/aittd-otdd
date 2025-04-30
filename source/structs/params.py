from collections.abc import Sequence, Callable
from dataclasses import dataclass
from pathlib import Path
from typing import Optional

from source.structs.customTypes import DateRange


@dataclass
class LayerParams:
    Units: int
    KernelInitializer: Optional[Callable] = None
    KernelRegularizer: Optional[Callable] = None
    Activation: Optional[Callable] = None


@dataclass
class TrainingParams:
    Hash: str
    ColumnToPredict: str
    WindowWidth: int
    SetTrainingFlag: bool
    UseResidualWrapper: bool
    PrependBatchNormLayer: bool
    FitMaxEpochs: int
    FitPatience: int
    CompileLossFunction: Callable
    CompileOptimizer: Callable
    LayerStack: dict[int, LayerParams]
    DatasetPath: Path
    DatasetTimeFilter: DateRange
    DatasetShuffle: bool
    DatasetBatchSize: int


@dataclass
class LayerParamsCombinations:
    Units: Sequence[int]
    KernelInitializer: Optional[Sequence[Optional[Callable]]] = None
    KernelRegularizer: Optional[Sequence[Optional[Callable]]] = None
    Activation: Optional[Sequence[Optional[Callable]]] = None


@dataclass
class TrainingParamsCombinations:
    ColumnToPredict: Sequence[str]
    WindowWidth: Sequence[int]
    SetTrainingFlag: Sequence[bool]
    UseResidualWrapper: Sequence[bool]
    PrependBatchNormLayer: Sequence[bool]
    FitMaxEpochs: Sequence[int]
    FitPatience: Sequence[int]
    CompileLossFunction: Sequence[Callable]
    CompileOptimizer: Sequence[Callable]
    LayerStack: Sequence[dict[int, LayerParamsCombinations]]
    DatasetPath: Sequence[Path]
    DatasetTimeFilter: Sequence[DateRange]
    DatasetShuffle: Sequence[bool]
    DatasetBatchSize: Sequence[int]
