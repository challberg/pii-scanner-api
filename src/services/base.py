from abc import ABC, abstractmethod
from dataclasses import dataclass


@dataclass
class BrokerResult:
    source_name: str
    source_url: str | None
    data_found: bool
    data_details: str | None


class DataBroker(ABC):
    @abstractmethod
    def search(
        self,
        first_name: str | None = None,
        last_name: str | None = None,
        email: str | None = None,
        phone: str | None = None,
        address: str | None = None,
        city: str | None = None,
        state: str | None = None,
        zip_code: str | None = None,
    ) -> list[BrokerResult]:
        pass