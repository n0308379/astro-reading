"""Exceptions raised by astro_reading.

Error messages must never include birth data or other personal input.
"""


class AstroReadingError(Exception):
    """Base class for all errors raised by this package."""


class ValidationError(AstroReadingError, ValueError):
    """User input is missing or malformed."""


class ConfigurationError(AstroReadingError):
    """A required setting, such as an API key, is missing."""


class PlaceNotFoundError(AstroReadingError):
    """A place could not be resolved to coordinates."""


class GeocodingError(AstroReadingError):
    """The geocoding service returned an error."""


class ChartProviderError(AstroReadingError):
    """The chart calculation service returned an error."""


class WriterError(AstroReadingError):
    """The reading writer (LLM) returned an error."""
