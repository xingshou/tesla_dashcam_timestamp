# src/main.py
import sys

from PySide6.QtWidgets import QApplication

from ui.main_window import MainWindow


def main():
    """Initialize and run the TeslaDashcam application."""
    app = QApplication(sys.argv)
    window = MainWindow()
    window.show()
    sys.exit(app.exec())


if __name__ == "__main__":
    main()
