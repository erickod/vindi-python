from typing import Any
import httpx
from .http_response import HttpResponse


class HttpxClient:
    def __init__(self) -> None:
        self.__auth = None

    def authenticate(self, type: str, **kwargs) -> None:
        self.__auth = self.__get_auth(type=type, **kwargs)

    def __get_auth(self, type: str, **kwargs) -> Any:
        if type.lower() == "basic":
            return httpx.BasicAuth(
                username=kwargs.get("username", ""), password=kwargs.get("password", "")
            )
        return None

    async def get(
        self, url: str, headers: dict[str, str] = {}, **kwargs
    ) -> HttpResponse:
        async with httpx.AsyncClient() as client:
            response = await client.get(url=url, headers=headers, auth=self.__auth)
            return HttpResponse(headers=response.headers, json=response.json())

    async def post(
        self, url: str, json, files=None, headers: dict[str, str] = {}, **kwargs
    ) -> HttpResponse:
        async with httpx.AsyncClient() as client:
            if files:
                response = await client.post(
                    url=url, data=json, files=files, headers=headers, auth=self.__auth
                )
                return HttpResponse(headers=response.headers, json=response.json())
            response = await client.post(
                url=url, json=json, files=files, headers=headers, auth=self.__auth
            )
            return HttpResponse(headers=response.headers, json=response.json())

    async def put(
        self, url: str, json, headers: dict[str, str] = {}, **kwargs
    ) -> HttpResponse:
        async with httpx.AsyncClient() as client:
            response = await client.put(
                url=url, json=json, headers=headers, auth=self.__auth
            )
            return HttpResponse(headers=response.headers, json=response.json())

    async def delete(
        self, url: str, headers: dict[str, str] = {}, **kwargs
    ) -> HttpResponse:
        async with httpx.AsyncClient() as client:
            response = await client.delete(url=url, headers=headers, auth=self.__auth)
            return HttpResponse(headers=response.headers, json=response.json())

    async def patch(
        self, url: str, json, headers: dict[str, str] = {}, **kwargs
    ) -> HttpResponse:
        async with httpx.AsyncClient() as client:
            response = await client.patch(
                url=url, json=json, headers=headers, auth=self.__auth
            )
            return HttpResponse(headers=response.headers, json=response.json())
