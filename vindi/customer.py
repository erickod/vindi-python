from dataclasses import dataclass
from typing import Any, Literal
from uuid import uuid1
from vindi.address import Address


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
