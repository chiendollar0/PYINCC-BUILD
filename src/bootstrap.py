"""Bootstrap sequence for the PYINCC PySide6 desktop application."""

from __future__ import annotations

import logging
import sys
import traceback
from dataclasses import dataclass
from pathlib import Path

from PySide6.QtCore import QTimer, Qt
from PySide6.QtGui import QIcon, QPixmap
from PySide6.QtWidgets import QApplication, QMessageBox, QSplashScreen

from src.core.config import AppConfig, load_config
from src.core.logging_config import configure_logging
from src.core.paths import APP_AUTHOR, APP_NAME, ensure_app_directories, resource_path
from src.gui.main_window import MainWindow

LOGGER = logging.getLogger(__name__)


@dataclass(slots=True)
class BootstrapContext:
    """Objects created during application startup."""

    app: QApplication
    config: AppConfig
    directories: dict[str, Path]
    log_path: Path
    main_window: MainWindow


def install_exception_hook() -> None:
    """Install a global exception hook that logs and displays fatal errors."""

    def handle_exception(exc_type: type[BaseException], exc: BaseException, tb: object) -> None:
        logging.critical("Unhandled exception", exc_info=(exc_type, exc, tb))
        message = "".join(traceback.format_exception_only(exc_type, exc)).strip()
        if QApplication.instance() is not None:
            QMessageBox.critical(None, "PYINCC Error", f"An unexpected error occurred:\n\n{message}")
        else:
            sys.__excepthook__(exc_type, exc, tb)

    sys.excepthook = handle_exception


def create_application(argv: list[str] | None = None) -> QApplication:
    """Create and configure the Qt application object."""
    app = QApplication(argv or sys.argv)
    app.setApplicationName(APP_NAME)
    app.setApplicationDisplayName("PYINCC")
    app.setOrganizationName(APP_AUTHOR)
    app.setDesktopFileName("pyincc")

    icon_path = resource_path("icon.ico")
    if icon_path.exists():
        app.setWindowIcon(QIcon(str(icon_path)))
    return app


def create_splash() -> QSplashScreen | None:
    """Create the splash screen when bundled artwork is available."""
    splash_path = resource_path("splash.png")
    if not splash_path.exists():
        return None

    pixmap = QPixmap(str(splash_path))
    if pixmap.isNull():
        return None

    splash = QSplashScreen(pixmap)
    splash.showMessage("Starting PYINCC...", Qt.AlignmentFlag.AlignBottom | Qt.AlignmentFlag.AlignCenter)
    splash.show()
    QApplication.processEvents()
    return splash


def bootstrap(argv: list[str] | None = None) -> BootstrapContext:
    """Run the startup sequence and return the initialized application context."""
    directories = ensure_app_directories()
    config = load_config(directories["config"])
    log_path = configure_logging(directories["logs"], config.log_level)
    install_exception_hook()

    LOGGER.info("Starting PYINCC bootstrap")
    LOGGER.info("Data directory: %s", directories["data"])
    LOGGER.info("Log file: %s", log_path)

    app = create_application(argv)
    splash = create_splash() if config.show_splash else None
    main_window = MainWindow(config)

    icon_path = resource_path("icon.ico")
    if icon_path.exists():
        main_window.setWindowIcon(QIcon(str(icon_path)))

    if config.start_minimized:
        main_window.showMinimized()
    else:
        main_window.show()

    if splash is not None:
        QTimer.singleShot(600, splash.close)

    return BootstrapContext(
        app=app,
        config=config,
        directories=directories,
        log_path=log_path,
        main_window=main_window,
    )


def run(argv: list[str] | None = None) -> int:
    """Bootstrap and execute the Qt event loop."""
    context = bootstrap(argv)
    return context.app.exec()
