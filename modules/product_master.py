from PySide6.QtWidgets import *
from config import APP_NAME

from database.product_master_db import (
    get_products,
    update_product,
    delete_product
)


class ProductMasterWindow(QWidget):

    def __init__(self):

        super().__init__()

        self.setWindowTitle(f"{APP_NAME} - Product Master")

        self.resize(1200,700)

        layout = QVBoxLayout()

        # Search

        self.txt_search = QLineEdit()
        self.txt_search.setPlaceholderText("Search Product...")
        layout.addWidget(self.txt_search)

        # Table

        self.table = QTableWidget()

        self.table.setColumnCount(5)

        self.table.setHorizontalHeaderLabels([
            "Product",
            "Company",
            "HSN",
            "GST %",
            "ID"
        ])

        self.table.horizontalHeader().setSectionResizeMode(
            QHeaderView.Stretch
        )

        layout.addWidget(self.table)

        # Buttons

        btn = QHBoxLayout()

        self.btn_refresh = QPushButton("Refresh")
        self.btn_edit = QPushButton("Edit")
        self.btn_delete = QPushButton("Delete")
        self.btn_close = QPushButton("Close")

        btn.addStretch()

        btn.addWidget(self.btn_refresh)
        btn.addWidget(self.btn_edit)
        btn.addWidget(self.btn_delete)
        btn.addWidget(self.btn_close)

        layout.addLayout(btn)

        self.setLayout(layout)

        self.btn_refresh.clicked.connect(self.load_data)
        self.btn_edit.clicked.connect(self.edit_product)
        self.btn_delete.clicked.connect(self.delete_selected)
        self.btn_close.clicked.connect(self.close)
        self.txt_search.textChanged.connect(self.search)

        self.load_data()

    def load_data(self):

        self.rows = get_products()

        self.table.setRowCount(len(self.rows))

        for r,row in enumerate(self.rows):

            self.table.setItem(r,0,QTableWidgetItem(row["product_name"]))
            self.table.setItem(r,1,QTableWidgetItem(row["company"]))
            self.table.setItem(r,2,QTableWidgetItem(row["hsn_code"]))
            self.table.setItem(r,3,QTableWidgetItem(str(row["gst_percent"])))
            self.table.setItem(r,4,QTableWidgetItem(str(row["id"])))

    def search(self):

        text = self.txt_search.text().lower()

        for row in range(self.table.rowCount()):

            product = self.table.item(row,0).text().lower()

            self.table.setRowHidden(
                row,
                text not in product
            )

    def edit_product(self):

        row = self.table.currentRow()

        if row < 0:
            return

        pid = int(self.table.item(row,4).text())

        name = self.table.item(row,0).text()
        company = self.table.item(row,1).text()
        hsn = self.table.item(row,2).text()
        gst = self.table.item(row,3).text()

        name,ok = QInputDialog.getText(
            self,
            APP_NAME,
            "Product",
            text=name
        )

        if not ok:
            return

        company,ok = QInputDialog.getText(
            self,
            APP_NAME,
            "Company",
            text=company
        )

        if not ok:
            return

        hsn,ok = QInputDialog.getText(
            self,
            APP_NAME,
            "HSN",
            text=hsn
        )

        if not ok:
            return

        gst,ok = QInputDialog.getDouble(
            self,
            APP_NAME,
            "GST %",
            float(gst),
            0,
            100,
            2
        )

        if not ok:
            return

        update_product(
            pid,
            name,
            company,
            hsn,
            gst
        )

        self.load_data()

    def delete_selected(self):

        row = self.table.currentRow()

        if row < 0:
            return

        reply = QMessageBox.question(
            self,
            APP_NAME,
            "Delete Product?",
            QMessageBox.Yes |
            QMessageBox.No
        )

        if reply != QMessageBox.Yes:
            return

        pid = int(self.table.item(row,4).text())

        delete_product(pid)

        self.load_data()