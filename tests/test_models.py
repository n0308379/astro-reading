import pytest

from astro_reading.errors import ValidationError
from astro_reading.models import Place, ReadingRequest, ReadingType


def test_solar_return_requires_a_year(birth):
    with pytest.raises(ValidationError):
        ReadingRequest(birth=birth, reading_type=ReadingType.SOLAR_RETURN, theme="Love")


def test_theme_is_required(birth):
    with pytest.raises(ValidationError):
        ReadingRequest(birth=birth, reading_type=ReadingType.NATAL, theme="   ")


def test_return_place_defaults_to_birth_place(birth):
    request = ReadingRequest(
        birth=birth,
        reading_type=ReadingType.SOLAR_RETURN,
        theme="Love",
        solar_return_year=2026,
    )
    assert request.return_city == birth.city
    assert request.return_country_code == birth.country_code


def test_place_description_includes_region_when_known():
    place = Place("Lisboa", "PT", 38.7167, -9.1333, "Europe/Lisbon", "Lisboa")
    assert place.describe().startswith("Lisboa, Lisboa, PT")
