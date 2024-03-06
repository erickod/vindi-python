from vindi.handlers.customer_handler import Address, Customer


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


async def test_add_phone_to_the_customer() -> None:
    sut = Customer(
        "John Doe",
        "mail@mail.com",
        "04071239468",
        code="EXTERNAL_API_CODE",
        address=address,
    )
    sut.add_phone("mobile", number="61999999999")
