from dataclasses import dataclass
from typing import Any
from uuid import uuid1
from vindi.errors import ApiError
from vindi.handlers.base_handler import BaseVindiHandler


@dataclass
class Plan:
    name: str
    description: str = "active"
    status: str = "active"
    code: str = str(uuid1())

    def asdict(self) -> dict[str, Any]:
        return {
            "name": self.name,
            "interval": "days",
            "interval_count": 30,
            "billing_trigger_type": "beginning_of_period",
            "billing_trigger_day": 0,
            "billing_cycles": 0,
            "code": self.code,
            "description": self.description,
            "installments": 12,
            "invoice_split": False,
            "status": self.status,
            # "plan_items": [{"cycles": 0, "product_id": 0}],
            "metadata": {},
        }


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
