"""Orchestration: resolve places, fetch the chart, retrieve references, write."""

from __future__ import annotations

from .models import Place, ReadingRequest, ReadingType
from .providers import ChartProvider, Geocoder, KnowledgeBase, ReadingWriter


def resolve_places(request: ReadingRequest, geocoder: Geocoder) -> tuple[Place, Place | None]:
    """Resolve the birth place and, for a solar return, the return place."""
    birth_place = geocoder.resolve(request.birth.city, request.birth.country_code)
    return_place = None
    if request.reading_type is ReadingType.SOLAR_RETURN:
        return_place = geocoder.resolve(request.return_city, request.return_country_code)
    return birth_place, return_place


def generate_reading(
    request: ReadingRequest,
    *,
    birth_place: Place,
    return_place: Place | None,
    chart_provider: ChartProvider,
    knowledge_base: KnowledgeBase,
    writer: ReadingWriter,
) -> str:
    """Produce the reading text for an already-resolved request."""
    if request.reading_type is ReadingType.SOLAR_RETURN:
        if return_place is None or request.solar_return_year is None:
            raise ValueError("A solar return needs a year and a resolved return place.")
        chart = chart_provider.solar_return(
            request.birth, birth_place, request.solar_return_year, return_place
        )
    else:
        chart = chart_provider.birth_chart(request.birth, birth_place)

    references = knowledge_base.search(request.theme)
    return writer.write(
        theme=request.theme,
        reading_type=request.reading_type,
        chart_context=chart,
        references=references,
    )
