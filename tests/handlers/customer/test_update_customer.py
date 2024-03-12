import pytest
from vindi.handlers.customer_handler import CustomerHandler, Customer, Address
from vindi.config import Config
from vindi.http_client.fake_http_client import FakeHttpClient
from vindi.errors import ApiError


address = Address(
    street="Rua dos bobos",
    neighborhood="bairro ABC",
    city="city",
    state="GO",
    zipcode="72120020",
    complement="",
    number="1",
    country="BR",
)


async def test_ensure_update_customer_calls_the_http_client_method() -> None:
    http_client = FakeHttpClient()
    sut = CustomerHandler(
        http_client=http_client, config=Config(api_key="", environment="sandbox")
    )
    customer = Customer("John Doe", "mail@mail.com", "04071239468", address)
    await sut.update_customer(customer, id=1)
    assert http_client.put_called


async def test_ensure_update_customer_raises_when_api_return_errors() -> None:
    http_client = FakeHttpClient(output_payload={"errors": [{"detail": "any error"}]})
    sut = CustomerHandler(
        http_client=http_client, config=Config(api_key="", environment="sandbox")
    )
    customer = Customer("John Doe", "mail@mail.com", "04071239468", address)
    with pytest.raises(ApiError):
        await sut.create_customer(customer)
