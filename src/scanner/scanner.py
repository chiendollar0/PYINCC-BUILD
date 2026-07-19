"""Scanner registry."""

from __future__ import annotations

from src.scanner.base import BaseScanner


class ScannerRegistry:
    def __init__(self) -> None:
        self._scanners: dict[str, BaseScanner] = {}

    def register(self, scanner: BaseScanner) -> None:
        self._scanners[scanner.name] = scanner

    def get(self, name: str) -> BaseScanner:
        return self._scanners[name]

    def all(self) -> tuple[BaseScanner, ...]:
        return tuple(self._scanners.values())
