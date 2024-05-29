from dataclasses import dataclass, field
from typing import Any
from .http_status import HttpStatus


class HttpAuth:
    type: str
    data: dict[str, str]

    def __post_init__(self) -> None:
        self.type = self.type.lower()


@dataclass
class HttpResponse:
    status: HttpStatus = HttpStatus.OK
    headers: dict[Any, Any] = field(default_factory=dict)
    json: dict[Any, Any] = field(default_factory=dict)
