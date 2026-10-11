"""Turn a finished reading into a Markdown file.

Privacy rules: the file name never contains a name or a birth date, and the
birth date is not written into the file unless explicitly requested.
"""

from __future__ import annotations

import re
import unicodedata
from datetime import datetime
from pathlib import Path

from .models import ReadingRequest, ReadingType

_MAX_SLUG_LENGTH = 40


def slugify(text: str) -> str:
    """Lower-case ASCII slug, safe to use in a file name."""
    folded = unicodedata.normalize("NFKD", text).encode("ascii", "ignore").decode("ascii")
    slug = re.sub(r"[^a-z0-9]+", "-", folded.lower()).strip("-")
    return slug[:_MAX_SLUG_LENGTH].strip("-") or "reading"


def build_filename(request: ReadingRequest, now: datetime) -> str:
    """File name made of a timestamp, the reading type and the theme only."""
    return f"{now:%Y%m%d-%H%M%S}_{request.reading_type.value}_{slugify(request.theme)}.md"


def render_markdown(
    request: ReadingRequest,
    reading: str,
    now: datetime,
    *,
    include_identity: bool = False,
) -> str:
    """Build the Markdown document for a reading."""
    kind = "Natal chart" if request.reading_type is ReadingType.NATAL else "Solar return"
    lines = ["# Astrology reading", "", f"**Type:** {kind}"]
    if request.reading_type is ReadingType.SOLAR_RETURN:
        lines.append(f"**Year:** {request.solar_return_year}")
    lines.append(f"**Theme:** {request.theme}")
    lines.append(f"**Generated:** {now:%Y-%m-%d}")
    if include_identity:
        if request.birth.name:
            lines.append(f"**Name:** {request.birth.name}")
        lines.append(f"**Birth date:** {request.birth.birth_date.isoformat()}")
    lines += ["", "---", "", reading.strip(), ""]
    return "\n".join(lines)


def save_markdown(content: str, directory: Path, filename: str) -> Path:
    """Write the file, refusing to overwrite an existing one."""
    directory.mkdir(parents=True, exist_ok=True)
    path = directory / filename
    with path.open("x", encoding="utf-8") as handle:
        handle.write(content)
    return path
