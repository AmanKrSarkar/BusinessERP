from PySide6.QtWidgets import *
from config import APP_NAME
from database.sales_register_db import get_sales_register


class SalesRegisterWindow(QWidget):

    def __init__(self):

        super().__init__()

        self.setWindowTitle(f"{APP_NAME} - Sales Register")

        self.resize(1000,700)

        layout=QVBoxLayout()

        self.table=QTableWidget()

        self.table.setColumnCount(5)

        self.table.setHorizontalHeaderLabels([
            "Invoice",
            "Date",
            "Customer",
            "Net Amount",
            "ID"
        ])

        self.table.horizontalHeader().setSectionResizeMode(
            QHeaderView.Stretch
        )

        layout.addWidget(self.table)

        self.setLayout(layout)

        self.load_data()

    def load_data(self):

        rows=get_sales_register()

        self.table.setRowCount(len(rows))

        for r,row in enumerate(rows):

            self.table.setItem(r,0,QTableWidgetItem(str(row["invoice_number"])))
            self.table.setItem(r,1,QTableWidgetItem(str(row["invoice_date"])))
            self.table.setItem(r,2,QTableWidgetItem(str(row["party_name"])))
            self.table.setItem(r,3,QTableWidgetItem(str(row["net_amount"])))
            self.table.setItem(r,4,QTableWidgetItem(str(row["id"])))