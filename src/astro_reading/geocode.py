"""Place lookup through the GeoNames web services."""

from __future__ import annotations

from typing import Any

import httpx

from .errors import GeocodingError, PlaceNotFoundError
from .models import Place


class GeoNamesGeocoder:
    """Resolve a city and country to coordinates and a time zone using GeoNames.

    The base URL is configurable. Check the GeoNames documentation for the
    endpoint that matches your account type.
    """

    def __init__(
        self,
        username: str,
        client: httpx.Client | None = None,
        base_url: str = "https://api.geonames.org",
    ) -> None:
        self._username = username
        self._client = client or httpx.Client(timeout=15.0)
        self._base_url = base_url.rstrip("/")

    def resolve(self, city: str, country_code: str) -> Place:
        data = self._get(
            "/searchJSON",
            {
                "q": city,
                "country": country_code,
                "featureClass": "P",
                "orderby": "population",
                "maxRows": 1,
            },
        )
        results = data.get("geonames") or []
        if not results:
            raise PlaceNotFoundError(
                "No place found. Check the city name and country code, "
                "and add the region if the name is ambiguous."
            )
        top = results[0]
        latitude = float(top["lat"])
        longitude = float(top["lng"])
        return Place(
            name=top.get("name", city),
            country_code=top.get("countryCode", country_code),
            latitude=latitude,
            longitude=longitude,
            timezone=self._timezone(latitude, longitude),
            admin_area=top.get("adminName1") or None,
        )

    def _timezone(self, latitude: float, longitude: float) -> str | None:
        data = self._get("/timezoneJSON", {"lat": latitude, "lng": longitude})
        return data.get("timezoneId")

    def _get(self, path: str, params: dict[str, Any]) -> dict[str, Any]:
        try:
            response = self._client.get(
                f"{self._base_url}{path}", params={**params, "username": self._username}
            )
            response.raise_for_status()
            data = response.json()
        except (httpx.HTTPError, ValueError) as exc:
            raise GeocodingError("The GeoNames request failed.") from exc
        if "status" in data:
            raise GeocodingError("GeoNames returned an error for this request.")
        return data
