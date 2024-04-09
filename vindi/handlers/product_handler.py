from dataclasses import dataclass
from enum import Enum
from typing import Any
from uuid import UUID
from vindi.errors import ApiError
from vindi.handlers.base_handler import BaseVindiHandler


class DiscountType(Enum):
    percentage = "percentage"
    amount = "amount"
    quantity = "quantity"


@dataclass
class Discount:
    discount_type: DiscountType
    percentage: float | None = None
    value: float | int | None = None
    quantity: int | None = None
    cycles: int | None = None
    amount: float | None = None

    @property
    def asdict(self) -> dict:
        if self.discount_type.value == "amount":
            self.amount = self.value
        elif self.discount_type.value == "percentage":
            self.percentage = self.value
        elif self.discount_type.value == "quantity":
            self.quantity == self.value

        repr = {
            "discount_type": self.discount_type.value,
            "percentage": self.percentage,
            "amount": self.amount,
            "quantity": self.quantity,
            "cycles": self.cycles,
        }
        output = {k: v for k, v in repr.items() if v is not None}
        return output


@dataclass
class ProductItem:
    product_id: UUID
    price: float | None = None
    cycles: int | None = None
    quantity: int = 1
    discount: Discount | None = None

    @property
    def asdict(self) -> dict:
        repr = {
            "product_id": self.product_id,
            "cycles": self.cycles,
            "quantity": self.quantity,
            "pricing_schema": {"price": self.price, "schema_type": "per_unit"}
            if self.price
            else None,
            "discounts": [self.discount.asdict] if self.discount else None,
        }
        return {k: v for k, v in repr.items() if v is not None}


@dataclass
class Subscription:
    customer_id: UUID
    plan_id: UUID
    code: str
    payment_method_code: str
    product_items: list[ProductItem]
    installments: int = 1
    start_at: str | None = None
    payment_profile_id: str | None = None
    metadata: dict | None = None
    body: dict | None = None

    @property
    def asdict(self) -> dict[str, Any]:
        repr = {
            "plan_id": str(self.plan_id),
            "customer_id": str(self.customer_id),
            "code": self.code,
            "start_at": self.start_at,
            "payment_method_code": self.payment_method_code,
            "installments": self.installments,
            "metadata": {k: v for k, v in self.metadata.items()}
            if self.metadata
            else None,
            "body": {k: v for k, v in self.body} if self.body else None,
            "payment_profile": {"id": self.payment_profile_id}
            if self.payment_profile_id
            else None,
            "product_items": [p.asdict for p in self.product_items],
        }
        return {k: v for k, v in repr.items() if v is not None}


class SubscriptionHandler(BaseVindiHandler):
    @property
    def base_endpoint(self) -> str:
        return "/v1/subscriptions/"

    async def create_subscription(self, subscription: Subscription):
        output = await self.request(
            method="post",
            url=self._config.get_environ_url() + self.base_endpoint,
            json=subscription.asdict,
        )
        if "errors" in output.json:
            raise ApiError(output.json.get("errors", "unknown error"))
        return output

    async def update_subscription(self, subscription: Subscription, id):
        output = await self.request(
            method="put",
            url=self._config.get_environ_url() + self.base_endpoint + id,
            json=subscription.asdict,
        )
        if "errors" in output.json:
            raise ApiError(output.json.get("errors", "unknown error"))
        return output
