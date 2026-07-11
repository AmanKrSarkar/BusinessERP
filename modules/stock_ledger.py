from PySide6.QtWidgets import *

from config import APP_NAME
from database.stock_ledger_db import get_stock_ledger


class StockLedgerWindow(QWidget):

    def __init__(self):

        super().__init__()

        self.setWindowTitle(f"{APP_NAME} - Stock Ledger")

        self.resize(1200,700)

        layout=QVBoxLayout()

        self.search=QLineEdit()
        self.search.setPlaceholderText("Search Product...")

        layout.addWidget(self.search)

        self.table=QTableWidget()

        self.table.setColumnCount(6)

        self.table.setHorizontalHeaderLabels([

            "Product",
            "Batch",
            "Expiry",
            "MRP",
            "Rate",
            "Stock"

        ])

        self.table.horizontalHeader().setSectionResizeMode(
            QHeaderView.Stretch
        )

        layout.addWidget(self.table)

        self.setLayout(layout)

        self.search.textChanged.connect(
            self.filter_rows
        )

        self.load()

    def load(self):

        rows=get_stock_ledger()

        self.table.setRowCount(len(rows))

        for r,row in enumerate(rows):

            self.table.setItem(r,0,QTableWidgetItem(row["product_name"]))
            self.table.setItem(r,1,QTableWidgetItem(row["batch_name"]))
            self.table.setItem(r,2,QTableWidgetItem(row["expiry_date"]))
            self.table.setItem(r,3,QTableWidgetItem(str(row["mrp"])))
            self.table.setItem(r,4,QTableWidgetItem(str(row["rate"])))
            self.table.setItem(r,5,QTableWidgetItem(str(row["available_stock"])))

    def filter_rows(self):

        text=self.search.text().lower()

        for row in range(self.table.rowCount()):

            item=self.table.item(row,0)

            if item:

                self.table.setRowHidden(
                    row,
                    text not in item.text().lower()
                )