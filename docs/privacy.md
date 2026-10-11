# Privacy

Birth date, time and place are personal data. This document says exactly where they go.

## What the tool stores

- No database. No cache of birth data. No logs of input.
- One output file, only when you do not use `--stdout`. Its name contains a timestamp, the reading type and the theme. Its content includes the name and birth date only with `--include-identity`.

## What leaves your machine

| Data | Sent to | Why |
|------|---------|-----|
| City and country | GeoNames | Resolve coordinates and time zone |
| Birth date, time, city, country, optional name | Astrologer API (via RapidAPI) | Calculate the chart |
| Chart data and the theme | Anthropic | Write the reading |

If no name is given, the neutral label `Subject` is sent instead.

Each of these providers has its own terms and retention policy. Read them before using real data about other people.

## Rules for contributors and tests

- Use fictitious data only. Never commit real birth data.
- Never commit API keys. `.env` is ignored by git.
- Error messages and logs must not include user input.
- Tests mock all network calls.
