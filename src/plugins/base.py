"""Base contracts for scan plugins."""

from __future__ import annotations

from abc import ABC, abstractmethod

from src.models import PluginResult, ScanContext, ScanResult


class BasePlugin(ABC):
    """Plugin provider interface used by the scanner engine."""

    name: str = "plugin"

    def setup(self, context: ScanContext) -> None:
        """Prepare the plugin for a scan session."""

    @abstractmethod
    def run(self, context: ScanContext, result: ScanResult) -> PluginResult:
        """Process a scanner result and return plugin output."""
