import requests
import singer

LOGGER = singer.get_logger()  # noqa


class ClockifyClient:

    MAX_TRIES = 5

    def __init__(self, config):
        self.config = config

    def make_request(self, url, method, params=None, body=None):
        LOGGER.info("Making %s request to %s (%s)", method, url, params)

        response = requests.request(
            method,
            url,
            headers={
                "x-api-key": self.config["api_key"],
                "Content-Type": "application/json",
            },
            params=params,
            json=body,
        )

        if response.status_code != 200:
            raise RuntimeError(response.text)

        return response.json()
