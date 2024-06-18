from dataclasses import dataclass
from enum import Enum
from typing import Any
from vindi.errors import ApiError
from vindi.handlers.base_handler import BaseVindiHandler


class DiscountType(Enum):
    percentage = "percentage"
    amount = "amount"
    quantity = "quantity"


@dataclass
class Discount:
    product_item_id: int | None
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
            "product_item_id": self.product_item_id,
            "discount_type": self.discount_type.value,
            "percentage": self.percentage,
            "amount": self.amount,
            "quantity": self.quantity,
            "cycles": self.cycles,
        }
        return {k: v for k, v in repr.items() if v is not None}


class DiscountHandler(BaseVindiHandler):
    
    @property
    def base_endpoint(self) -> str:
        return "/v1/discounts/"

    async def apply_discount(self, discount: Discount):
        output = await self.request(
            method="post",
            url=self._config.get_environ_url() + self.base_endpoint,
            json=discount.asdict
        )
        if "errors" in output.json:
            raise ApiError(output.json.get("errors", "unknown error"))
        return output
    
    async def get_discount_by_id(self, id: str):
        output = await self.request(
            method="get",
            url=self._config.get_environ_url() + self.base_endpoint + id,
        )
        if "errors" in output.json:
            raise ApiError(output.json.get("errors", "unknown error"))
        return output
    
    async def delete_discount_by_id(self, id: str):
        output = await self.request(
            method="delete",
            url=self._config.get_environ_url() + self.base_endpoint + id,
        )
        if "errors" in output.json:
            raise ApiError(output.json.get("errors", "unknown error"))
        return output
