"""Plugin registry and dispatcher."""

from __future__ import annotations

from src.models import PluginResult, ScanContext, ScanResult
from src.plugins.base import BasePlugin
from src.scanner.errors import ErrorHandler
from src.scanner.events import EventBus, EventType


class PluginManager:
    def __init__(self, event_bus: EventBus | None = None, error_handler: ErrorHandler | None = None) -> None:
        self._plugins: list[BasePlugin] = []
        self._event_bus = event_bus
        self._error_handler = error_handler or ErrorHandler()

    @property
    def plugins(self) -> tuple[BasePlugin, ...]:
        return tuple(self._plugins)

    def register(self, plugin: BasePlugin, context: ScanContext | None = None) -> None:
        if context is not None:
            plugin.setup(context)
        self._plugins.append(plugin)
        if self._event_bus:
            self._event_bus.publish(EventType.PLUGIN_LOADED, plugin=plugin.name)

    def dispatch(self, context: ScanContext, result: ScanResult) -> list[PluginResult]:
        plugin_results: list[PluginResult] = []
        for plugin in self._plugins:
            try:
                plugin_results.append(plugin.run(context, result))
            except Exception as exc:
                warning = self._error_handler.handle(plugin.name, exc)
                if self._event_bus:
                    self._event_bus.publish(EventType.PLUGIN_ERROR, plugin=plugin.name, error=exc)
                plugin_results.append(PluginResult(plugin_name=plugin.name, warnings=[warning.message]))
        return plugin_results
