"""Stream type classes for tap-datateer-graphql-api."""

from __future__ import annotations

import typing as t
from pathlib import Path
from urllib.parse import urlencode
import requests  # noqa: TCH002
from typing import Iterable

from singer_sdk import typing as th  # JSON Schema typing helpers

from tap_datateer_graphql_api.client import DatateerGraphqlApiStream

class BalancesStream(DatateerGraphqlApiStream):
    """ Balances are calculated from individual charges"""

    name = "balances"
    schema = th.PropertiesList(
        th.Property("startDate", th.DateTimeType),
        th.Property("endDate", th.DateTimeType),
        th.Property("accrualHours", th.NumberType),
        th.Property("availableHours", th.NumberType),
        th.Property("chargedHours", th.NumberType),
        th.Property("excessHours", th.NumberType),
        th.Property("expiredHours", th.NumberType),
        th.Property("priorPeriodRolloverHours", th.NumberType),
        th.Property("projectedCharges", th.NumberType),
        th.Property("rolloverHours", th.NumberType)
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
            'organizationId': self.config.get("organization_id"),
            'startDate': self.config.get("start_date")
        }
        return params

    def parse_response(self, response: requests.Respeonse) -> Iterable[dict]:
        """Parse the response and return an iterator of result records.

        Args:
            response: The HTTP ``requests.Response`` object.

        Yields:
            Each record from the source.
        """
        res = response.json()['data']['dataCrew']['balances']
        yield from res


