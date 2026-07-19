"""Application configuration loading and persistence."""

from __future__ import annotations

import json
from dataclasses import asdict, dataclass
from pathlib import Path
from typing import Any


@dataclass(slots=True)
class AppConfig:
    """User-configurable desktop settings."""

    theme: str = "system"
    language: str = "vi"
    start_minimized: bool = False
    show_splash: bool = True
    log_level: str = "INFO"
    window_width: int = 1180
    window_height: int = 760

    @classmethod
    def from_mapping(cls, values: dict[str, Any]) -> "AppConfig":
        """Create a config object while ignoring unknown keys."""
        allowed = cls.__dataclass_fields__.keys()
        return cls(**{key: values[key] for key in allowed if key in values})


def load_config(config_dir: Path) -> AppConfig:
    """Load configuration from disk, creating defaults when missing."""
    config_path = config_dir / "settings.json"
    if not config_path.exists():
        config = AppConfig()
        save_config(config, config_dir)
        return config

    with config_path.open("r", encoding="utf-8") as stream:
        data = json.load(stream)
    if not isinstance(data, dict):
        raise ValueError(f"Invalid configuration payload in {config_path}")
    return AppConfig.from_mapping(data)


def save_config(config: AppConfig, config_dir: Path) -> None:
    """Persist configuration to disk."""
    config_dir.mkdir(parents=True, exist_ok=True)
    config_path = config_dir / "settings.json"
    with config_path.open("w", encoding="utf-8") as stream:
        json.dump(asdict(config), stream, indent=2, ensure_ascii=False)
        stream.write("\n")
