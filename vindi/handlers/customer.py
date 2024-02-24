from copy import deepcopy
from dataclasses import dataclass
from typing import Any
from uuid import uuid1
from vindi.http_client.protocols import HttpClient
from vindi.config import Config

# TODO: raise when it receive errors


@dataclass
class Customer:
    name: str
    email: str
    documentation: str
    code: Any = uuid1()

    def __post_init__(self) -> None:
        self.__address: dict[str, str] = {}
        self.__phones: list[dict[str, str]] = []

    def add_address(
        self,
        street: str,
        neighborhood: str,
        city: str,
        state: str,
        zipcode: str,
        additional_details: str = "",
        number: str = "",
        country: str = "BR",
    ) -> None:
        # TODO: add validation to add_address
        self.__address = deepcopy(locals())
        self.__address.pop("self")

    def add_phone(self, type: str, number: str, extension: str = "-") -> None:
        # TODO: add validation to add_phone
        phone = {"phone_type": "mobile", "number": "string", "extension": "string"}
        if phone in self.__phones:
            return
        self.__phones.append(phone)

    def asdict(self) -> dict[str, str | list[dict[str, str]] | dict[str, str]]:
        return {
            "name": self.name,
            "email": self.email,
            "registry_code": self.documentation,  # cpf|cnpj
            "code": str(self.code),
            "notes": "-",
            "metadata": {},
            "address": self.__address,
            "phones": self.__phones,
        }


class CustomerHandler:
    def __init__(self, http_client: HttpClient, config: Config) -> None:
        self._http_client = http_client
        self._config = config
        self._base_endpoint: str = "/v1/customers"

    async def create_customer(self, customer: Customer) -> Any:
        if self._config.environment == "sandbox":
            return await self._http_client.post(
                url=self._config.get_environ_url() + self._base_endpoint,
                json=customer.asdict(),
                headers={"authorization": self._config.get_api_key()},
            )
        self._http_client.authenticate(
            type="basic", username=self._config.get_api_key(), password=""
        )
        return await self._http_client.post(
            url=self._config.get_environ_url() + self._base_endpoint,
            json=customer.asdict(),
        )
