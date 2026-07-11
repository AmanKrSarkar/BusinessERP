from PySide6.QtWidgets import *
from PySide6.QtCore import Signal
from config import APP_NAME

from database.company_db import (
    save_company,
    get_company
)


class CompanyProfileWindow(QWidget):

    company_updated = Signal()

    def __init__(self, parent=None):

        super().__init__(parent)

        self.setWindowTitle(f"{APP_NAME} - Company Profile")

        self.resize(700,500)

        layout = QVBoxLayout()

        form = QGridLayout()

        form.addWidget(QLabel("Company Name"),0,0)
        self.txt_name=QLineEdit()
        form.addWidget(self.txt_name,0,1)

        form.addWidget(QLabel("Address"),1,0)
        self.txt_address=QLineEdit()
        form.addWidget(self.txt_address,1,1)

        form.addWidget(QLabel("Mobile"),2,0)
        self.txt_mobile=QLineEdit()
        form.addWidget(self.txt_mobile,2,1)

        form.addWidget(QLabel("Email"),3,0)
        self.txt_email=QLineEdit()
        form.addWidget(self.txt_email,3,1)

        form.addWidget(QLabel("GSTIN"),4,0)
        self.txt_gstin=QLineEdit()
        form.addWidget(self.txt_gstin,4,1)

        layout.addLayout(form)

        btn=QHBoxLayout()

        self.btn_save=QPushButton("Save")
        self.btn_close=QPushButton("Close")

        btn.addStretch()
        btn.addWidget(self.btn_save)
        btn.addWidget(self.btn_close)

        layout.addLayout(btn)

        self.setLayout(layout)

        self.btn_save.clicked.connect(self.save)
        self.btn_close.clicked.connect(self.close)

        self.load_data()

    def load_data(self):

        row=get_company()

        if row is None:
            return

        self.txt_name.setText(row["company_name"] or "")
        self.txt_address.setText(row["address"] or "")
        self.txt_mobile.setText(row["mobile"] or "")
        self.txt_email.setText(row["email"] or "")
        self.txt_gstin.setText(row["gstin"] or "")

    def save(self):

        save_company(

            self.txt_name.text(),

            self.txt_address.text(),

            self.txt_mobile.text(),

            self.txt_email.text(),

            self.txt_gstin.text()

        )

        QMessageBox.information(
            self,
            APP_NAME,
            "Company Profile Saved."
        )
        self.company_updated.emit()
        