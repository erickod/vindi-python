from dataclasses import dataclass
from typing import Any
from vindi.errors import ApiError, ParamError
from vindi.handlers.base_handler import BaseVindiHandler


@dataclass
class ChargeBillParams:
    # TODO: Check if any of thise are required or not
    payment_method_code: str | None = None
    installments: float | None = None

    @property
    def asdict(self) -> dict:
        repr = {
            "payment_method_code": self.payment_method_code,
            "installments": self.installments,
        }
        return {k: v for k, v in repr.items() if v is not None}


@dataclass
class BillItem:
    product_id: str
    product_code: str | None = None
    amount: int | None = None
    description: str | None = None

    @property
    def asdict(self) -> dict:
        repr: dict[str, Any] = {
            "product_id": self.product_id,
            "amount": self.amount,
            "description": self.description,
            "product_code": self.product_code,
        }
        return {k: v for k, v in repr.items() if v is not None}


@dataclass
class Bill:
    customer_id: str
    code: str
    payment_method_code: str
    bill_items: list[BillItem]
    installments: int = 1
    billing_at: str | None = None
    due_at: str | None = None
    payment_profile_id: str | None = None
    gateway_token: str | None = None
    metadata: dict | None = None

    @property
    def asdict(self) -> dict[str, Any]:
        repr = {
            "customer_id": str(self.customer_id),
            "code": self.code,
            "payment_method_code": self.payment_method_code,
            "installments": self.installments,
            "billing_at": self.billing_at,
            "due_at": self.due_at,
            "metadata": {k: v for k, v in self.metadata.items()}
            if self.metadata
            else None,
            "payment_profile": None,
            "bill_items": [p.asdict for p in self.bill_items],
        }
        if bool(self.payment_profile_id) + bool(self.gateway_token) > 1:
            err = "give either payment_profile_id or credit_card_token, not both."
            raise ParamError(err)
        if self.payment_profile_id:
            repr["payment_profile"] = {"id": self.payment_profile_id}
        if self.gateway_token:
            repr["payment_profile"] = {"gateway_token": self.gateway_token}
        return {k: v for k, v in repr.items() if v is not None}


class BillHandler(BaseVindiHandler):
    @property
    def base_endpoint(self) -> str:
        return "/v1/bills/"

    async def create_bill(self, bill: Bill):
        output = await self.request(
            method="post",
            url=self._config.get_environ_url() + self.base_endpoint,
            json=bill.asdict,
        )
        if "errors" in output.json:
            raise ApiError(output.json.get("errors", "unknown error"))
        return output

    async def cancel_bill(self, id: str):
        output = await self.request(
            method="delete",
            url=self._config.get_environ_url() + self.base_endpoint + str(id),
        )
        if "errors" in output.json:
            raise ApiError(output.json.get("errors", "unknown error"))
        return output

    async def update_bill(self, bill: Bill, id):
        output = await self.request(
            method="put",
            url=self._config.get_environ_url() + self.base_endpoint + str(id),
            json=bill.asdict,
        )
        if "errors" in output.json:
            raise ApiError(output.json.get("errors", "unknown error"))
        return output

    async def get_bill(self, id: str):
        output = await self.request(
            method="get",
            url=self._config.get_environ_url() + self.base_endpoint + str(id),
        )
        if "errors" in output.json:
            raise ApiError(output.json.get("errors", "unknown error"))
        return output

    async def approve_bill_in_review(self, id: str):
        # TODO: Check with Vindi how can i simulate this review stats so we can test this
        endpoint = "/approve"
        output = await self.request(
            method="post",
            url=self._config.get_environ_url()
            + self.base_endpoint
            + str(id)
            + endpoint,
        )
        if "errors" in output.json:
            raise ApiError(output.json.get("errors", "unknown error"))
        return output

    async def charge_bill_scheduled(self, id: str, params: ChargeBillParams = {}):
        endpoint = "charge"
        output = await self.request(
            method="post",
            url=self._config.get_environ_url()
            + self.base_endpoint
            + str(id)
            + endpoint,
            json=params,
        )
        if "errors" in output.json:
            raise ApiError(output.json.get("errors", "unknown error"))
        return output

    async def invoice_bill(self, id: str):
        endpoint = "invoice"
        output = await self.request(
            method="post",
            url=self._config.get_environ_url()
            + self.base_endpoint
            + str(id)
            + endpoint,
        )
        if "errors" in output.json:
            raise ApiError(output.json.get("errors", "unknown error"))
        return output
