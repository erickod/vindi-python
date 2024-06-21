from dataclasses import dataclass
from typing import Any
from vindi.errors import ApiError, ParamError
from vindi.handlers.base_handler import BaseVindiHandler


class ChargeHandler(BaseVindiHandler):
    @property
    def base_endpoint(self) -> str:
        return "/v1/charges/"

    async def charge(self, id, gateway_token: str):
        payload = {'gateway_token': gateway_token}
        output = await self.request(
            method="post",
            url=self._config.get_environ_url() + self.base_endpoint + f'{id}/charge/',
            json=payload,
        )
        if "errors" in output.json:
            raise ApiError(output.json.get("errors", "unknown error"))
        return output
