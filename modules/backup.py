from PySide6.QtWidgets import *

from config import APP_NAME

from database.backup_db import create_backup


class BackupWindow(QWidget):

    def __init__(self):

        super().__init__()

        self.setWindowTitle(f"{APP_NAME} - Backup")

        self.resize(500,200)

        layout = QVBoxLayout()

        info = QLabel(
            "Click the button below to create a database backup."
        )

        layout.addWidget(info)

        self.btn_backup = QPushButton("Create Backup")

        layout.addWidget(self.btn_backup)

        self.setLayout(layout)

        self.btn_backup.clicked.connect(self.backup)

    def backup(self):

        file = create_backup()

        QMessageBox.information(

            self,

            APP_NAME,

            f"Backup Created Successfully.\n\n{file}"

        )