from vindi import Vindi

async def test_ensure_vindi_is_instantiated_with_right_params() -> None:
    sut = Vindi(api_key="any_valid_api_key", environment="sandbox")
    assert sut.api_key == "any_valid_api_key"
    assert sut.environment == "sandbox"
    
