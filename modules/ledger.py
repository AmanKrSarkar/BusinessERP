from PySide6.QtWidgets import *

from config import APP_NAME

from database.ledger_db import get_party_ledger


class LedgerWindow(QWidget):

    def __init__(self):

        super().__init__()

        self.setWindowTitle(f"{APP_NAME} - Party Ledger")

        self.resize(1000,700)

        layout = QVBoxLayout()

        self.table = QTableWidget()

        self.table.setColumnCount(4)

        self.table.setHorizontalHeaderLabels([
            "Party",
            "Invoice",
            "Date",
            "Amount"
        ])

        self.table.horizontalHeader().setSectionResizeMode(
            QHeaderView.Stretch
        )

        layout.addWidget(self.table)

        self.setLayout(layout)

        self.load_data()


    def load_data(self):

        rows = get_party_ledger()

        self.table.setRowCount(len(rows))

        for r,row in enumerate(rows):

            self.table.setItem(r,0,QTableWidgetItem(str(row["party_name"])))
            self.table.setItem(r,1,QTableWidgetItem(str(row["invoice_number"])))
            self.table.setItem(r,2,QTableWidgetItem(str(row["invoice_date"])))
            self.table.setItem(r,3,QTableWidgetItem(str(row["net_amount"])))