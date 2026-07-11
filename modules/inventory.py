from PySide6.QtWidgets import *
from config import APP_NAME
from database.inventory_db import get_current_stock


class InventoryWindow(QWidget):

    def __init__(self):
        super().__init__()

        self.setWindowTitle(f"{APP_NAME} - Inventory")

        self.resize(1200,700)

        layout = QVBoxLayout()

        self.table = QTableWidget()

        self.table.setColumnCount(7)

        self.table.setHorizontalHeaderLabels([
            "Product",
            "Company",
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

        self.load_stock()

    def load_stock(self):

        rows = get_current_stock()

        self.table.setRowCount(len(rows))

        for r,row in enumerate(rows):

            self.table.setItem(r,0,QTableWidgetItem(str(row["product_name"])))
            self.table.setItem(r,1,QTableWidgetItem(str(row["company"])))
            self.table.setItem(r,2,QTableWidgetItem(str(row["batch_name"])))
            self.table.setItem(r,3,QTableWidgetItem(str(row["expiry_date"])))
            self.table.setItem(r,4,QTableWidgetItem(str(row["mrp"])))
            self.table.setItem(r,5,QTableWidgetItem(str(row["rate"])))
            self.table.setItem(r,6,QTableWidgetItem(str(row["available_stock"])))