"""Interfaces for the external services used to build a reading.

Every service sits behind a Protocol so that it can be replaced by an offline
implementation in tests and demos. Real credentials are never needed to run the
test suite.
"""

from __future__ import annotations

from typing import Protocol

from .models import BirthData, Place, ReadingType


class Geocoder(Protocol):
    def resolve(self, city: str, country_code: str) -> Place:
        """Return the most likely place for a city name and country code."""


class ChartProvider(Protocol):
    def birth_chart(self, birth: BirthData, birth_place: Place) -> str:
        """Return the natal chart as text suitable for an LLM prompt."""

    def solar_return(
        self, birth: BirthData, birth_place: Place, year: int, return_place: Place
    ) -> str:
        """Return the solar return chart as text suitable for an LLM prompt."""


class KnowledgeBase(Protocol):
    def search(self, query: str, limit: int = 5) -> list[str]:
        """Return passages relevant to a query, best first."""


class ReadingWriter(Protocol):
    def write(
        self,
        *,
        theme: str,
        reading_type: ReadingType,
        chart_context: str,
        references: list[str],
    ) -> str:
        """Write the reading as prose."""
