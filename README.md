# Astro Reading

A command-line tool that generates narrative astrology readings (natal chart or solar return) on a theme of your choice, and saves them as a Markdown file.

The chart is calculated by an ephemeris service, relevant reference passages are retrieved from a knowledge base, and an LLM writes the reading from those real chart values. The tool is designed for personal use and keeps no database.

## How it works

```
birth data ──> place lookup ──> you confirm the places
                                      │
              chart service <─────────┤
                    │                 │
                    ▼                 ▼
              chart context     reference passages (knowledge base)
                    └────────┬────────┘
                             ▼
                    LLM writes the reading ──> Markdown file
```

Every external service sits behind a small interface (`src/astro_reading/providers.py`), so it can be replaced by an offline implementation. The test suite and the demo mode run with no network and no credentials.

| Step | Default implementation |
|------|------------------------|
| Place and time zone lookup | GeoNames |
| Chart calculation | Astrologer API (RapidAPI) |
| Knowledge base | In-memory search over `.txt` / `.md` files |
| Reading generation | Anthropic Messages API |

## Quick start

Requires Python 3.10 or newer.

```bash
python -m venv .venv
source .venv/bin/activate
pip install -e ".[dev]"
```

Try it offline. This uses fictitious chart data and no services:

```bash
astro-reading --offline --yes --stdout \
  --date 1990-05-17 --time 14:30 --city Lisboa --country PT \
  --theme "Career and purpose"
```

Solar return:

```bash
astro-reading --offline --yes --stdout --type solar-return --year 2026 \
  --date 1990-05-17 --time 14:30 --city Lisboa --country PT \
  --return-city Porto --return-country PT --theme "Relationships"
```

## Using the real services

Copy `.env.example` to `.env`, fill it in, and load it into your shell (the tool reads environment variables, it does not read `.env` itself):

```bash
cp .env.example .env
set -a; source .env; set +a
astro-reading --date 1990-05-17 --time 14:30 --city Lisboa --country PT \
  --theme "Career and purpose" --knowledge-dir data/knowledge
```

Required variables: `GEONAMES_USERNAME`, `RAPIDAPI_KEY`, `ANTHROPIC_API_KEY`. Never commit your `.env`.

Reference material goes in `data/knowledge/` as `.txt` or `.md` files. It is excluded from git because it may be third-party content.

## Privacy

- No database is used and nothing is logged. The tool never writes birth data anywhere except the output file you ask for.
- Saved file names contain a timestamp, the reading type and the theme only. The name and birth date are written into the file only if you pass `--include-identity`. `--stdout` prints the reading without saving anything.
- The name is optional. When it is not given, a neutral label is sent to the chart service.
- To produce a reading, input data is sent to third-party services: birth details to the chart service and to the LLM provider, place names to GeoNames. See [docs/privacy.md](docs/privacy.md).
- Test data in this repository is fictitious. Use your own or fictitious data when trying the tool.

## Development

```bash
pytest
ruff check .
```

The tests mock every HTTP call. No test needs an API key.

Planned work is listed in [docs/backlog.md](docs/backlog.md).

## Project layout

```
src/astro_reading/   package: models, validation, providers, CLI
tests/               unit tests with fictitious data and mocked services
docs/                architecture, privacy, backlog
data/knowledge/      your reference files (not committed)
output/              generated readings (not committed)
```

## Status

Early work in progress.

## License

To be decided. Chart calculation is done through a hosted service. If an ephemeris library is ever bundled into this project (for example Swiss Ephemeris or Kerykeion, which are AGPL or dual-licensed), the license of this project will need to account for it.
