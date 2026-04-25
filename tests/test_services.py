import pytest
from src.services.mock_broker import MockDataBroker
from src.services.base import BrokerResult


def test_mock_broker_returns_results():
    broker = MockDataBroker()
    results = broker.search(first_name="John", last_name="Doe")

    assert isinstance(results, list)
    assert len(results) == 5
    assert all(isinstance(r, BrokerResult) for r in results)


def test_mock_broker_result_structure():
    broker = MockDataBroker()
    results = broker.search(email="john@example.com")

    for result in results:
        assert result.source_name is not None
        assert result.source_url is not None
        assert isinstance(result.data_found, bool)
        if result.data_found:
            assert result.data_details is not None


def test_mock_broker_result_count():
    broker = MockDataBroker()
    results = broker.search(
        first_name="Jane",
        last_name="Smith",
        phone="5551234567",
        address="123 Main St",
        city="Boston",
        state="MA",
        zip_code="02101"
    )

    assert len(results) == 5
    found_count = sum(1 for r in results if r.data_found)
    assert 0 <= found_count <= 5