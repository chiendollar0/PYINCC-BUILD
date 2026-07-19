"""Application entry point for PYINCC."""

from __future__ import annotations

import sys

from src.bootstrap import run


def main() -> int:
    """Start the PYINCC application."""
    return run(sys.argv)


if __name__ == "__main__":
    raise SystemExit(main())
