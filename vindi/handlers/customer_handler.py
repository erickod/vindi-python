from typing import Any, Literal
from vindi.address import Address
from vindi.customer import Customer
from vindi.errors import ApiError
from vindi.handlers.base_handler import BaseVindiHandler


class CustomerHandler(BaseVindiHandler):
    @property
    def base_endpoint(self) -> str:
        return "/v1/customers/"

    async def create_customer(self, customer: Customer) -> Any:
        output = await self.request(
            method="post",
            url=self._config.get_environ_url() + self.base_endpoint,
            json=customer.asdict(),
        )
        if "errors" in output.json:
            raise ApiError(output.json.get("errors", "unknow error"))
        return output

    async def update_customer(self, customer: Customer, id: int) -> Any:
        url = f"{self._config.get_environ_url()}{self.base_endpoint}{id}"
        customer_asdict = customer.asdict()
        del customer_asdict["email"]
        output = await self.request(
            method="put",
            url=url,
            json=customer_asdict,
        )
        if "errors" in output.json:
            raise ApiError(output.json.get("errors", "unknow error"))
        return output

    async def delete_customer(self, id: int) -> Any:
        url = f"{self._config.get_environ_url()}{self.base_endpoint}{id}"
        output = await self.request(method="delete", url=url, json=None)
        if "errors" in output.json:
            output.json = {"id": id}
            return output
        return output

    async def list_customers(
        self,
        page: int = 1,
        items_per_page: int = 25,
        sort_by: str = "created_at",
        order: Literal["asc", "desc"] = "asc",
        query: str = "",
    ) -> Any:
        # TODO: raise when it receive errors
        url = (
            f"{self._config.get_environ_url()}"
            f"{self.base_endpoint}?page={page}"
            f"&per_page={items_per_page}&sort={sort_by}"
            f"sort_order={order}&query={query}"
        )
        output = await self.request(method="get", url=url)
        if "errors" in output.json:
            raise ApiError(output.json.get("errors", "unknow error"))
        raw_customers = output.json.get("customers", [])
        customers: list[Customer] = []
        for c in raw_customers:
            address = c.get("address", {})
            customer = Customer(
                name=c.get("name"),
                email=c.get("email"),
                documentation=c.get("registry_code"),
                code=c.get("code"),
                address=Address(
                    street=address.get("street"),
                    neighborhood=address.get("neighborhood"),
                    city=address.get("city"),
                    zipcode=address.get("zipcode"),
                    complement=address.get("additional_details"),
                    number=address.get("number"),
                    country=address.get("country"),
                ),
            )
            customers.append(customer)
        return customers

    async def create_payment_profile(self, gateway_token: str, customer_id: str, payment_method_code: str) -> Any:
        base_endpoint = '/v1/payment_profiles'
        output = await self.request(
            method="post",
            url=self._config.get_environ_url() + base_endpoint,
            json={
                "gateway_token": gateway_token,
                "customer_id": customer_id,
                "payment_method_code": payment_method_code
            }
        )
        if "errors" in output.json:
            raise ApiError(output.json.get("errors", "unknown error"))
        return output
