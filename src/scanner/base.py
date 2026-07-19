"""Base scanner contract."""

from __future__ import annotations

from abc import ABC, abstractmethod

from src.models import ScanContext, ScanResult, ScanTask


class BaseScanner(ABC):
    """Scanner provider interface for the engine."""

    name: str = "scanner"

    def prepare(self, context: ScanContext) -> list[ScanTask]:
        return [ScanTask(scanner_name=self.name)]

    @abstractmethod
    def scan(self, context: ScanContext, task: ScanTask) -> ScanResult:
        """Execute a single scan task."""
