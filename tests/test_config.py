from vindi.config import Config
import pytest


async def test_ensure_config_raises_when_api_key_is_an_invalid_value() -> None:
    with pytest.raises(ValueError):
        Config(api_key=10000, environment="prod")


@pytest.mark.parametrize("environ", [10000, "any invalid str"])
async def test_ensure_config_raises_when_environment_is_an_invalid_value(
    environ,
) -> None:
    with pytest.raises(ValueError):
        Config(api_key="any_valid_api_key", environment=environ)
