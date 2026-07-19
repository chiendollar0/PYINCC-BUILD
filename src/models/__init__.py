"""Data models for scanner sessions, records, tasks, and plugins."""

from __future__ import annotations

from dataclasses import dataclass, field
from datetime import datetime, timezone
from enum import Enum
from typing import Any
from uuid import uuid4


class TaskStatus(str, Enum):
    """Execution status for a scan task."""

    PENDING = "pending"
    RUNNING = "running"
    COMPLETED = "completed"
    WARNING = "warning"
    FAILED = "failed"
    CANCELLED = "cancelled"


@dataclass(slots=True)
class EvidenceRecord:
    """A normalized piece of evidence found during a scan."""

    source: str
    kind: str
    value: str
    metadata: dict[str, Any] = field(default_factory=dict)
    record_id: str = field(default_factory=lambda: str(uuid4()))


@dataclass(slots=True)
class SoftwareRecord:
    """A software-oriented output record built from one or more evidence items."""

    name: str
    version: str | None = None
    publisher: str | None = None
    source: str | None = None
    evidence: list[EvidenceRecord] = field(default_factory=list)
    metadata: dict[str, Any] = field(default_factory=dict)
    record_id: str = field(default_factory=lambda: str(uuid4()))


@dataclass(slots=True)
class ScanTask:
    """A scanner task scheduled for execution."""

    scanner_name: str
    payload: dict[str, Any] = field(default_factory=dict)
    task_id: str = field(default_factory=lambda: str(uuid4()))
    status: TaskStatus = TaskStatus.PENDING
    warning: str | None = None


@dataclass(slots=True)
class PluginResult:
    """Result returned by a plugin provider."""

    plugin_name: str
    software: list[SoftwareRecord] = field(default_factory=list)
    evidence: list[EvidenceRecord] = field(default_factory=list)
    metadata: dict[str, Any] = field(default_factory=dict)
    warnings: list[str] = field(default_factory=list)


@dataclass(slots=True)
class ScanResult:
    """Result returned by a scanner task."""

    task_id: str
    scanner_name: str
    software: list[SoftwareRecord] = field(default_factory=list)
    evidence: list[EvidenceRecord] = field(default_factory=list)
    plugin_results: list[PluginResult] = field(default_factory=list)
    metadata: dict[str, Any] = field(default_factory=dict)
    warnings: list[str] = field(default_factory=list)


@dataclass(slots=True)
class ScanContext:
    """Shared context passed through scanners and plugins."""

    session_id: str = field(default_factory=lambda: str(uuid4()))
    config: dict[str, Any] = field(default_factory=dict)
    started_at: datetime = field(default_factory=lambda: datetime.now(timezone.utc))
    metadata: dict[str, Any] = field(default_factory=dict)
    cancelled: bool = False


@dataclass(slots=True)
class ScanReport:
    """Final report model returned to a GUI or another caller."""

    session_id: str
    software: list[SoftwareRecord] = field(default_factory=list)
    evidence: list[EvidenceRecord] = field(default_factory=list)
    warnings: list[str] = field(default_factory=list)
    metadata: dict[str, Any] = field(default_factory=dict)
    started_at: datetime | None = None
    finished_at: datetime | None = None


__all__ = [
    "EvidenceRecord",
    "PluginResult",
    "ScanContext",
    "ScanReport",
    "ScanResult",
    "ScanTask",
    "SoftwareRecord",
    "TaskStatus",
]
