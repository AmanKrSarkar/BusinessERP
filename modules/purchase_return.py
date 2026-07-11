from PySide6.QtWidgets import *
from PySide6.QtCore import QDate

from config import APP_NAME
from database.purchase_return_db import save_purchase_return
from database.party_db import get_party


class PurchaseReturnWindow(QWidget):

    def __init__(self):

        super().__init__()

        self.setWindowTitle(f"{APP_NAME} - Purchase Return")

        self.resize(900,650)

        layout = QVBoxLayout()

        form = QGridLayout()

        form.addWidget(QLabel("Supplier"),0,0)
        self.txt_party = QLineEdit()
        form.addWidget(self.txt_party,0,1)

        form.addWidget(QLabel("Purchase Bill No"),0,2)
        self.txt_bill = QLineEdit()
        form.addWidget(self.txt_bill,0,3)

        form.addWidget(QLabel("Return Date"),1,0)
        self.txt_date = QDateEdit()
        self.txt_date.setCalendarPopup(True)
        self.txt_date.setDate(QDate.currentDate())
        form.addWidget(self.txt_date,1,1)

        form.addWidget(QLabel("Total"),1,2)
        self.txt_total = QLineEdit()
        form.addWidget(self.txt_total,1,3)

        layout.addLayout(form)

        btn = QHBoxLayout()

        self.btn_save = QPushButton("Save")
        self.btn_clear = QPushButton("Clear")
        self.btn_close = QPushButton("Close")

        btn.addStretch()
        btn.addWidget(self.btn_save)
        btn.addWidget(self.btn_clear)
        btn.addWidget(self.btn_close)

        layout.addLayout(btn)

        self.setLayout(layout)

        self.btn_save.clicked.connect(self.save)
        self.btn_clear.clicked.connect(self.clear)
        self.btn_close.clicked.connect(self.close)

    def save(self):

        party = get_party(self.txt_party.text().strip())

        if party is None:

            QMessageBox.warning(
                self,
                APP_NAME,
                "Supplier not found."
            )
            return

        try:
            total = float(self.txt_total.text())
        except:
            QMessageBox.warning(
                self,
                APP_NAME,
                "Invalid Total."
            )
            return

        save_purchase_return(

            self.txt_bill.text(),

            party["id"],

            self.txt_date.date().toString("yyyy-MM-dd"),

            total

        )

        QMessageBox.information(

            self,

            APP_NAME,

            "Purchase Return Saved."

        )

        self.clear()

    def clear(self):

        self.txt_party.clear()
        self.txt_bill.clear()
        self.txt_total.clear()

        self.txt_date.setDate(
            QDate.currentDate()
        )