"""Result collector for normalized report output."""

from __future__ import annotations

from datetime import datetime, timezone
from threading import RLock

from src.models import ScanReport, ScanResult


class ResultCollector:
    def __init__(self, session_id: str) -> None:
        self._report = ScanReport(session_id=session_id)
        self._lock = RLock()

    def receive(self, result: ScanResult) -> None:
        with self._lock:
            self._report.software.extend(result.software)
            self._report.evidence.extend(result.evidence)
            self._report.warnings.extend(result.warnings)
            for plugin_result in result.plugin_results:
                self._report.software.extend(plugin_result.software)
                self._report.evidence.extend(plugin_result.evidence)
                self._report.warnings.extend(plugin_result.warnings)

    def finalize(self) -> ScanReport:
        with self._lock:
            self._report.finished_at = datetime.now(timezone.utc)
            return self._report
