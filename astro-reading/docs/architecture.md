# Architecture

## Flow

1. `cli.py` parses and validates the input (`validation.py`) into a `ReadingRequest` (`models.py`).
2. `service.resolve_places` resolves the birth place, and the return place for a solar return, through a `Geocoder`.
3. The user confirms the places.
4. `service.generate_reading` asks a `ChartProvider` for the chart, a `KnowledgeBase` for passages about the theme, and a `ReadingWriter` for the final text.
5. `render.py` builds the Markdown document and a privacy-safe file name.

## Interfaces

Defined in `providers.py` as `typing.Protocol` classes:

| Interface | Default | Offline |
|-----------|---------|---------|
| `Geocoder` | `GeoNamesGeocoder` | `OfflineGeocoder` |
| `ChartProvider` | `AstrologerApiProvider` | `OfflineChartProvider` |
| `KnowledgeBase` | `InMemoryKnowledgeBase` | same |
| `ReadingWriter` | `AnthropicWriter` | `OfflineWriter` |

Keeping services behind interfaces means a provider can be swapped (for example a local ephemeris library, or a Qdrant-backed knowledge base) without touching the orchestration code.

## Errors

All errors derive from `AstroReadingError` (`errors.py`). Messages never contain user input, so they are safe to print or log.
