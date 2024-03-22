from dataclasses import asdict, dataclass, field
from typing import Any, Literal
from uuid import uuid1
from vindi.errors import ApiError
from vindi.handlers.base_handler import BaseVindiHandler


@dataclass
class PlanItem:
    cycles: int
    product_id: str


@dataclass
class Plan:
    name: str
    description: str
    installments: Literal[1, 2, 3, 4, 5, 6, 7, 8, 9, 10, 11, 12]
    code: str = str(uuid1())
    status: str = "active"
    interval: Literal["months", "days"] = "months"
    invoice_split: bool = False
    billing_cycles: int | None = None
    plan_items: list[PlanItem] = field(default_factory=list)
    interval_count: int = 1

    def asdict(self) -> dict[str, Any]:
        output = {
            "name": self.name,
            "interval": self.interval,
            "interval_count": self.interval_count,
            "billing_trigger_type": "beginning_of_period",
            "billing_trigger_day": 0,
            "billing_cycles": self.billing_cycles,
            "code": self.code,
            "description": self.description,
            "installments": self.installments,
            "invoice_split": self.invoice_split,
            "status": self.status,
            "metadata": {},
        }
        if self.plan_items:
            output["plan_items"] = [asdict(item) for item in self.plan_items]
        return output


class PlanHandler(BaseVindiHandler):
    @property
    def base_endpoint(self) -> str:
        return "/v1/plans/"

    async def create_plan(self, plan: Plan) -> Any:
        output = await self.request(
            method="post",
            url=self._config.get_environ_url() + self.base_endpoint,
            json=plan.asdict(),
        )
        if "errors" in output.json:
            raise ApiError(output.json.get("errors", "unknow error"))
        return output
