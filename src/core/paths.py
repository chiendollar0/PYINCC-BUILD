"""Filesystem paths used by the PYINCC desktop application."""

from __future__ import annotations

import os
from pathlib import Path

APP_NAME = "PYINCC"
APP_AUTHOR = "PYINCC"


def project_root() -> Path:
    """Return the repository/application root directory."""
    return Path(__file__).resolve().parents[2]


def resource_path(*parts: str) -> Path:
    """Return a path inside the bundled assets directory."""
    return project_root().joinpath("assets", *parts)


def user_data_dir() -> Path:
    """Return the per-user data directory for PYINCC."""
    if os.name == "nt":
        base = Path(os.environ.get("LOCALAPPDATA", Path.home() / "AppData" / "Local"))
        return base / APP_NAME

    base = Path(os.environ.get("XDG_DATA_HOME", Path.home() / ".local" / "share"))
    return base / APP_NAME.lower()


def ensure_app_directories() -> dict[str, Path]:
    """Create and return the local application directory layout."""
    root = user_data_dir()
    directories = {
        "data": root,
        "config": root / "config",
        "logs": root / "logs",
        "reports": root / "reports",
        "cache": root / "cache",
    }
    for path in directories.values():
        path.mkdir(parents=True, exist_ok=True)
    return directories
