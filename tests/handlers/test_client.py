from vindi import Vindi


async def test_instantiation_params() -> None:
    sut = Vindi("APIKEY", "sandbox")
    assert sut.api_key == "APIKEY"
    assert sut.environment == "sandbox"
