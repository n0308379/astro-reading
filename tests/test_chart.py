import json

import httpx
import pytest

from astro_reading.chart import AstrologerApiProvider
from astro_reading.errors import ChartProviderError
from astro_reading.models import Place

LISBON = Place("Lisboa", "PT", 38.7167, -9.1333, "Europe/Lisbon")


def make_provider(handler) -> AstrologerApiProvider:
    client = httpx.Client(transport=httpx.MockTransport(handler))
    return AstrologerApiProvider("fake-key", "demo-user", client=client)


def test_birth_chart_request_shape(birth):
    seen = {}

    def handler(request: httpx.Request) -> httpx.Response:
        seen["path"] = request.url.path
        seen["headers"] = request.headers
        seen["body"] = json.loads(request.content)
        return httpx.Response(200, json={"status": "OK", "context": "<chart/>"})

    context = make_provider(handler).birth_chart(birth, LISBON)

    assert context == "<chart/>"
    assert seen["path"] == "/api/v5/context/birth-chart"
    assert seen["headers"]["x-rapidapi-key"] == "fake-key"
    subject = seen["body"]["subject"]
    assert (subject["year"], subject["month"], subject["day"]) == (1990, 5, 17)
    assert (subject["hour"], subject["minute"]) == (14, 30)
    assert subject["nation"] == "PT"
    assert subject["geonames_username"] == "demo-user"


def test_neutral_name_is_sent_when_no_name_is_given(birth):
    from dataclasses import replace

    seen = {}

    def handler(request: httpx.Request) -> httpx.Response:
        seen["body"] = json.loads(request.content)
        return httpx.Response(200, json={"status": "OK", "context": "<chart/>"})

    make_provider(handler).birth_chart(replace(birth, name=None), LISBON)
    assert seen["body"]["subject"]["name"] == "Subject"


def test_solar_return_request_shape(birth):
    seen = {}

    def handler(request: httpx.Request) -> httpx.Response:
        seen["path"] = request.url.path
        seen["body"] = json.loads(request.content)
        return httpx.Response(200, json={"status": "OK", "context": "<chart/>"})

    make_provider(handler).solar_return(birth, LISBON, 2026, LISBON)

    assert seen["path"] == "/api/v5/context/solar-return"
    assert seen["body"]["year"] == 2026
    assert seen["body"]["return_location"]["timezone"] == "Europe/Lisbon"


def test_solar_return_needs_a_timezone(birth):
    no_timezone = Place("Lisboa", "PT", 38.7167, -9.1333, None)
    provider = make_provider(lambda request: httpx.Response(200, json={}))
    with pytest.raises(ChartProviderError):
        provider.solar_return(birth, LISBON, 2026, no_timezone)


@pytest.mark.parametrize(
    "response",
    [
        httpx.Response(500),
        httpx.Response(200, json={"status": "ERROR"}),
        httpx.Response(200, json={"status": "OK", "context": ""}),
    ],
)
def test_service_failures_raise(birth, response):
    provider = make_provider(lambda request: response)
    with pytest.raises(ChartProviderError):
        provider.birth_chart(birth, LISBON)
