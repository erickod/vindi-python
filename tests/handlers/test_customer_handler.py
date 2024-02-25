from vindi.handlers.customer import CustomerHandler, Customer, Address
from vindi.config import Config
from vindi.http_client.fake_http_client import FakeHttpClient


address = Address(
    street="Rua dos bobos",
    neighborhood="bairro ABC",
    city="city",
    zipcode="72120020",
    complement="",
    number="1",
    country="BR",
)


async def test_customer_is_instantiated_with_right_params() -> None:
    sut = Customer(
        "John Doe",
        "mail@mail.com",
        "04071239468",
        code="EXTERNAL_API_CODE",
        address=address,
    )
    assert sut.name == "John Doe"
    assert sut.email == "mail@mail.com"
    assert sut.documentation == "04071239468"
    assert sut.code == "EXTERNAL_API_CODE"
    assert sut.address == address


async def test_ensure_create_customer_calls_the_http_client_method() -> None:
    http_client = FakeHttpClient()
    sut = CustomerHandler(
        http_client=http_client, config=Config(api_key="", environment="sandbox")
    )
    customer = Customer("John Doe", "mail@mail.com", "04071239468", address)
    await sut.create_customer(customer)
    assert http_client.post_called
