import json

import httpx
import pytest

from astro_reading.errors import WriterError
from astro_reading.models import ReadingType
from astro_reading.writer import AnthropicWriter, OfflineWriter, build_prompt


def make_writer(handler) -> AnthropicWriter:
    client = httpx.Client(transport=httpx.MockTransport(handler))
    return AnthropicWriter("fake-key", client=client)


def test_prompt_contains_theme_chart_and_references():
    prompt = build_prompt("Career", ReadingType.NATAL, "<chart/>", ["passage one"])
    assert "THEME: Career" in prompt
    assert "<chart/>" in prompt
    assert "passage one" in prompt


def test_prompt_marks_missing_references():
    assert "(none)" in build_prompt("Career", ReadingType.NATAL, "<chart/>", [])


def test_request_and_response_handling():
    seen = {}

    def handler(request: httpx.Request) -> httpx.Response:
        seen["headers"] = request.headers
        seen["body"] = json.loads(request.content)
        blocks = [
            {"type": "text", "text": "Part one. "},
            {"type": "text", "text": "Part two."},
        ]
        return httpx.Response(200, json={"content": blocks})

    text = make_writer(handler).write(
        theme="Career", reading_type=ReadingType.NATAL, chart_context="<chart/>", references=[]
    )

    assert text == "Part one. Part two."
    assert seen["headers"]["x-api-key"] == "fake-key"
    assert seen["body"]["messages"][0]["role"] == "user"
    assert "European Portuguese" in seen["body"]["system"]


@pytest.mark.parametrize(
    "response",
    [httpx.Response(500), httpx.Response(200, json={"content": []})],
)
def test_failures_raise(response):
    writer = make_writer(lambda request: response)
    with pytest.raises(WriterError):
        writer.write(
            theme="Career", reading_type=ReadingType.NATAL, chart_context="<chart/>", references=[]
        )


def test_offline_writer_is_deterministic():
    writer = OfflineWriter()
    kwargs = dict(
        theme="Career", reading_type=ReadingType.NATAL, chart_context="<chart/>", references=["a"]
    )
    assert writer.write(**kwargs) == writer.write(**kwargs)
