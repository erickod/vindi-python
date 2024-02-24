from dataclasses import dataclass
from .config import Config

class Client:
    def __init__(self, api_key: str, environment:str = "sandbox") -> None:
        self._config = Config(api_key=api_key, environment = environment)

    @property
    def api_key(self) -> str:
        return self._config.api_key

    @property
    def environment(self) -> str:
        return self._config.environment
