"""Progress state management for scan sessions."""

from __future__ import annotations

from dataclasses import dataclass
from enum import Enum
from threading import RLock

from src.scanner.events import EventBus, EventType


class ProgressState(str, Enum):
    PREPARING = "Preparing"
    SCANNING = "Scanning"
    COLLECTING = "Collecting"
    FINALIZING = "Finalizing"
    COMPLETED = "Completed"
    CANCELLED = "Cancelled"
    FAILED = "Failed"


@dataclass(frozen=True, slots=True)
class ProgressSnapshot:
    state: ProgressState
    completed_tasks: int = 0
    total_tasks: int = 0
    message: str = ""


class ProgressManager:
    def __init__(self, event_bus: EventBus | None = None) -> None:
        self._event_bus = event_bus
        self._snapshot = ProgressSnapshot(state=ProgressState.PREPARING)
        self._lock = RLock()

    @property
    def snapshot(self) -> ProgressSnapshot:
        with self._lock:
            return self._snapshot

    def update(self, state: ProgressState, completed_tasks: int | None = None, total_tasks: int | None = None, message: str = "") -> ProgressSnapshot:
        with self._lock:
            current = self._snapshot
            self._snapshot = ProgressSnapshot(
                state=state,
                completed_tasks=current.completed_tasks if completed_tasks is None else completed_tasks,
                total_tasks=current.total_tasks if total_tasks is None else total_tasks,
                message=message,
            )
            snapshot = self._snapshot
        if self._event_bus:
            self._event_bus.publish(EventType.PROGRESS_CHANGED, snapshot=snapshot)
        return snapshot
