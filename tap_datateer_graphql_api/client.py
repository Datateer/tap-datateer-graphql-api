"""GraphQL client handling, including DatateerGraphqlApiStream base class."""

from __future__ import annotations

from typing import Iterable
from urllib.parse import urlencode

import requests  # noqa: TCH002
from singer_sdk.streams import GraphQLStream
from singer_sdk.authenticators import APIKeyAuthenticator


class DatateerGraphqlApiStream(GraphQLStream):
    """DatateerGraphqlApi stream class."""

    @property
    def url_base(self) -> str:
        """Return the API URL root, configurable via tap settings."""
        url = self.config.get('api_url') or "https://api.datateer.com/graphql"
        return url

    @property
    def http_headers(self) -> dict:
        """Return the http headers needed.

        Returns:
            A dictionary of HTTP headers.
        """
        headers = {}
        if "user_agent" in self.config:
            headers["User-Agent"] = self.config.get("user_agent")
        return headers
    
    @property
    def authenticator(self):
        return APIKeyAuthenticator(
            stream=self,
            key="x-api-key",
            value=self.config.get('auth_token'),
            location="header"
        )

    def parse_response(self, response: requests.Response) -> Iterable[dict]:
        """Parse the response and return an iterator of result records.

        Args:
            response: The HTTP ``requests.Response`` object.

        Yields:
            Each record from the source.
        """
        raise Exception('Needs to be implemented for each query')

