from src.services.base import DataBroker, BrokerResult
from src.services.mock_broker import MockDataBroker


def get_broker() -> DataBroker:
    return MockDataBroker()