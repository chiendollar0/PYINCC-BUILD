"""Main window shell for the Phase 1 PYINCC desktop application."""

from __future__ import annotations

from PySide6.QtCore import Qt
from PySide6.QtGui import QAction
from PySide6.QtWidgets import QLabel, QMainWindow, QStatusBar, QVBoxLayout, QWidget

from src.core.config import AppConfig


class MainWindow(QMainWindow):
    """Initial application window prepared for future UI modules."""

    def __init__(self, config: AppConfig) -> None:
        super().__init__()
        self._config = config
        self.setWindowTitle("PYINCC - Software Evidence Scanner")
        self.resize(config.window_width, config.window_height)
        self._build_menu()
        self._build_central_widget()
        self.setStatusBar(QStatusBar(self))
        self.statusBar().showMessage("Ready")

    def _build_menu(self) -> None:
        file_menu = self.menuBar().addMenu("File")
        exit_action = QAction("Exit", self)
        exit_action.triggered.connect(self.close)
        file_menu.addAction(exit_action)

        help_menu = self.menuBar().addMenu("Help")
        about_action = QAction("About PYINCC", self)
        about_action.setEnabled(False)
        help_menu.addAction(about_action)

    def _build_central_widget(self) -> None:
        container = QWidget(self)
        layout = QVBoxLayout(container)
        layout.setAlignment(Qt.AlignmentFlag.AlignCenter)

        title = QLabel("PYINCC")
        title.setObjectName("AppTitle")
        title.setAlignment(Qt.AlignmentFlag.AlignCenter)

        subtitle = QLabel("Phase 1 Bootstrap is ready. UI modules will be added next.")
        subtitle.setAlignment(Qt.AlignmentFlag.AlignCenter)

        layout.addWidget(title)
        layout.addWidget(subtitle)
        self.setCentralWidget(container)
