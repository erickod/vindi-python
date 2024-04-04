from typing import Literal

from vindi.handlers.customer_handler import CustomerHandler
from vindi.handlers.plan_handler import PlanHandler
from vindi.handlers.product_handler import ProductHandler
from vindi.handlers.subscription import SubscriptionHandler
from vindi.http_client.httpx_client import HttpxClient
from vindi.http_client.protocols import HttpClient
from .config import Config


class Client:
    def __init__(
        self,
        api_key: str,
        environment: Literal["prod", "sandbox"] = "sandbox",
        http_client: HttpClient = HttpxClient(),
    ) -> None:
        self._config = Config(api_key=api_key, environment=environment)
        self._http_client = http_client

    @property
    def api_key(self) -> str:
        return self._config.api_key

    @property
    def environment(self) -> str:
        return self._config.environment

    @property
    def customer(self) -> CustomerHandler:
        return CustomerHandler(http_client=self._http_client, config=self._config)

    @property
    def product(self) -> ProductHandler:
        return ProductHandler(http_client=self._http_client, config=self._config)

    @property
    def plan(self) -> PlanHandler:
        return PlanHandler(http_client=self._http_client, config=self._config)

    @property
    def subscription(self) -> SubscriptionHandler:
        return SubscriptionHandler(http_client=self._http_client, config=self._config)
