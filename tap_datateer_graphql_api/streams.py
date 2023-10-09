"""Stream type classes for tap-datateer-graphql-api."""

from __future__ import annotations

import typing as t
from pathlib import Path
from urllib.parse import urlencode
import requests  # noqa: TCH002
from typing import Iterable

from singer_sdk import typing as th  # JSON Schema typing helpers

from tap_datateer_graphql_api.client import DatateerGraphqlApiStream


class OrganizationsStream(DatateerGraphqlApiStream):
    """Organizations with Balances"""

    name = "organizations"
    schema = th.PropertiesList(th.Property("id", th.StringType)).to_dict()
    replication_key = None
    query = """
    query {
        organizations {
        id
        }
    }
    """

    def parse_response(self, response: requests.Response) -> Iterable[dict]:
        """Parse the response and return an iterator of result records.

        Args:
            response: The HTTP ``requests.Response`` object.

        Yields:
            Each record from the source.
        """
        res = response.json()["data"]["organizations"]
        yield from res

    def get_child_context(self, record: dict, context: Optional[dict]) -> dict:
        """Return a context dictionary for the child streams.
        Refer to https://sdk.meltano.com/en/latest/parent_streams.html"""
        return {"organization_id": record["id"]}


class BalancesStream(DatateerGraphqlApiStream):
    """Balances are calculated from individual charges"""

    name = "balances"
    schema = th.PropertiesList(
        th.Property("organizationId", th.StringType),
        th.Property("startDate", th.DateTimeType),
        th.Property("endDate", th.DateTimeType),
        th.Property("accrualHours", th.NumberType),
        th.Property("availableHours", th.NumberType),
        th.Property("chargedHours", th.NumberType),
        th.Property("excessHours", th.NumberType),
        th.Property("expiredHours", th.NumberType),
        th.Property("priorPeriodRolloverHours", th.NumberType),
        th.Property("projectedCharges", th.NumberType),
        th.Property("rolloverHours", th.NumberType),
    ).to_dict()
    replication_key = None
    query = """
    query($organizationId: ID!, $startDate: Date!) {
        dataCrew {
            balances(input: {organizationId: $organizationId, startDate: $startDate}) {
            startDate
            endDate
            accrualHours
            availableHours
            chargedHours
            excessHours
            expiredHours
            priorPeriodRolloverHours
            projectedCharges
            rolloverHours
            }
        }
    }
    """

    def get_url_params(self, context, next_page_token):
        params = {
            "startDate": self.config.get("start_date"),
            "organizationId": context["organization_id"],
        }
        return params

    def parse_response(self, response: requests.Response) -> Iterable[dict]:
        """Parse the response and return an iterator of result records.

        Args:
            response: The HTTP ``requests.Response`` object.

        Yields:
            Each record from the source.
        """
        res = response.json()["data"]["dataCrew"]["balances"]
        yield from res

    def post_process(self, row: dict, context: dict) -> dict:
        """Adds the organization id to each record"""
        row["organizationId"] = context["organization_id"]
        return row

    parent_stream_type = OrganizationsStream
    ignore_parent_replication_key = True
