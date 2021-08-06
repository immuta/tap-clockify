"""REST client handling, including ClockifyStream base class."""

import requests
from pathlib import Path
from typing import Any, Dict, Optional, Union, List, Iterable

from singer_sdk.helpers.jsonpath import extract_jsonpath
from singer_sdk.streams import RESTStream


SCHEMAS_DIR = Path(__file__).parent / Path("./schemas")


class ClockifyStream(RESTStream):
    """Clockify stream class."""

    records_jsonpath = "$[*]"
    next_page_token_jsonpath = "$.next_page"

    @property
    def url_base(self):
        return f'https://api.clockify.me/api/v1/workspaces/{self.config["workspace"]}'

    @property
    def http_headers(self) -> dict:
        """Return the http headers needed."""
        headers = {
            "Content-Type": "application/json",
            "x-api-key": self.config["api_key"]
        }
        if "user_agent" in self.config:
            headers["User-Agent"] = self.config.get("user_agent")
        return headers
