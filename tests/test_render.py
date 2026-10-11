from datetime import datetime

from astro_reading.render import build_filename, render_markdown, save_markdown, slugify

NOW = datetime(2026, 10, 11, 17, 30, 0)


def test_slugify_removes_accents_and_symbols():
    assert slugify("Amor & Relações!") == "amor-relacoes"


def test_slugify_has_a_fallback():
    assert slugify("???") == "reading"


def test_filename_never_contains_name_or_birth_date(natal_request):
    filename = build_filename(natal_request, NOW)
    assert filename == "20261011-173000_natal_career-and-purpose.md"
    assert "test" not in filename.lower()
    assert "1990" not in filename


def test_markdown_hides_identity_by_default(natal_request):
    document = render_markdown(natal_request, "Reading text.", NOW)
    assert "Test Person" not in document
    assert "1990-05-17" not in document
    assert "Reading text." in document


def test_markdown_can_include_identity_when_requested(natal_request):
    document = render_markdown(natal_request, "Reading text.", NOW, include_identity=True)
    assert "Test Person" in document
    assert "1990-05-17" in document


def test_solar_return_header_shows_year(solar_return_request):
    document = render_markdown(solar_return_request, "Text.", NOW)
    assert "**Year:** 2026" in document


def test_save_markdown_does_not_overwrite(tmp_path):
    path = save_markdown("first", tmp_path, "a.md")
    assert path.read_text(encoding="utf-8") == "first"
    try:
        save_markdown("second", tmp_path, "a.md")
    except FileExistsError:
        pass
    else:
        raise AssertionError("expected FileExistsError")
    assert path.read_text(encoding="utf-8") == "first"
