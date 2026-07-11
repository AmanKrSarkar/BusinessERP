from PySide6.QtCore import Qt, QDate
from config import APP_NAME
from database.product_db import get_product
from database.party_db import get_party
from PySide6.QtWidgets import QCompleter
from PySide6.QtCore import QStringListModel
from database.product_db import get_product_names
from PySide6.QtWidgets import QStyledItemDelegate, QLineEdit
from modules.product_delegate import ProductDelegate
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

from database.purchase_db import (
    get_or_create_party,
    get_or_create_product,
    get_or_create_batch,
    create_purchase_bill,
    save_purchase_item,
    invoice_exists
)

class PurchaseWindow(QWidget):

    def __init__(self):
        super().__init__()

        self.setWindowTitle(f"{APP_NAME} - Purchase Bill")
        self.resize(1500, 850)

        self.create_ui()

    def create_ui(self):

        self.main_layout = QVBoxLayout()

        # ==========================
        # TITLE
        # ==========================

        title = QLabel("PURCHASE BILL")
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

        lbl_supplier = QLabel("Supplier")
        self.txt_supplier = QLineEdit()

        lbl_invoice = QLabel("Invoice No")
        self.txt_invoice = QLineEdit()

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

        header.addWidget(lbl_supplier,0,0)
        header.addWidget(self.txt_supplier,0,1)

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

        # ==========================
        # PRODUCT TABLE
        # ==========================

        self.table = QTableWidget()

        self.table.setColumnCount(15)

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
            "Total"
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
        self.btn_save.clicked.connect(self.save_bill)
        self.btn_clear.clicked.connect(self.clear_bill)
        self.connect_events()
        self.txt_supplier.editingFinished.connect(self.auto_fill_supplier)
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

        for row in range(self.table.rowCount()):

            qty = self.get_float(row, 7)
            rate = self.get_float(row, 9)
            disc1 = self.get_float(row, 10)
            disc2 = self.get_float(row, 11)
            gst = self.get_float(row, 12)

            if qty == 0 or rate == 0:

                self.set_value(row, 13, 0)
                self.set_value(row, 14, 0)

                continue

            # -----------------------------
            # Taxable
            # -----------------------------

            taxable = qty * rate

            total_discount = disc1 + disc2

            taxable -= taxable * total_discount / 100

            # -----------------------------
            # GST
            # -----------------------------

            gst_amount = taxable * gst / 100

            total = taxable + gst_amount

            self.set_value(row, 13, taxable)
            self.set_value(row, 14, total)

            gross_amount += total

        self.table.blockSignals(False)

        self.txt_gross.setText(f"{gross_amount:.2f}")

        try:
            other = float(self.txt_other.text())
        except:
            other = 0

        try:
            round_off = float(self.txt_round.text())
        except:
            round_off = 0

        net = gross_amount + other + round_off

        self.txt_net.setText(f"{net:.2f}")

    # =====================================
    # CLEAR BILL
    # =====================================

    def clear_bill(self):

        self.txt_supplier.clear()
        self.txt_invoice.clear()

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

        self.txt_supplier.setFocus()

    # =====================================
    # SAVE BUTTON
    # =====================================

    def save_bill(self):

        try:
        
            if self.txt_supplier.text().strip() == "":
                QMessageBox.warning(self, APP_NAME, "Please select a Supplier.")
                self.txt_supplier.setFocus()
                return

            if self.txt_invoice.text().strip() == "":
                QMessageBox.warning(self, APP_NAME, "Please enter Invoice Number.")
                self.txt_invoice.setFocus()
                return

            product_found = False

            for row in range(self.table.rowCount()):

                item = self.table.item(row,1)

                if item and item.text().strip() != "":
                    product_found = True
                    break

            if not product_found:
                QMessageBox.warning(self, APP_NAME, "Please add at least one Product.")
                return

            invoice = self.txt_invoice.text().strip()

            if invoice == "":
                QMessageBox.warning(
                    self,
                    APP_NAME,
                    "Invoice Number is required."
                )
                return

            if invoice_exists(invoice):
                QMessageBox.warning(
                    self,
                    APP_NAME,
                    f"Invoice No '{invoice}' already exists."
                )
                return

            # -----------------------------
            # Supplier
            # -----------------------------

            party_id = get_or_create_party(
                self.txt_supplier.text().strip(),
                self.txt_mobile.text().strip(),
                self.txt_gstin.text().strip(),
                self.txt_address.text().strip()
            )

            # -----------------------------
            # Purchase Bill
            # -----------------------------

            purchase_bill_id = create_purchase_bill(
                invoice,
                self.txt_date.date().toString("yyyy-MM-dd"),
                party_id,
                float(self.txt_gross.text() or 0),
                float(self.txt_other.text() or 0),
                float(self.txt_round.text() or 0),
                float(self.txt_net.text() or 0)
            )

            # -----------------------------
            # Products
            # -----------------------------

            for row in range(self.table.rowCount()):

                product = self.table.item(row,1)

                if product is None:
                    continue

                product_name = product.text().strip()

                if product_name == "":
                    continue

                company = self.table.item(row,2)
                hsn = self.table.item(row,3)
                batch = self.table.item(row,4)
                expiry = self.table.item(row,5)
                mrp = self.table.item(row,6)

                company = company.text() if company else ""
                hsn = hsn.text() if hsn else ""
                batch = batch.text() if batch else ""
                expiry = expiry.text() if expiry else ""

                mrp = self.get_float(row,6)
                qty = self.get_float(row,7)
                free = self.get_float(row,8)
                rate = self.get_float(row,9)
                disc1 = self.get_float(row,10)
                disc2 = self.get_float(row,11)
                gst = self.get_float(row,12)
                taxable = self.get_float(row,13)
                total = self.get_float(row,14)

                product_id = get_or_create_product(
                    product_name,
                    company,
                    hsn,
                    gst
                )

                batch_id = get_or_create_batch(
                    product_id,
                    batch,
                    expiry,
                    mrp,
                    rate,
                    qty,
                    free,
                    purchase_bill_id
                )

                save_purchase_item(
                    purchase_bill_id,
                    product_id,
                    batch_id,
                    qty,
                    free,
                    rate,
                    disc1,
                    disc2,
                    gst,
                    taxable,
                    total
                )

            reply = QMessageBox.question(
                self,
                APP_NAME,
                f"""Purchase Bill Saved Successfully.

            Invoice : {invoice}
            Items : {self.table.rowCount()-1}

            Do you want to create a New Bill?""",
                QMessageBox.StandardButton.Yes |
                QMessageBox.StandardButton.No
            )

            if reply == QMessageBox.StandardButton.Yes:
                self.clear_bill()
                self.txt_supplier.setFocus()

        except Exception as e:
            import traceback

            print(traceback.format_exc())

            QMessageBox.critical(
                self,
                "Error",
                str(e)
            )

    def auto_fill_product(self, row, column):

        if column != 1:
            return

        item = self.table.item(row, 1)

        if item is None:
            return

        product_name = item.text().strip()

        if product_name == "":
            return

        product = get_product(product_name)

        if product is None:
            return

        self.table.blockSignals(True)

        self.table.setItem(row, 2, QTableWidgetItem(product["company"] or ""))
        self.table.setItem(row, 3, QTableWidgetItem(product["hsn_code"] or ""))
        self.table.setItem(row, 12, QTableWidgetItem(str(product["gst_percent"] or 0)))

        self.table.blockSignals(False)

    def auto_fill_supplier(self):

        supplier_name = self.txt_supplier.text().strip()

        if supplier_name == "":
            return

        party = get_party(supplier_name)

        if party is None:
            return

        self.txt_mobile.setText(party["mobile"] or "")
        self.txt_gstin.setText(party["gstin"] or "")
        self.txt_address.setText(party["address"] or "")