"""Error policy for non-fatal scanner and plugin failures."""

from __future__ import annotations

import logging
from dataclasses import dataclass

logger = logging.getLogger(__name__)


@dataclass(frozen=True, slots=True)
class ScanWarning:
    source: str
    message: str


class ErrorHandler:
    """Logs scanner errors and converts them into warnings so scans continue."""

    def handle(self, source: str, error: Exception) -> ScanWarning:
        logger.exception("%s failed during scan", source)
        return ScanWarning(source=source, message=str(error))
