import sys

from PySide6.QtWidgets import QApplication

from database.database import initialize_database
from modules.dashboard import Dashboard


def main():
    initialize_database()

    app = QApplication(sys.argv)

    window = Dashboard()
    window.show()

    sys.exit(app.exec())


if __name__ == "__main__":
    main()