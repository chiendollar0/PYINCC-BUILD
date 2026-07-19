"""High-level scan manager and task scheduler."""

from __future__ import annotations

from concurrent.futures import ThreadPoolExecutor, as_completed

from src.models import ScanContext, ScanReport, ScanTask
from src.plugins.base import BasePlugin
from src.plugins.loader import PluginLoader
from src.plugins.manager import PluginManager
from src.scanner.base import BaseScanner
from src.scanner.collector import ResultCollector
from src.scanner.errors import ErrorHandler
from src.scanner.events import EventBus, EventType
from src.scanner.pipeline import ScanPipeline
from src.scanner.progress import ProgressManager, ProgressState
from src.scanner.scanner import ScannerRegistry


class TaskScheduler:
    """Prepares tasks from registered scanners."""

    def __init__(self, registry: ScannerRegistry) -> None:
        self._registry = registry

    def prepare(self, context: ScanContext) -> list[ScanTask]:
        tasks: list[ScanTask] = []
        for scanner in self._registry.all():
            tasks.extend(scanner.prepare(context))
        return tasks


class ScanManager:
    """Coordinates the full scan lifecycle without blocking GUI callers unnecessarily."""

    def __init__(self, max_workers: int = 4) -> None:
        self.event_bus = EventBus()
        self.progress = ProgressManager(self.event_bus)
        self.errors = ErrorHandler()
        self.registry = ScannerRegistry()
        self.plugins = PluginManager(self.event_bus, self.errors)
        self.loader = PluginLoader(self.plugins)
        self.max_workers = max_workers

    def register_scanner(self, scanner: BaseScanner) -> None:
        self.registry.register(scanner)

    def register_plugin(self, plugin: BasePlugin, context: ScanContext | None = None) -> None:
        self.plugins.register(plugin, context=context)

    def run(self, context: ScanContext | None = None) -> ScanReport:
        context = context or ScanContext()
        collector = ResultCollector(context.session_id)
        collector._report.started_at = context.started_at
        scheduler = TaskScheduler(self.registry)
        self.event_bus.publish(EventType.SCAN_STARTED, context=context)
        self.progress.update(ProgressState.PREPARING, message="Preparing tasks")
        tasks = scheduler.prepare(context)
        self.progress.update(ProgressState.SCANNING, completed_tasks=0, total_tasks=len(tasks))
        pipeline = ScanPipeline(self.registry, self.plugins, collector, self.progress, self.event_bus, self.errors)
        completed = 0
        with ThreadPoolExecutor(max_workers=self.max_workers) as executor:
            futures = [executor.submit(pipeline.execute_task, context, task) for task in tasks]
            for future in as_completed(futures):
                future.result()
                completed += 1
                self.progress.update(ProgressState.SCANNING, completed_tasks=completed, total_tasks=len(tasks))
        pipeline.collect(completed, len(tasks))
        self.progress.update(ProgressState.FINALIZING, completed_tasks=completed, total_tasks=len(tasks))
        report = collector.finalize()
        self.progress.update(ProgressState.COMPLETED, completed_tasks=completed, total_tasks=len(tasks))
        self.event_bus.publish(EventType.SCAN_FINISHED, report=report)
        return report
