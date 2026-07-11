from PySide6.QtCore import Qt, QDate
from config import APP_NAME
from database.product_db import get_product
from database.party_db import get_party
from PySide6.QtWidgets import QCompleter
from PySide6.QtCore import QStringListModel
from database.product_db import get_product_names
from PySide6.QtWidgets import QStyledItemDelegate, QLineEdit
from modules.product_delegate import ProductDelegate
from database.product_db import get_product_by_name
from database.party_db import get_party_names
from modules.search_lineedit import SearchLineEdit
from PySide6.QtWidgets import (
    QWidget,
    QLabel,
    QLineEdit,
    QPushButton,
    QVBoxLayout,
    QHBoxLayout,
    QGridLayout,
    QTableWidget,
    QTableWidgetItem,
    QHeaderView,
    QDateEdit,
    QMessageBox
)

from database.sales_db import (
    create_sales_bill,
    save_sales_item,
    fifo_sale,
    get_available_stock,
    get_first_available_batch,
    get_next_invoice_number
)

from database.party_db import get_party
from database.product_db import get_product

class SalesWindow(QWidget):

    def __init__(self):
        super().__init__()

        self.setWindowTitle(f"{APP_NAME} - Sales Bill")
        self.resize(1500, 850)

        self.create_ui()
        

    def create_ui(self):

        self.main_layout = QVBoxLayout()

        # ==========================
        # TITLE
        # ==========================

        title = QLabel("SALES BILL")
        title.setAlignment(Qt.AlignmentFlag.AlignCenter)
        title.setStyleSheet("""
            font-size:24px;
            font-weight:bold;
            padding:10px;
        """)

        self.main_layout.addWidget(title)

        # ==========================
        # HEADER
        # ==========================

        header = QGridLayout()

        lbl_customer = QLabel("Customer")
        self.txt_customer = SearchLineEdit()

        lbl_invoice = QLabel("Invoice No")
        self.txt_invoice = QLineEdit()
        self.txt_invoice.setText(get_next_invoice_number())

        lbl_date = QLabel("Invoice Date")
        self.txt_date = QDateEdit()
        self.txt_date.setCalendarPopup(True)
        self.txt_date.setDate(QDate.currentDate())

        lbl_mobile = QLabel("Mobile")
        self.txt_mobile = QLineEdit()

        lbl_gstin = QLabel("GSTIN")
        self.txt_gstin = QLineEdit()

        lbl_address = QLabel("Address")
        self.txt_address = QLineEdit()

        header.addWidget(lbl_customer,0,0)
        header.addWidget(self.txt_customer,0,1)
        

        header.addWidget(lbl_invoice,0,2)
        header.addWidget(self.txt_invoice,0,3)

        header.addWidget(lbl_date,0,4)
        header.addWidget(self.txt_date,0,5)

        header.addWidget(lbl_mobile,1,0)
        header.addWidget(self.txt_mobile,1,1)

        header.addWidget(lbl_gstin,1,2)
        header.addWidget(self.txt_gstin,1,3)

        header.addWidget(lbl_address,1,4)
        header.addWidget(self.txt_address,1,5)

        self.main_layout.addLayout(header)
        self.load_party_completer()

        # ==========================
        # PRODUCT TABLE
        # ==========================

        self.table = QTableWidget()

        self.table.setColumnCount(16)

        self.table.setHorizontalHeaderLabels([
            "Sr",
            "Product Name",
            "Company",
            "HSN",
            "Batch",
            "Expiry",
            "MRP",
            "Qty",
            "Free Qty",
            "Rate",
            "Disc 1 %",
            "Disc 2 %",
            "GST %",
            "Taxable",
            "Total",
            "Stock"
        ])

        self.table.setRowCount(1)

        for i in range(1):
            item = QTableWidgetItem(str(i+1))
            item.setFlags(item.flags() & ~Qt.ItemFlag.ItemIsEditable)
            self.table.setItem(i,0,item)

        header = self.table.horizontalHeader()
        header.setSectionResizeMode(QHeaderView.Stretch)

        self.main_layout.addWidget(self.table)
        self.setup_product_autocomplete()

        delegate = ProductDelegate(
            self.product_completer,
            self.table
        )

        self.table.setItemDelegateForColumn(
            1,
            delegate
        )

        # ==========================
        # FOOTER
        # ==========================

        footer = QGridLayout()

        lbl_gross = QLabel("Gross Amount")
        self.txt_gross = QLineEdit("0.00")

        lbl_other = QLabel("Other Charges")
        self.txt_other = QLineEdit("0.00")

        lbl_round = QLabel("Round Off")
        self.txt_round = QLineEdit("0.00")
        self.txt_round.setReadOnly(True)

        lbl_net = QLabel("Net Amount")

        self.txt_net = QLineEdit("0.00")
        self.txt_net.setReadOnly(True)

        footer.addWidget(lbl_gross,0,0)
        footer.addWidget(self.txt_gross,0,1)

        footer.addWidget(lbl_other,0,2)
        footer.addWidget(self.txt_other,0,3)

        footer.addWidget(lbl_round,0,4)
        footer.addWidget(self.txt_round,0,5)

        footer.addWidget(lbl_net,1,4)
        footer.addWidget(self.txt_net,1,5)

        self.main_layout.addLayout(footer)

        # ==========================
        # BUTTONS
        # ==========================

        button_layout = QHBoxLayout()

        self.btn_add = QPushButton("Add Row")
        self.btn_delete = QPushButton("Delete Row")
        self.btn_save = QPushButton("Save")
        self.btn_clear = QPushButton("Clear")
        self.btn_print = QPushButton("Print")
        self.btn_close = QPushButton("Close")

        button_layout.addWidget(self.btn_add)
        button_layout.addWidget(self.btn_delete)
        button_layout.addStretch()
        button_layout.addWidget(self.btn_save)
        button_layout.addWidget(self.btn_clear)
        button_layout.addWidget(self.btn_print)
        button_layout.addWidget(self.btn_close)

        self.main_layout.addLayout(button_layout)

        self.setLayout(self.main_layout)

        # ==========================
        # EVENTS
        # ==========================

        self.btn_close.clicked.connect(self.close)
        self.btn_add.clicked.connect(self.add_row)
        self.btn_delete.clicked.connect(self.delete_row)
        self.btn_save.clicked.connect(self.save_sales_bill)
        self.btn_clear.clicked.connect(self.clear_bill)
        self.connect_events()
        self.txt_customer.editingFinished.connect(self.auto_fill_customer)
        self.table.cellChanged.connect(self.auto_fill_product)
    def setup_product_autocomplete(self):

        self.product_model = QStringListModel()

        self.product_model.setStringList(
            get_product_names()
        )

        self.product_completer = QCompleter()

        self.product_completer.setModel(
            self.product_model
        )

        self.product_completer.setCaseSensitivity(
            Qt.CaseInsensitive
        )

        self.product_completer.setFilterMode(
            Qt.MatchContains
        )    

    # =====================================
    # ADD NEW ROW
    # =====================================

    def add_row(self):

        row = self.table.rowCount()

        self.table.insertRow(row)

        item = QTableWidgetItem(str(row + 1))
        item.setFlags(item.flags() & ~Qt.ItemFlag.ItemIsEditable)

        self.table.setItem(row, 0, item)

        for col in range(1, self.table.columnCount()):
            self.table.setItem(row, col, QTableWidgetItem(""))

        self.table.setCurrentCell(row, 1)

    # =====================================
    # DELETE ROW
    # =====================================

    def delete_row(self):

        row = self.table.currentRow()

        if row < 0:
            return

        reply = QMessageBox.question(
            self,
            APP_NAME,
            "Delete selected row?",
            QMessageBox.StandardButton.Yes |
            QMessageBox.StandardButton.No
        )

        if reply != QMessageBox.StandardButton.Yes:
            return

        self.table.removeRow(row)

        for i in range(self.table.rowCount()):

            item = QTableWidgetItem(str(i+1))
            item.setFlags(item.flags() & ~Qt.ItemFlag.ItemIsEditable)
            self.table.setItem(i,0,item)

    # =====================================
    # GET CELL VALUE
    # =====================================

    def get_float(self, row, column):

        item = self.table.item(row, column)

        if item is None:
            return 0.0

        text = item.text().strip()

        if text == "":
            return 0.0

        try:
            return float(text)
        except:
            return 0.0

    # =====================================
    # SET CELL VALUE
    # =====================================

    def set_value(self, row, column, value):

        self.table.blockSignals(True)

        self.table.setItem(
            row,
            column,
            QTableWidgetItem(f"{value:.2f}")
        )

        self.table.blockSignals(False)

    # =====================================
    # CONNECT EVENTS
    # =====================================

    def connect_events(self):

        self.table.cellChanged.connect(self.on_cell_changed)

        self.txt_other.textChanged.connect(
            self.calculate_bill
        )

        self.txt_round.textChanged.connect(
            self.calculate_bill
        )

    def on_cell_changed(self, row, column):

        print("CELL CHANGED:", row, column)
        self.calculate_bill()

        # Only check the last row
        if row != self.table.rowCount() - 1:
            return

        product = self.table.item(row, 1)
        qty = self.table.item(row, 7)
        rate = self.table.item(row, 9)

        if not product or not qty or not rate:
            return

        if (
            product.text().strip() == "" or
            qty.text().strip() == "" or
            rate.text().strip() == ""
        ):
            return

        # Prevent adding multiple rows
        if row == self.table.rowCount() - 1:
            self.add_row()   

    # =====================================
    # CALCULATE COMPLETE BILL
    # =====================================

    def calculate_bill(self):

        gross_amount = 0.0

        self.table.blockSignals(True)
        
        product_total = {}

        for row in range(self.table.rowCount()):

            product_item = self.table.item(row, 1)

            if not product_item:
                continue

            product_name = product_item.text().strip()

            if product_name == "":
                continue
            qty = self.get_float(row, 7)
            free_qty = self.get_float(row, 8)
            sold_qty = qty + free_qty
            product_total.setdefault(product_name, 0)

            product_total[product_name] += sold_qty
            
            
            rate = self.get_float(row, 9)
            disc1 = self.get_float(row, 10)
            disc2 = self.get_float(row, 11)
            gst = self.get_float(row, 12)

            if qty == 0 or rate == 0:

                self.set_value(row, 13, 0)
                self.set_value(row, 14, 0)

                continue

            # -----------------------------
            # Basic Amount
            # -----------------------------

            basic = qty * rate

            # -----------------------------
            # Discount
            # -----------------------------

            total_discount = disc1 + disc2

            discount_amount = basic * total_discount / 100

            taxable = basic - discount_amount

            # -----------------------------
            # GST
            # -----------------------------

            gst_amount = taxable * gst / 100

            # -----------------------------
            # Total
            # -----------------------------

            total = taxable + gst_amount

            self.set_value(row, 13, taxable)
            self.set_value(row, 14, total)

            gross_amount += total
        for row in range(self.table.rowCount()):

            product_item = self.table.item(row, 1)

            if not product_item:
                continue

            product_name = product_item.text().strip()

            stock_item = self.table.item(row, 15)

            if not stock_item:
                continue

            original_stock = stock_item.data(Qt.UserRole)

            if original_stock is None:
                continue

            remaining = original_stock - product_total.get(product_name, 0)

            stock_item.setText(str(remaining))
        self.table.blockSignals(False)

        self.txt_gross.setText(f"{gross_amount:.2f}")

        try:
            other = float(self.txt_other.text())
        except:
            other = 0

        gross = gross_amount + other

        net = round(gross)

        round_off = net - gross

        self.txt_round.setText(f"{round_off:.2f}")

        self.txt_net.setText(f"{net:.2f}")

    # =====================================
    # CLEAR BILL
    # =====================================

    def clear_bill(self):

        self.txt_customer.clear()
        self.txt_invoice.clear()
        self.txt_invoice.setText(get_next_invoice_number())

        self.txt_date.setDate(QDate.currentDate())

        self.txt_mobile.clear()
        self.txt_gstin.clear()
        self.txt_address.clear()

        self.txt_other.setText("0.00")
        self.txt_round.setText("0.00")
        self.txt_gross.setText("0.00")
        self.txt_net.setText("0.00")

        self.table.blockSignals(True)

        self.table.setRowCount(1)
        self.table.clearContents()

        item = QTableWidgetItem("1")
        item.setFlags(item.flags() & ~Qt.ItemFlag.ItemIsEditable)
        self.table.setItem(0,0,item)

        for col in range(1,self.table.columnCount()):
            self.table.setItem(0,col,QTableWidgetItem(""))

        self.table.blockSignals(False)

        self.txt_customer.setFocus()

    # =====================================
    # SAVE BUTTON
    # =====================================

    def save_sales_bill(self):

        customer = self.txt_customer.text().strip()

        if customer == "":
            QMessageBox.warning(self, APP_NAME, "Customer required.")
            return

        invoice = self.txt_invoice.text().strip()

        if invoice == "":
            QMessageBox.warning(self, APP_NAME, "Invoice required.")
            return

        party = get_party(customer)

        if party is None:
            QMessageBox.warning(self, APP_NAME, "Customer not found.")
            return

        bill_id = create_sales_bill(
            invoice,
            self.txt_date.date().toString("yyyy-MM-dd"),
            party["id"],
            float(self.txt_gross.text()),
            float(self.txt_other.text()),
            float(self.txt_round.text()),
            float(self.txt_net.text())
        )

        for row in range(self.table.rowCount()):

            item = self.table.item(row,1)

            if item is None:
                continue

            product_name = item.text().strip()

            if product_name == "":
                continue

            product = get_product_by_name(product_name)

            qty = self.get_float(row,7)

            batches,remaining = fifo_sale(
                product["id"],
                qty
            )

            if remaining > 0:

                QMessageBox.warning(
                    self,
                    APP_NAME,
                    f"Insufficient Stock : {product_name}"
                )

                return

            rate = self.get_float(row,9)
            disc1 = self.get_float(row,10)
            disc2 = self.get_float(row,11)
            gst = self.get_float(row,12)
            taxable = self.get_float(row,13)
            total = self.get_float(row,14)

            for batch_id, sold_qty in batches:

                save_sales_item(
                    bill_id,
                    product["id"],
                    batch_id,
                    sold_qty,
                    rate,
                    disc1,
                    disc2,
                    gst,
                    taxable,
                    total
                )

        QMessageBox.information(
            self,
            APP_NAME,
            "Sales Bill Saved Successfully."
        )

        self.clear_bill()

            # -----------------------------
            # Customer
            # -----------------------------


    def auto_fill_product(self, row, column):

        if column != 1:
            return

        item = self.table.item(row,1)

        if item is None:
            return

        product_name = item.text().strip()

        if product_name == "":
            return

        product = get_product(product_name)

        if product is None:
            return

        product_row = get_product_by_name(product_name)

        if product_row is None:
            return

        batch = get_first_available_batch(product_row["id"])

        self.table.blockSignals(True)

        self.table.setItem(row,2,QTableWidgetItem(product["company"] or ""))
        self.table.setItem(row,3,QTableWidgetItem(product["hsn_code"] or ""))

        if batch:

            self.table.setItem(row,4,QTableWidgetItem(batch["batch_name"]))

            self.table.setItem(
                row,
                5,
                QTableWidgetItem(str(batch["expiry_date"]))
            )

            self.table.setItem(
                row,
                6,
                QTableWidgetItem(str(batch["mrp"]))
            )

            self.table.setItem(
                row,
                9,
                QTableWidgetItem(str(batch["rate"]))
            )

            stock_item = QTableWidgetItem(str(batch["available_stock"]))

            stock_item.setData(
                Qt.UserRole,
                batch["available_stock"]
            )

            self.table.setItem(
                row,
                15,
                stock_item
            )

        self.table.setItem(
            row,
            12,
            QTableWidgetItem(str(product["gst_percent"]))
        )

        self.table.blockSignals(False)
        self.calculate_bill()
        self.on_cell_changed(row, 1)

    def auto_fill_customer(self):

        customer_name = self.txt_customer.text().strip()

        if customer_name == "":
            return

        party = get_party(customer_name)

        if party is None:
            return

        self.txt_mobile.setText(party["mobile"] or "")
        self.txt_gstin.setText(party["gstin"] or "")
        self.txt_address.setText(party["address"] or "")

    def load_party_completer(self):

        self.party_model = QStringListModel(get_party_names())

        self.party_completer = QCompleter(self.party_model, self)

        self.party_completer.setMaxVisibleItems(10)

        self.party_completer.setCaseSensitivity(
            Qt.CaseInsensitive
        )

        self.party_completer.setFilterMode(
            Qt.MatchContains
        )

        self.party_completer.setCompletionMode(
            QCompleter.PopupCompletion
        )

        self.txt_customer.setCompleter(
            self.party_completer
        )