from datetime import date, time

import pytest

from astro_reading.errors import ValidationError
from astro_reading.validation import (
    normalize_country_code,
    parse_date,
    parse_time,
    parse_year,
    require_text,
)


def test_parse_date_accepts_iso_format():
    assert parse_date("1990-05-17") == date(1990, 5, 17)


@pytest.mark.parametrize("value", ["17/05/1990", "1990-13-01", "", "not a date"])
def test_parse_date_rejects_bad_input(value):
    with pytest.raises(ValidationError):
        parse_date(value)


def test_parse_time_accepts_24_hour_clock():
    assert parse_time("14:30") == time(14, 30)


@pytest.mark.parametrize("value", ["25:00", "14h30", "", "2:30 PM"])
def test_parse_time_rejects_bad_input(value):
    with pytest.raises(ValidationError):
        parse_time(value)


def test_country_code_is_normalized():
    assert normalize_country_code(" pt ") == "PT"


@pytest.mark.parametrize("value", ["", "P", "PRT", "P1"])
def test_country_code_rejects_bad_input(value):
    with pytest.raises(ValidationError):
        normalize_country_code(value)


def test_parse_year():
    assert parse_year("2026") == 2026
    with pytest.raises(ValidationError):
        parse_year("abc")
    with pytest.raises(ValidationError):
        parse_year("26")


def test_require_text():
    assert require_text("  hello ", "Field") == "hello"
    with pytest.raises(ValidationError):
        require_text("   ", "Field")
