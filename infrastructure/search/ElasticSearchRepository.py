from domain.commands.SearchCommand import SearchCommand
from domain.entities.Register import Register
from .ElastisSearchRegisterMapping import RegisterMapping
from domain.repositories.ISearchRepository import ISearchRepository
from dotenv import load_dotenv
from elasticsearch import Elasticsearch
from typing import List
from utils.with_retry import with_retry
import os
import base64

load_dotenv()

ELASTICSEARCH_URL = os.getenv("ELASTICSEARCH_HOST")
ELASTICSEARCH_USER = os.getenv("ELASTICSEARCH_USERNAME")
ELASTICSEARCH_PWD = os.getenv("ELASTICSEARCH_PASSWORD")
ELASTICSEARCH_INDEX = os.getenv("ELASTICSEARCH_INDEX")


class ElasticSearchRepository(ISearchRepository):
    es: Elasticsearch = None
    engine = "ElasticSearch"
    index = "registers"
    schema = RegisterMapping

    def _connect(self) -> None:
        if self.es is None:
            self.es = Elasticsearch(
                [ELASTICSEARCH_URL],
                basic_auth=(ELASTICSEARCH_USER, ELASTICSEARCH_PWD),
                verify_certs=False,  # This disables SSL certificate verification
            )

    @with_retry(retries=3, backoff=20)
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

    @with_retry(retries=3, backoff=20)
    def search_command(self, command: SearchCommand):
        self._connect()
        headers = (
            {"Content-Type": "application/json"} if command.body is not None else {}
        )
        headers["Authorization"] = (
            f"Basic {base64.b64encode(f'{ELASTICSEARCH_USER}:{ELASTICSEARCH_PWD}'.encode('utf-8')).decode('utf-8')}"
        )

        try:
            print("ElasticSearch Command", command)
            response = self.es.transport.perform_request(
                command.method.upper(),
                command.path
                if command.path.count(self.index) > 0
                else f"/{self.index}{command.path}",
                headers=headers,
                body=command.body,
                max_retries=3,
                request_timeout=30000,
            )
            print("ElasticSearch Response", response.body)
            return response.body
        except Exception as e:
            raise e
