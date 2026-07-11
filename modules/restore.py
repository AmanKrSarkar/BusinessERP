from PySide6.QtWidgets import *

from config import APP_NAME

from database.restore_db import restore_backup


class RestoreWindow(QWidget):

    def __init__(self):

        super().__init__()

        self.setWindowTitle(f"{APP_NAME} - Restore")

        self.resize(500,200)

        layout = QVBoxLayout()

        label = QLabel(
            "Restore Database from Backup"
        )

        layout.addWidget(label)

        self.btn_restore = QPushButton(
            "Restore Backup"
        )

        layout.addWidget(self.btn_restore)

        self.setLayout(layout)

        self.btn_restore.clicked.connect(
            self.restore
        )

    def restore(self):

        reply = QMessageBox.question(

            self,

            APP_NAME,

            "Restore Backup?\n\nCurrent database will be overwritten.",

            QMessageBox.Yes |
            QMessageBox.No

        )

        if reply != QMessageBox.Yes:
            return

        if restore_backup():

            QMessageBox.information(

                self,

                APP_NAME,

                "Database Restored Successfully."

            )

        else:

            QMessageBox.warning(

                self,

                APP_NAME,

                "Backup file not found."

            )