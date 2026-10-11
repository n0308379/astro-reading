"""Data models shared across the package."""

from __future__ import annotations

from dataclasses import dataclass
from datetime import date, time
from enum import Enum

from .errors import ValidationError


class ReadingType(str, Enum):
    NATAL = "natal"
    SOLAR_RETURN = "solar_return"


@dataclass(frozen=True)
class Place:
    """A resolved geographic place."""

    name: str
    country_code: str
    latitude: float
    longitude: float
    timezone: str | None = None
    admin_area: str | None = None

    def describe(self) -> str:
        parts = [self.name]
        if self.admin_area:
            parts.append(self.admin_area)
        parts.append(self.country_code)
        return f"{', '.join(parts)} (lat {self.latitude:.4f}, lng {self.longitude:.4f})"


@dataclass(frozen=True)
class BirthData:
    """Birth details. The name is optional and never required."""

    birth_date: date
    birth_time: time
    city: str
    country_code: str
    name: str | None = None


@dataclass(frozen=True)
class ReadingRequest:
    """Everything needed to generate one reading."""

    birth: BirthData
    reading_type: ReadingType
    theme: str
    solar_return_year: int | None = None
    solar_return_city: str | None = None
    solar_return_country_code: str | None = None

    def __post_init__(self) -> None:
        if not self.theme.strip():
            raise ValidationError("Theme is required.")
        if self.reading_type is ReadingType.SOLAR_RETURN and self.solar_return_year is None:
            raise ValidationError("A solar return reading needs a year.")

    @property
    def return_city(self) -> str:
        """City of the solar return, defaulting to the birth city."""
        return self.solar_return_city or self.birth.city

    @property
    def return_country_code(self) -> str:
        """Country of the solar return, defaulting to the birth country."""
        return self.solar_return_country_code or self.birth.country_code
