import pytest
from vindi import Vindi
from vindi.handlers.customer import CustomerHandler


async def test_instantiation_params() -> None:
    sut = Vindi("APIKEY", "sandbox")
    assert sut.api_key == "APIKEY"
    assert sut.environment == "sandbox"


@pytest.mark.parametrize("handler_detail", [("customer", CustomerHandler)])
async def test_handler_access(handler_detail) -> None:
    sut = Vindi("APIKEY", "sandbox")
    handler = getattr(sut, handler_detail[0])
    handler_type = handler_detail[1]
    assert isinstance(handler, handler_type)
