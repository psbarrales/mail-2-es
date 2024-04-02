from domain.entities.Register import Register
from domain.repositories.ISearchRepository import ISearchRepository
from dotenv import load_dotenv
from elasticsearch import Elasticsearch
from typing import List
from utils.with_retry import with_retry
import os

load_dotenv()

ELASTICSEARCH_URL = os.getenv("ELASTICSEARCH_HOST")
ELASTICSEARCH_USER = os.getenv("ELASTICSEARCH_USERNAME")
ELASTICSEARCH_PWD = os.getenv("ELASTICSEARCH_PASSWORD")
ELASTICSEARCH_INDEX = os.getenv("ELASTICSEARCH_INDEX")


class ElasticSearchRepository(ISearchRepository):
    es: Elasticsearch = None

    def _connect(self) -> None:
        if self.es is None:
            self.es = Elasticsearch(
                [ELASTICSEARCH_URL],
                basic_auth=(ELASTICSEARCH_USER, ELASTICSEARCH_PWD),
                verify_certs=False,  # This disables SSL certificate verification
            )

    @with_retry(retries=5, backoff=10)
    def store_register(self, registers: List[Register]):
        self._connect()
        # Ensure connection to Elasticsearch
        if not self.es.ping():
            raise ConnectionError("Elasticsearch connection failed")

        # Prepare documents for bulk indexing
        actions = []
        for register in registers:
            action = {
                "index": {
                    "_index": ELASTICSEARCH_INDEX,
                }
            }
            actions.append(action)
            actions.append(
                register.json(
                    exclude={
                        "account": {"similarity", "billDate", "billDay", "primary"},
                        "destinationAccount": {
                            "similarity",
                            "billDate",
                            "billDay",
                            "primary",
                        },
                    }
                )
            )

        # Perform bulk indexing
        response = self.es.bulk(body=actions, refresh=True)

        # Check for errors in response
        if response["errors"]:
            for item in response["items"]:
                if "index" in item and item["index"]["error"]:
                    print("Failed to index document:", item["index"]["error"])
        else:
            print("Bulk operation completed successfully.")
