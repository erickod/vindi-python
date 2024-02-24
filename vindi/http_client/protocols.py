from typing import Protocol
from .http_response import HttpResponse


class HttpClient(Protocol):
    def authenticate(self, type: str, **kwargs) -> None:
        pass

    async def get(self, url: str, headers: dict[str, str] = {}) -> HttpResponse:
        pass

    async def post(
        self, url: str, json, files=None, headers: dict[str, str] = {}
    ) -> HttpResponse:
        pass

    async def put(self, url: str, json, headers: dict[str, str] = {}) -> HttpResponse:
        pass

    async def delete(self, url: str, headers: dict[str, str] = {}) -> HttpResponse:
        pass

    async def patch(self, url: str, json, headers: dict[str, str] = {}) -> HttpResponse:
        pass
