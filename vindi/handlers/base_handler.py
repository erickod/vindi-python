from abc import ABC, abstractproperty
from typing import Callable, Literal
from vindi.config import Config
from vindi.http_client.http_response import HttpResponse
from vindi.http_client.protocols import HttpClient


class BaseVindiHandler(ABC):
    def __init__(self, http_client: HttpClient, config: Config) -> None:
        self._http_client = http_client
        self._config = config

    @abstractproperty
    def base_endpoint(self) -> str:
        pass

    async def request(
        self,
        method: Literal["get", "post", "put", "patch", "delete"],
        url: str,
        json={},
        files=None,
    ) -> HttpResponse:
        http_method: Callable = getattr(self._http_client, method)
        if self._config.environment == "sandbox":
            headers = {"authorization": self._config.get_api_key()}
            return await http_method(url=url, json=json, headers=headers, files=files)
        self._http_client.authenticate(
            type="basic", username=self._config.get_api_key(), password=""
        )
        return await http_method(url=url, json=json, headers={}, files=files)
