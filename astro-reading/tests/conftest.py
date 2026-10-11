from datetime import date, time

import pytest

from astro_reading.models import BirthData, ReadingRequest, ReadingType

# All data in the test suite is fictitious.


@pytest.fixture
def birth() -> BirthData:
    return BirthData(
        birth_date=date(1990, 5, 17),
        birth_time=time(14, 30),
        city="Lisboa",
        country_code="PT",
        name="Test Person",
    )


@pytest.fixture
def natal_request(birth: BirthData) -> ReadingRequest:
    return ReadingRequest(birth=birth, reading_type=ReadingType.NATAL, theme="Career and purpose")


@pytest.fixture
def solar_return_request(birth: BirthData) -> ReadingRequest:
    return ReadingRequest(
        birth=birth,
        reading_type=ReadingType.SOLAR_RETURN,
        theme="Relationships",
        solar_return_year=2026,
        solar_return_city="Porto",
        solar_return_country_code="PT",
    )
