"""Parsing and validation of user input."""

from __future__ import annotations

from datetime import date, datetime, time

from .errors import ValidationError


def parse_date(value: str) -> date:
    """Parse a date written as YYYY-MM-DD."""
    try:
        return date.fromisoformat(value.strip())
    except (ValueError, AttributeError) as exc:
        raise ValidationError("Date must be in the format YYYY-MM-DD.") from exc


def parse_time(value: str) -> time:
    """Parse a time written as HH:MM (24-hour clock)."""
    try:
        return datetime.strptime(value.strip(), "%H:%M").time()
    except (ValueError, AttributeError) as exc:
        raise ValidationError("Time must be in the format HH:MM (24-hour clock).") from exc


def normalize_country_code(value: str) -> str:
    """Return an upper-case ISO 3166-1 alpha-2 code."""
    code = (value or "").strip().upper()
    if len(code) != 2 or not code.isalpha():
        raise ValidationError("Country must be a 2-letter ISO code, for example PT.")
    return code


def parse_year(value: str | int) -> int:
    """Parse a four-digit year."""
    try:
        year = int(value)
    except (TypeError, ValueError) as exc:
        raise ValidationError("Year must be a number, for example 2026.") from exc
    if not 1000 <= year <= 9999:
        raise ValidationError("Year must have four digits.")
    return year


def require_text(value: str | None, field: str) -> str:
    """Return stripped text, or raise if it is empty."""
    text = (value or "").strip()
    if not text:
        raise ValidationError(f"{field} is required.")
    return text
