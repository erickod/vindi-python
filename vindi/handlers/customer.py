from dataclasses import dataclass
from typing import Any, Literal
from uuid import uuid1
from vindi.errors import ApiError
from vindi.handlers.base_handler import BaseVindiHandler


@dataclass
class Address:
    street: str
    neighborhood: str
    city: str
    zipcode: str
    complement: str
    number: str
    country: str

    def asdict(self) -> dict[str, str]:
        return {
            "street": self.street,
            "neighborhood": self.neighborhood,
            "city": self.city,
            "zipcode": self.zipcode,
            "complement": self.complement,
            "number": self.number,
            "country": self.country,
        }


@dataclass
class Customer:
    name: str
    email: str
    documentation: str
    address: Address
    code: Any = uuid1()

    def __post_init__(self) -> None:
        self.__phones: list[dict[str, str]] = []
        self.__status: Literal["active", "inactive"]

    def add_phone(self, type: str, number: str, extension: str = "-") -> None:
        # TODO: add validation to add_phone
        phone = {"phone_type": type, "number": number, "extension": extension}
        if phone in self.__phones:
            return
        self.__phones.append(phone)

    def set_status(self, status: Literal["active", "inactive"]) -> None:
        self.__status = status

    def asdict(self) -> dict[str, str | list[dict[str, str]] | dict[str, str]]:
        return {
            "name": self.name,
            "email": self.email,
            "registry_code": self.documentation,  # cpf|cnpj
            "code": str(self.code),
            "notes": "-",
            "metadata": {},
            "address": self.address.asdict(),
            "phones": self.__phones,
        }


class CustomerHandler(BaseVindiHandler):
    @property
    def base_endpoint(self) -> str:
        return "/v1/customers"

    async def create_customer(self, customer: Customer) -> None:
        output = await self.request(
            method="post",
            url=self._config.get_environ_url() + self.base_endpoint,
            json=customer.asdict(),
        )
        if "errors" in output.json:
            raise ApiError(output.json.get("errors", "unknow error"))

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
        customers: list[Customer] = []
        output = await self.request(method="get", url=url)
        if "errors" in output.json:
            raise ApiError(output.json.get("errors", "unknow error"))
        raw_customers = output.json.get("customers", [])
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
