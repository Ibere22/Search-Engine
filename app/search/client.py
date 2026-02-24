import os
import meilisearch
from dotenv import load_dotenv


def get_client() -> meilisearch.Client:
    load_dotenv()
    key = os.getenv('MEILI_MASTER_KEY')
    url = os.getenv('MEILI_HTTP_ADDR')
    client = meilisearch.Client(url=url, api_key=key)
    return client