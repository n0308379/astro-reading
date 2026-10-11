"""Chart calculation through the Astrologer API (hosted on RapidAPI)."""

from __future__ import annotations

from typing import Any

import httpx

from .errors import ChartProviderError
from .models import BirthData, Place


class AstrologerApiProvider:
    """Fetch natal and solar return charts as AI-ready context text.

    The request shapes follow the public Astrologer API. Confirm them against
    the current API documentation before relying on them.
    """

    BASE_URL = "https://astrologer.p.rapidapi.com"
    HOST = "astrologer.p.rapidapi.com"
    BIRTH_CHART_PATH = "/api/v5/context/birth-chart"
    SOLAR_RETURN_PATH = "/api/v5/context/solar-return"

    def __init__(
        self,
        rapidapi_key: str,
        geonames_username: str,
        client: httpx.Client | None = None,
    ) -> None:
        self._rapidapi_key = rapidapi_key
        self._geonames_username = geonames_username
        self._client = client or httpx.Client(timeout=60.0)

    def birth_chart(self, birth: BirthData, birth_place: Place) -> str:
        payload = {"subject": self._subject(birth)}
        return self._post(self.BIRTH_CHART_PATH, payload)

    def solar_return(
        self, birth: BirthData, birth_place: Place, year: int, return_place: Place
    ) -> str:
        if not return_place.timezone:
            raise ChartProviderError("The solar return place has no time zone.")
        payload = {
            "subject": self._subject(birth),
            "year": year,
            "return_location": {
                "latitude": return_place.latitude,
                "longitude": return_place.longitude,
                "timezone": return_place.timezone,
            },
        }
        return self._post(self.SOLAR_RETURN_PATH, payload)

    def _subject(self, birth: BirthData) -> dict[str, Any]:
        # The name is optional for the user, so a neutral label is sent by default.
        return {
            "name": birth.name or "Subject",
            "year": birth.birth_date.year,
            "month": birth.birth_date.month,
            "day": birth.birth_date.day,
            "hour": birth.birth_time.hour,
            "minute": birth.birth_time.minute,
            "city": birth.city,
            "nation": birth.country_code,
            "geonames_username": self._geonames_username,
        }

    def _post(self, path: str, payload: dict[str, Any]) -> str:
        headers = {
            "X-RapidAPI-Host": self.HOST,
            "X-RapidAPI-Key": self._rapidapi_key,
            "Content-Type": "application/json",
        }
        try:
            response = self._client.post(f"{self.BASE_URL}{path}", headers=headers, json=payload)
            response.raise_for_status()
            data = response.json()
        except (httpx.HTTPError, ValueError) as exc:
            raise ChartProviderError("The chart service request failed.") from exc
        if data.get("status") != "OK" or not data.get("context"):
            raise ChartProviderError("The chart service did not return valid chart data.")
        return str(data["context"])
