from vindi.handlers.base_handler import BaseVindiHandler


class ChargeHandler(BaseVindiHandler):
    @property
    def base_endpoint(self) -> str:
        return "/v1/charge/"
