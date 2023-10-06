"""DatateerGraphqlApi tap class."""

from __future__ import annotations

from singer_sdk import Tap
from singer_sdk import typing as th  # JSON schema typing helpers

# TODO: Import your custom stream types here:
from tap_datateer_graphql_api import streams


class TapDatateerGraphqlApi(Tap):
    """DatateerGraphqlApi tap class."""

    name = "tap-datateer-graphql-api"

    config_jsonschema = th.PropertiesList(
        th.Property(
            "auth_token",
            th.StringType,
            required=True,
            secret=True,  # Flag config as protected.
            description="The token to authenticate against the API service",
        ),
        th.Property(
            "api_url",
            th.StringType,
            required=False,
            description="The URL of the API e.g. https://api.datateer.com/graphql or http://localhost:3000/graphql. Defaults to https://api.datateer.com/api",
            default="https://api.datateer.com/graphql",
        ),
        th.Property(
            "start_date",
            th.DateTimeType,
            description="The earliest record date to sync",
            default="2023-01-01",
        ),
    ).to_dict()

    def discover_streams(self) -> list[streams.DatateerGraphqlApiStream]:
        """Return a list of discovered streams.

        Returns:
            A list of discovered streams.
        """
        return [streams.BalancesStream(self), streams.OrganizationsStream(self)]


if __name__ == "__main__":
    TapDatateerGraphqlApi.cli()
