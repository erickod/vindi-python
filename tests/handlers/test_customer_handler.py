from vindi.handlers.customer import CustomerHandler, Customer
from vindi.config import Config
from vindi.http_client.fake_http_client import FakeHttpClient


async def test_ensure_create_customer_calls_the_http_client_method() -> None:
    http_client = FakeHttpClient()
    sut = CustomerHandler(
        http_client=http_client, config=Config(api_key="", environment="sandbox")
    )
    customer = Customer("John Doe", "mail@mail.com", "04071239468")
    customer.add_address(
        "Rua Senador Sócrates Diniz", "Dom Pedro II", "Anápolis", "GO", "75140070"
    )
    await sut.create_customer(customer)
    assert http_client.post_called
