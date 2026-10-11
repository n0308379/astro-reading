"""Offline implementations for tests and demos. No network, no credentials."""

from __future__ import annotations

from .errors import PlaceNotFoundError
from .models import BirthData, Place

_KNOWN_PLACES = {
    ("lisboa", "PT"): Place("Lisboa", "PT", 38.7167, -9.1333, "Europe/Lisbon", "Lisboa"),
    ("lisbon", "PT"): Place("Lisboa", "PT", 38.7167, -9.1333, "Europe/Lisbon", "Lisboa"),
    ("porto", "PT"): Place("Porto", "PT", 41.1496, -8.6110, "Europe/Lisbon", "Porto"),
    ("sao paulo", "BR"): Place("São Paulo", "BR", -23.5475, -46.6361, "America/Sao_Paulo", "SP"),
}


class OfflineGeocoder:
    """Resolve a handful of well-known cities from a built-in table."""

    def resolve(self, city: str, country_code: str) -> Place:
        place = _KNOWN_PLACES.get((city.strip().lower(), country_code.upper()))
        if place is None:
            raise PlaceNotFoundError("No place found in the offline table.")
        return place


class OfflineChartProvider:
    """Return fixed, fictitious chart context. The values are not real."""

    def birth_chart(self, birth: BirthData, birth_place: Place) -> str:
        return (
            "<chart type='natal' fictitious='true'>"
            "<planet name='Sun' sign='Libra' house='10'/>"
            "<planet name='Moon' sign='Cancer' house='7'/>"
            "<aspect between='Sun,Moon' type='trine'/>"
            "</chart>"
        )

    def solar_return(
        self, birth: BirthData, birth_place: Place, year: int, return_place: Place
    ) -> str:
        return (
            f"<chart type='solar_return' year='{year}' fictitious='true'>"
            "<planet name='Sun' sign='Libra' house='4'/>"
            "<planet name='Moon' sign='Aries' house='10'/>"
            "</chart>"
        )
