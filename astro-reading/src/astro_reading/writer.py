"""Writers that turn chart data and references into a narrative reading."""

from __future__ import annotations

import httpx

from .errors import WriterError
from .models import ReadingType

DEFAULT_SYSTEM_PROMPT = """\
You write astrology readings as a warm, reflective narrative with a beginning, \
a middle and an end, not as a list of technical aspects.

You receive calculated chart data, optional reference passages, and one theme \
requested by the reader. Rules:
- Focus only on the requested theme and the chart elements relevant to it.
- Never invent or change chart values. If a needed value is missing from the \
data, say so.
- Use the reference passages to ground the interpretation, but do not quote \
them. Express the ideas in your own words.
- Present tendencies as possibilities for self-observation, never as fixed \
destiny or certainty.
- End with a short question that invites the reader to reflect on the theme.
- Write in {language}.
"""


class AnthropicWriter:
    """Write a reading with the Anthropic Messages API."""

    API_URL = "https://api.anthropic.com/v1/messages"
    API_VERSION = "2023-06-01"

    def __init__(
        self,
        api_key: str,
        model: str = "claude-sonnet-5-5",
        language: str = "European Portuguese",
        max_tokens: int = 4096,
        client: httpx.Client | None = None,
    ) -> None:
        self._api_key = api_key
        self._model = model
        self._language = language
        self._max_tokens = max_tokens
        self._client = client or httpx.Client(timeout=120.0)

    def write(
        self,
        *,
        theme: str,
        reading_type: ReadingType,
        chart_context: str,
        references: list[str],
    ) -> str:
        body = {
            "model": self._model,
            "max_tokens": self._max_tokens,
            "system": DEFAULT_SYSTEM_PROMPT.format(language=self._language),
            "messages": [
                {
                    "role": "user",
                    "content": build_prompt(theme, reading_type, chart_context, references),
                }
            ],
        }
        headers = {
            "x-api-key": self._api_key,
            "anthropic-version": self.API_VERSION,
            "content-type": "application/json",
        }
        try:
            response = self._client.post(self.API_URL, headers=headers, json=body)
            response.raise_for_status()
            data = response.json()
        except (httpx.HTTPError, ValueError) as exc:
            raise WriterError("The writing service request failed.") from exc
        blocks = data.get("content") or []
        text = "".join(b.get("text", "") for b in blocks if b.get("type") == "text").strip()
        if not text:
            raise WriterError("The writing service returned no text.")
        return text


class OfflineWriter:
    """Deterministic writer for tests and demos. It does not call any service."""

    def write(
        self,
        *,
        theme: str,
        reading_type: ReadingType,
        chart_context: str,
        references: list[str],
    ) -> str:
        label = "natal chart" if reading_type is ReadingType.NATAL else "solar return"
        return (
            f"Offline demo reading ({label}) on the theme: {theme}.\n\n"
            f"This text was produced without a writing service. "
            f"{len(references)} reference passage(s) were retrieved."
        )


def build_prompt(
    theme: str, reading_type: ReadingType, chart_context: str, references: list[str]
) -> str:
    """Assemble the user message sent to the writing service."""
    label = "Natal chart" if reading_type is ReadingType.NATAL else "Solar return"
    refs = "\n---\n".join(references) if references else "(none)"
    return (
        f"THEME: {theme}\n"
        f"READING TYPE: {label}\n\n"
        f"CHART DATA:\n{chart_context}\n\n"
        f"REFERENCE PASSAGES:\n{refs}"
    )
