import random
from src.services.base import DataBroker, BrokerResult


class MockDataBroker(DataBroker):
    MOCK_SOURCES = [
        {
            "name": "PublicRecordsFinder",
            "url": "https://publicrecords.example.com",
            "found_rate": 0.6,
            "details": "Found in public property records",
        },
        {
            "name": "PeopleSearchPlus",
            "url": "https://peoplesearch.example.com",
            "found_rate": 0.7,
            "details": "Listed in people search directory",
        },
        {
            "name": "DataBrokerNet",
            "url": "https://databrokernet.example.com",
            "found_rate": 0.8,
            "details": "Your data is available for purchase",
        },
        {
            "name": "SocialLookup",
            "url": "https://sociallookup.example.com",
            "found_rate": 0.4,
            "details": "Found on social media profiles",
        },
        {
            "name": " VoterRecords",
            "url": "https://voterrecords.example.com",
            "found_rate": 0.5,
            "details": "Found in voter registration database",
        },
    ]

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
        results = []
        for source in self.MOCK_SOURCES:
            data_found = random.random() < source["found_rate"]
            results.append(
                BrokerResult(
                    source_name=source["name"],
                    source_url=source["url"],
                    data_found=data_found,
                    data_details=source["details"] if data_found else None,
                )
            )
        return results