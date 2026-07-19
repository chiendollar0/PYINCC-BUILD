"""Scan pipeline execution."""

from __future__ import annotations

from src.models import ScanContext, ScanResult, ScanTask, TaskStatus
from src.plugins.manager import PluginManager
from src.scanner.collector import ResultCollector
from src.scanner.errors import ErrorHandler
from src.scanner.events import EventBus, EventType
from src.scanner.progress import ProgressManager, ProgressState
from src.scanner.scanner import ScannerRegistry


class ScanPipeline:
    """Runs scanner tasks, dispatches plugins, and collects results."""

    def __init__(
        self,
        registry: ScannerRegistry,
        plugins: PluginManager,
        collector: ResultCollector,
        progress: ProgressManager,
        event_bus: EventBus,
        error_handler: ErrorHandler | None = None,
    ) -> None:
        self._registry = registry
        self._plugins = plugins
        self._collector = collector
        self._progress = progress
        self._event_bus = event_bus
        self._error_handler = error_handler or ErrorHandler()

    def execute_task(self, context: ScanContext, task: ScanTask) -> ScanResult:
        task.status = TaskStatus.RUNNING
        self._event_bus.publish(EventType.TASK_STARTED, task=task)
        try:
            result = self._registry.get(task.scanner_name).scan(context, task)
            result.plugin_results.extend(self._plugins.dispatch(context, result))
            task.status = TaskStatus.COMPLETED if not result.warnings else TaskStatus.WARNING
        except Exception as exc:
            warning = self._error_handler.handle(task.scanner_name, exc)
            task.status = TaskStatus.WARNING
            task.warning = warning.message
            result = ScanResult(task_id=task.task_id, scanner_name=task.scanner_name, warnings=[warning.message])
        self._collector.receive(result)
        self._event_bus.publish(EventType.TASK_FINISHED, task=task, result=result)
        return result

    def collect(self, completed: int, total: int) -> None:
        self._progress.update(ProgressState.COLLECTING, completed_tasks=completed, total_tasks=total)
