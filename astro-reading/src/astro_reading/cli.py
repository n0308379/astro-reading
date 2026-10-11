"""Command-line interface."""

from __future__ import annotations

import argparse
import os
import sys
from collections.abc import Sequence
from datetime import datetime
from pathlib import Path

from .chart import AstrologerApiProvider
from .errors import AstroReadingError, ConfigurationError, ValidationError
from .geocode import GeoNamesGeocoder
from .knowledge import InMemoryKnowledgeBase
from .models import BirthData, Place, ReadingRequest, ReadingType
from .offline import OfflineChartProvider, OfflineGeocoder
from .providers import ChartProvider, Geocoder, KnowledgeBase, ReadingWriter
from .render import build_filename, render_markdown, save_markdown
from .service import generate_reading, resolve_places
from .validation import (
    normalize_country_code,
    parse_date,
    parse_time,
    parse_year,
    require_text,
)
from .writer import AnthropicWriter, OfflineWriter


def build_parser() -> argparse.ArgumentParser:
    parser = argparse.ArgumentParser(
        prog="astro-reading",
        description="Generate a narrative astrology reading (natal chart or solar return).",
    )
    parser.add_argument("--date", required=True, help="Birth date, YYYY-MM-DD")
    parser.add_argument("--time", required=True, help="Birth time, HH:MM (24-hour)")
    parser.add_argument("--city", required=True, help="Birth city")
    parser.add_argument("--country", required=True, help="Birth country, 2-letter ISO code")
    parser.add_argument("--theme", required=True, help="Theme of the reading")
    parser.add_argument(
        "--type",
        dest="reading_type",
        choices=["natal", "solar-return"],
        default="natal",
        help="Type of reading (default: natal)",
    )
    parser.add_argument("--year", help="Year of the solar return")
    parser.add_argument("--return-city", help="City of the solar return (default: birth city)")
    parser.add_argument("--return-country", help="Country of the solar return (default: birth)")
    parser.add_argument("--name", help="Optional name, only used if --include-identity is set")
    parser.add_argument("--knowledge-dir", type=Path, help="Folder with .txt/.md reference files")
    parser.add_argument("--output-dir", type=Path, default=Path("output"), help="Where to save")
    parser.add_argument("--stdout", action="store_true", help="Print the reading, do not save")
    parser.add_argument(
        "--include-identity",
        action="store_true",
        help="Write the name and birth date into the saved file",
    )
    parser.add_argument("--yes", action="store_true", help="Skip the place confirmation")
    parser.add_argument(
        "--offline", action="store_true", help="Use fictitious offline data, no services"
    )
    return parser


def build_request(args: argparse.Namespace) -> ReadingRequest:
    """Validate command-line input and build a ReadingRequest."""
    birth = BirthData(
        birth_date=parse_date(args.date),
        birth_time=parse_time(args.time),
        city=require_text(args.city, "City"),
        country_code=normalize_country_code(args.country),
        name=(args.name or "").strip() or None,
    )
    reading_type = ReadingType.SOLAR_RETURN if args.reading_type == "solar-return" else (
        ReadingType.NATAL
    )
    year = parse_year(args.year) if args.year else None
    return_country = normalize_country_code(args.return_country) if args.return_country else None
    return ReadingRequest(
        birth=birth,
        reading_type=reading_type,
        theme=require_text(args.theme, "Theme"),
        solar_return_year=year,
        solar_return_city=(args.return_city or "").strip() or None,
        solar_return_country_code=return_country,
    )


def _env(name: str) -> str:
    value = os.environ.get(name, "").strip()
    if not value:
        raise ConfigurationError(f"Missing environment variable {name}.")
    return value


def build_services(
    *, offline: bool, knowledge_dir: Path | None
) -> tuple[Geocoder, ChartProvider, KnowledgeBase, ReadingWriter]:
    """Create the services for a run, from environment variables unless offline."""
    knowledge: KnowledgeBase = (
        InMemoryKnowledgeBase.from_directory(knowledge_dir)
        if knowledge_dir
        else InMemoryKnowledgeBase([])
    )
    if offline:
        return OfflineGeocoder(), OfflineChartProvider(), knowledge, OfflineWriter()

    geonames_username = _env("GEONAMES_USERNAME")
    geocoder = GeoNamesGeocoder(geonames_username)
    chart = AstrologerApiProvider(_env("RAPIDAPI_KEY"), geonames_username)
    writer = AnthropicWriter(
        _env("ANTHROPIC_API_KEY"),
        model=os.environ.get("ANTHROPIC_MODEL", "claude-sonnet-5-5"),
    )
    return geocoder, chart, knowledge, writer


def confirm_places(birth_place: Place, return_place: Place | None) -> bool:
    """Ask the user to confirm the resolved places."""
    print(f"Birth place: {birth_place.describe()}")
    if return_place is not None:
        print(f"Solar return place: {return_place.describe()}")
    answer = input("Are these places correct? [y/N] ").strip().lower()
    return answer in {"y", "yes", "s", "sim"}


def main(argv: Sequence[str] | None = None) -> int:
    args = build_parser().parse_args(argv)
    try:
        request = build_request(args)
        geocoder, chart, knowledge, writer = build_services(
            offline=args.offline, knowledge_dir=args.knowledge_dir
        )
        birth_place, return_place = resolve_places(request, geocoder)
        if not args.yes and not confirm_places(birth_place, return_place):
            print("Cancelled. Adjust the city or add the region and try again.", file=sys.stderr)
            return 1
        reading = generate_reading(
            request,
            birth_place=birth_place,
            return_place=return_place,
            chart_provider=chart,
            knowledge_base=knowledge,
            writer=writer,
        )
    except (AstroReadingError, ValidationError) as exc:
        print(f"Error: {exc}", file=sys.stderr)
        return 1

    now = datetime.now()
    document = render_markdown(request, reading, now, include_identity=args.include_identity)
    if args.stdout:
        print(document)
        return 0
    path = save_markdown(document, args.output_dir, build_filename(request, now))
    print(f"Saved: {path}")
    return 0


if __name__ == "__main__":
    sys.exit(main())
