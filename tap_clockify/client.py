"""REST client handling, including ClockifyStream base class."""

import requests
from pathlib import Path
from typing import Any, Dict, Optional, Union, List, Iterable

from singer_sdk.authenticators import APIKeyAuthenticator
from singer_sdk.helpers.jsonpath import extract_jsonpath
from singer_sdk.streams import RESTStream


SCHEMAS_DIR = Path(__file__).parent / Path("./schemas")


class ClockifyStream(RESTStream):
    """Clockify stream class."""

    records_jsonpath = "$[*]"
    _page_size = 100

    @property
    def url_base(self):
        return f'https://api.clockify.me/api/v1/workspaces/{self.config["workspace"]}'

    @property
    def authenticator(self) -> APIKeyAuthenticator:
        return APIKeyAuthenticator.create_for_stream(
            self, key="x-api-key", value=self.config["api_key"], location="header"
        )

    def get_next_page_token(
        self, response: requests.Response, previous_token: Optional[Any]
    ) -> Optional[Any]:
        """Return a token for identifying next page or None if no more pages."""
        current_page = previous_token or 1
        count_records = len(response.json())
        if count_records == self._page_size:
            next_page_token = current_page + 1
            self.logger.debug(f"Next page token retrieved: {next_page_token}")
            return next_page_token
        return None

    def get_url_params(
        self, context: Optional[dict], next_page_token: Optional[Any]
    ) -> Dict[str, Any]:
        """Return a dictionary of values to be used in URL parameterization."""
        params = {
            "page-size": self._page_size,
            "page": 1,
        }
        if next_page_token:
            params["page"] = next_page_token
        if self.replication_key:
            start_time = self.get_starting_timestamp(context)
            start_time_fmt = start_time.strftime("%Y-%m-%dT%H:%M:%SZ") if start_time else None
            params["start"] = start_time_fmt
        return params
