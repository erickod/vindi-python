from dataclasses import dataclass
from typing import Literal


@dataclass(frozen=True)
class Config:
    api_key: str
    environment: Literal["sandbox", "prod"]

    def __post_init__(self) -> None:
        ALLOWED_ENVIRONMENTS = ("prod", "sandbox")
        if not isinstance(self.api_key, str):
            raise ValueError(f"api key must be a str, got {type(self.api_key)}")
        if not isinstance(self.environment, str):
            raise ValueError(f"environment must be a str, got {type(self.environment)}")
        if self.environment not in ALLOWED_ENVIRONMENTS:
            raise ValueError(
                f"environment {self.environment} doenst exist. The options are {ALLOWED_ENVIRONMENTS}"
            )

    def get_environ_url(self) -> str:
        if self.environment == "prod":
            return "https://app.vindi.com.br/api"
        return "https://sandbox-app.vindi.com.br/api"

    def get_api_key(self) -> str:
        return self.api_key
