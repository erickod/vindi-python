import pytest
from vindi.handlers.customer import CustomerHandler, Customer, Address
from vindi.config import Config
from vindi.http_client.fake_http_client import FakeHttpClient
from vindi.errors import ApiError


address = Address(
    street="Rua dos bobos",
    neighborhood="bairro ABC",
    city="city",
    zipcode="72120020",
    complement="",
    number="1",
    country="BR",
)


async def test_ensure_create_customer_calls_the_http_client_method() -> None:
    http_client = FakeHttpClient()
    sut = CustomerHandler(
        http_client=http_client, config=Config(api_key="", environment="sandbox")
    )
    customer = Customer("John Doe", "mail@mail.com", "04071239468", address)
    await sut.create_customer(customer)
    assert http_client.post_called


async def test_ensure_create_customer_raises_when_api_return_errors() -> None:
    http_client = FakeHttpClient(output_payload={"errors": [{"detail": "any error"}]})
    sut = CustomerHandler(
        http_client=http_client, config=Config(api_key="", environment="sandbox")
    )
    customer = Customer("John Doe", "mail@mail.com", "04071239468", address)
    with pytest.raises(ApiError):
        await sut.create_customer(customer)


async def test_ensure_clist_customer_raises_when_api_return_errors() -> None:
    http_client = FakeHttpClient(output_payload={"errors": [{"detail": "any error"}]})
    sut = CustomerHandler(
        http_client=http_client, config=Config(api_key="", environment="sandbox")
    )
    with pytest.raises(ApiError):
        await sut.list_customers()
