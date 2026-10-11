from astro_reading.cli import main
from astro_reading.knowledge import InMemoryKnowledgeBase
from astro_reading.offline import OfflineChartProvider, OfflineGeocoder
from astro_reading.service import generate_reading, resolve_places
from astro_reading.writer import OfflineWriter


def test_natal_reading_end_to_end_offline(natal_request):
    birth_place, return_place = resolve_places(natal_request, OfflineGeocoder())
    assert return_place is None
    text = generate_reading(
        natal_request,
        birth_place=birth_place,
        return_place=return_place,
        chart_provider=OfflineChartProvider(),
        knowledge_base=InMemoryKnowledgeBase([]),
        writer=OfflineWriter(),
    )
    assert "natal chart" in text
    assert "Career and purpose" in text


def test_solar_return_resolves_both_places(solar_return_request):
    birth_place, return_place = resolve_places(solar_return_request, OfflineGeocoder())
    assert birth_place.name == "Lisboa"
    assert return_place is not None and return_place.name == "Porto"


BASE_ARGS = [
    "--date", "1990-05-17",
    "--time", "14:30",
    "--city", "Lisboa",
    "--country", "PT",
    "--theme", "Career",
    "--offline",
    "--yes",
]  # fmt: skip


def test_cli_prints_reading_to_stdout(capsys):
    assert main([*BASE_ARGS, "--stdout"]) == 0
    output = capsys.readouterr().out
    assert "# Astrology reading" in output
    assert "1990-05-17" not in output


def test_cli_saves_file_without_identity_in_name(tmp_path, capsys):
    assert main([*BASE_ARGS, "--output-dir", str(tmp_path)]) == 0
    files = list(tmp_path.glob("*.md"))
    assert len(files) == 1
    assert "1990" not in files[0].name
    assert "Saved:" in capsys.readouterr().out


def test_cli_reports_invalid_input_without_echoing_it(capsys):
    args = ["--date", "17/05/1990", *BASE_ARGS[2:], "--stdout"]
    assert main(args) == 1
    error = capsys.readouterr().err
    assert "YYYY-MM-DD" in error
    assert "17/05/1990" not in error


def test_cli_solar_return_needs_a_year(capsys):
    assert main([*BASE_ARGS, "--type", "solar-return", "--stdout"]) == 1
    assert "year" in capsys.readouterr().err.lower()


def test_cli_solar_return_offline(capsys):
    args = [*BASE_ARGS, "--type", "solar-return", "--year", "2026", "--stdout"]
    assert main(args) == 0
    assert "Solar return" in capsys.readouterr().out


def test_cli_stops_when_places_are_not_confirmed(monkeypatch, capsys):
    monkeypatch.setattr("builtins.input", lambda prompt="": "n")
    args = [a for a in BASE_ARGS if a != "--yes"] + ["--stdout"]
    assert main(args) == 1


def test_cli_online_mode_requires_credentials(monkeypatch, capsys):
    for name in ("GEONAMES_USERNAME", "RAPIDAPI_KEY", "ANTHROPIC_API_KEY"):
        monkeypatch.delenv(name, raising=False)
    args = [a for a in BASE_ARGS if a != "--offline"] + ["--stdout"]
    assert main(args) == 1
    assert "GEONAMES_USERNAME" in capsys.readouterr().err
