from dataclasses import dataclass, field
from typing import Any
from uuid import uuid1
from vindi.errors import ApiError
from vindi.handlers.base_handler import BaseVindiHandler


@dataclass
class Product:
    name: str
    description: str = "active"
    price: int | float = 0
    status: str = "active"
    invoice: str = "always"
    unit: str = "UN"
    code: str = str(uuid1())
    pricing_schema: dict[str, Any] = field(default_factory=dict)

    def asdict(self) -> dict[str, Any]:
        return {
            "name": self.name,
            "code": self.code,
            "unit": self.unit,
            "status": self.status,
            "description": self.description,
            "invoice": self.invoice,
            "pricing_schema": {
                "price": self.price,
                "schema_type": "per_unit",
            },
            "metadata": {},
        }


class ProductHandler(BaseVindiHandler):
    @property
    def base_endpoint(self) -> str:
        return "/v1/products/"

    async def create_product(self, product: Product) -> Any:
        output = await self.request(
            method="post",
            url=self._config.get_environ_url() + self.base_endpoint,
            json=product.asdict(),
        )
        if "errors" in output.json:
            raise ApiError(output.json.get("errors", "unknow error"))
        return output

    async def update_product(self, product: Product, id) -> Any:
        product_as_dict = product.asdict()
        output = await self.request(
            method="put",
            url=self._config.get_environ_url() + self.base_endpoint + id,
            json=product_as_dict,
        )
        if "errors" in output.json:
            raise ApiError(output.json.get("errors", "unknow error"))
        return output
