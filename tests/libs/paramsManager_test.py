import pytest

from source.libs.params_manager import ParamsManager


@pytest.fixture
def new_instance() -> ParamsManager:
    return ParamsManager()


def test_instantiation_success(new_instance: ParamsManager):
    assert isinstance(new_instance, ParamsManager)
