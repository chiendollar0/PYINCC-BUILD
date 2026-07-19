"""Plugin loader utilities."""

from __future__ import annotations

from collections.abc import Iterable

from src.plugins.base import BasePlugin
from src.plugins.manager import PluginManager
from src.models import ScanContext


class PluginLoader:
    """Loads explicitly provided plugin instances into a manager."""

    def __init__(self, manager: PluginManager) -> None:
        self._manager = manager

    def load(self, plugins: Iterable[BasePlugin], context: ScanContext | None = None) -> None:
        for plugin in plugins:
            self._manager.register(plugin, context=context)
