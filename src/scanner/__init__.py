"""Scanner engine framework for PYINCC."""

from src.scanner.base import BaseScanner
from src.scanner.collector import ResultCollector
from src.scanner.errors import ErrorHandler, ScanWarning
from src.scanner.events import EventBus, EventType, ScanEvent
from src.scanner.progress import ProgressManager, ProgressSnapshot, ProgressState
from src.scanner.scanner import ScannerRegistry

__all__ = [
    "BaseScanner",
    "ErrorHandler",
    "EventBus",
    "EventType",
    "ProgressManager",
    "ProgressSnapshot",
    "ProgressState",
    "ResultCollector",
    "ScanEvent",
    "ScanManager",
    "ScanPipeline",
    "ScanWarning",
    "ScannerRegistry",
    "TaskScheduler",
]


def __getattr__(name: str):
    if name in {"ScanManager", "TaskScheduler"}:
        from src.scanner.manager import ScanManager, TaskScheduler

        return {"ScanManager": ScanManager, "TaskScheduler": TaskScheduler}[name]
    if name == "ScanPipeline":
        from src.scanner.pipeline import ScanPipeline

        return ScanPipeline
    raise AttributeError(name)
