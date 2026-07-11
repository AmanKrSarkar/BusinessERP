from PySide6.QtWidgets import *
from config import APP_NAME

from database.stock_adjustment_db import save_adjustment
from database.product_db import get_product_by_name
from database.sales_db import get_fifo_batches


class StockAdjustmentWindow(QWidget):

    def __init__(self):

        super().__init__()

        self.setWindowTitle(f"{APP_NAME} - Stock Adjustment")

        self.resize(900,600)

        layout = QVBoxLayout()

        form = QGridLayout()

        form.addWidget(QLabel("Product"),0,0)

        self.txt_product = QLineEdit()
        form.addWidget(self.txt_product,0,1)

        form.addWidget(QLabel("Quantity (+/-)"),0,2)

        self.txt_qty = QLineEdit()
        form.addWidget(self.txt_qty,0,3)

        form.addWidget(QLabel("Reason"),1,0)

        self.txt_reason = QLineEdit()
        form.addWidget(self.txt_reason,1,1,1,3)

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

        product = get_product_by_name(
            self.txt_product.text().strip()
        )

        if product is None:

            QMessageBox.warning(
                self,
                APP_NAME,
                "Product not found."
            )

            return

        batches = get_fifo_batches(product["id"])

        if len(batches)==0:

            QMessageBox.warning(
                self,
                APP_NAME,
                "No Batch Found."
            )

            return

        try:

            qty=float(self.txt_qty.text())

        except:

            QMessageBox.warning(
                self,
                APP_NAME,
                "Invalid Quantity."
            )

            return

        save_adjustment(

            product["id"],

            batches[0]["id"],

            qty,

            self.txt_reason.text()

        )

        QMessageBox.information(

            self,

            APP_NAME,

            "Stock Updated."

        )

        self.clear()

    def clear(self):

        self.txt_product.clear()
        self.txt_qty.clear()
        self.txt_reason.clear()