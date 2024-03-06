from dataclasses import dataclass


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
