from typing import Any, Coroutine
from .http_response import HttpResponse
from .http_status import HttpStatus


class FakeHttpClient:
    def __init__(
        self, output_payload: Any = {}, output_status: HttpStatus = HttpStatus.OK
    ):
        self._output_payload = output_payload
        self._output_status = output_status
        self.get_called = False
        self.post_called = False
        self.put_called = False
        self.patch_called = False
        self.delete_called = False

    def authenticate(self, type: str, **kwargs) -> None:
        pass

    def _make_async(self, data) -> HttpResponse:
        return HttpResponse(
            status=self._output_status, headers={}, json=self._output_payload
        )

    async def get(self, url: str, headers: dict[str, str] = {}) -> HttpResponse:
        self.get_called = True
        return self._make_async(url)

    async def post(
        self, url: str, json, files=None, headers: dict[str, str] = {}
    ) -> HttpResponse:
        self.post_called = True
        return self._make_async(data=json)

    async def put(self, url: str, json, headers: dict[str, str] = {}) -> HttpResponse:
        self.put_called = True
        return self._make_async(data=json)

    async def delete(self, url: str, headers: dict[str, str] = {}) -> HttpResponse:
        self.delete_called = True
        return self._make_async(data={})

    async def patch(self, url: str, json, headers: dict[str, str] = {}) -> HttpResponse:
        self.patch_called = True
        return self._make_async(data=json)
