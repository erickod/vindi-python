from typing import Literal
from .config import Config

class Client:
    def __init__(self, api_key: str, environment:Literal["prod", "sandbox"] = "sandbox") -> None:
        self._config = Config(api_key=api_key, environment = environment)

    @property
    def api_key(self) -> str:
        return self._config.api_key

    @property
    def environment(self) -> str:
        return self._config.environment
