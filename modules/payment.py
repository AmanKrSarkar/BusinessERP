from PySide6.QtWidgets import *
from PySide6.QtCore import QDate

from config import APP_NAME

from database.payment_db import (
    save_payment,
    get_payments
)

from database.party_db import (
    get_party
)


class PaymentWindow(QWidget):

    def __init__(self):

        super().__init__()

        self.setWindowTitle(f"{APP_NAME} - Payment")

        self.resize(1000,700)

        layout = QVBoxLayout()

        # -------------------------
        # Entry Form
        # -------------------------

        form = QGridLayout()

        form.addWidget(QLabel("Party"),0,0)
        self.txt_party = QLineEdit()
        form.addWidget(self.txt_party,0,1)

        form.addWidget(QLabel("Date"),0,2)
        self.txt_date = QDateEdit()
        self.txt_date.setCalendarPopup(True)
        self.txt_date.setDate(QDate.currentDate())
        form.addWidget(self.txt_date,0,3)

        form.addWidget(QLabel("Type"),1,0)

        self.cmb_type = QComboBox()
        self.cmb_type.addItems([
            "Payment In",
            "Payment Out"
        ])

        form.addWidget(self.cmb_type,1,1)

        form.addWidget(QLabel("Amount"),1,2)
        self.txt_amount = QLineEdit()
        form.addWidget(self.txt_amount,1,3)

        form.addWidget(QLabel("Remarks"),2,0)
        self.txt_remarks = QLineEdit()
        form.addWidget(self.txt_remarks,2,1,1,3)

        layout.addLayout(form)

        # -------------------------
        # Buttons
        # -------------------------

        btn_layout = QHBoxLayout()

        self.btn_save = QPushButton("Save")
        self.btn_clear = QPushButton("Clear")
        self.btn_close = QPushButton("Close")

        btn_layout.addStretch()
        btn_layout.addWidget(self.btn_save)
        btn_layout.addWidget(self.btn_clear)
        btn_layout.addWidget(self.btn_close)

        layout.addLayout(btn_layout)

        # -------------------------
        # Table
        # -------------------------

        self.table = QTableWidget()

        self.table.setColumnCount(5)

        self.table.setHorizontalHeaderLabels([
            "Party",
            "Date",
            "Type",
            "Amount",
            "Remarks"
        ])

        self.table.horizontalHeader().setSectionResizeMode(
            QHeaderView.Stretch
        )

        layout.addWidget(self.table)

        self.setLayout(layout)

        self.btn_save.clicked.connect(self.save)
        self.btn_clear.clicked.connect(self.clear)
        self.btn_close.clicked.connect(self.close)

        self.load_data()

    def save(self):

        party = get_party(
            self.txt_party.text().strip()
        )

        if party is None:

            QMessageBox.warning(
                self,
                APP_NAME,
                "Party not found."
            )
            return

        try:
            amount = float(self.txt_amount.text())
        except:
            QMessageBox.warning(
                self,
                APP_NAME,
                "Invalid amount."
            )
            return

        save_payment(
            party["id"],
            self.txt_date.date().toString("yyyy-MM-dd"),
            self.cmb_type.currentText(),
            amount,
            self.txt_remarks.text()
        )

        QMessageBox.information(
            self,
            APP_NAME,
            "Payment Saved Successfully."
        )

        self.clear()
        self.load_data()

    def load_data(self):

        rows = get_payments()

        self.table.setRowCount(len(rows))

        for r,row in enumerate(rows):

            self.table.setItem(r,0,QTableWidgetItem(str(row["party_name"])))
            self.table.setItem(r,1,QTableWidgetItem(str(row["payment_date"])))
            self.table.setItem(r,2,QTableWidgetItem(str(row["payment_type"])))
            self.table.setItem(r,3,QTableWidgetItem(str(row["amount"])))
            self.table.setItem(r,4,QTableWidgetItem(str(row["remarks"])))

    def clear(self):

        self.txt_party.clear()
        self.txt_amount.clear()
        self.txt_remarks.clear()

        self.txt_date.setDate(QDate.currentDate())

        self.cmb_type.setCurrentIndex(0)