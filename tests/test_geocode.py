import httpx
import pytest

from astro_reading.errors import GeocodingError, PlaceNotFoundError
from astro_reading.geocode import GeoNamesGeocoder


def make_geocoder(handler) -> GeoNamesGeocoder:
    client = httpx.Client(transport=httpx.MockTransport(handler))
    return GeoNamesGeocoder("demo-user", client=client)


def test_resolves_place_and_timezone():
    def handler(request: httpx.Request) -> httpx.Response:
        if request.url.path == "/searchJSON":
            assert request.url.params["q"] == "Lisboa"
            assert request.url.params["country"] == "PT"
            assert request.url.params["username"] == "demo-user"
            return httpx.Response(
                200,
                json={
                    "geonames": [
                        {
                            "name": "Lisboa",
                            "countryCode": "PT",
                            "lat": "38.71667",
                            "lng": "-9.13333",
                            "adminName1": "Lisboa",
                        }
                    ]
                },
            )
        return httpx.Response(200, json={"timezoneId": "Europe/Lisbon"})

    place = make_geocoder(handler).resolve("Lisboa", "PT")
    assert place.name == "Lisboa"
    assert place.timezone == "Europe/Lisbon"
    assert place.latitude == pytest.approx(38.71667)


def test_unknown_place_raises():
    geocoder = make_geocoder(lambda request: httpx.Response(200, json={"geonames": []}))
    with pytest.raises(PlaceNotFoundError):
        geocoder.resolve("Nowhere", "PT")


def test_service_error_status_raises():
    geocoder = make_geocoder(
        lambda request: httpx.Response(200, json={"status": {"message": "limit reached"}})
    )
    with pytest.raises(GeocodingError):
        geocoder.resolve("Lisboa", "PT")


def test_http_failure_raises_without_leaking_input():
    geocoder = make_geocoder(lambda request: httpx.Response(500))
    with pytest.raises(GeocodingError) as info:
        geocoder.resolve("Lisboa", "PT")
    assert "Lisboa" not in str(info.value)
