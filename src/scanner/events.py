"""Synchronous event bus for scanner lifecycle notifications."""

from __future__ import annotations

from dataclasses import dataclass, field
from datetime import datetime, timezone
from enum import Enum
from threading import RLock
from typing import Any, Callable


class EventType(str, Enum):
    SCAN_STARTED = "ScanStarted"
    TASK_STARTED = "TaskStarted"
    TASK_FINISHED = "TaskFinished"
    PROGRESS_CHANGED = "ProgressChanged"
    PLUGIN_LOADED = "PluginLoaded"
    PLUGIN_ERROR = "PluginError"
    SCAN_FINISHED = "ScanFinished"


@dataclass(frozen=True, slots=True)
class ScanEvent:
    type: EventType
    payload: dict[str, Any] = field(default_factory=dict)
    created_at: datetime = field(default_factory=lambda: datetime.now(timezone.utc))


EventHandler = Callable[[ScanEvent], None]


class EventBus:
    def __init__(self) -> None:
        self._handlers: dict[EventType, list[EventHandler]] = {}
        self._lock = RLock()

    def subscribe(self, event_type: EventType, handler: EventHandler) -> None:
        with self._lock:
            self._handlers.setdefault(event_type, []).append(handler)

    def publish(self, event_type: EventType, **payload: Any) -> None:
        event = ScanEvent(type=event_type, payload=payload)
        with self._lock:
            handlers = list(self._handlers.get(event_type, []))
        for handler in handlers:
            handler(event)
