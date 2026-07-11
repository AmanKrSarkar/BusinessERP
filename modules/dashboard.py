from PySide6.QtCore import Qt
from config import APP_NAME
from modules.inventory import InventoryWindow
from modules.sales import SalesWindow
from modules.sales_register import SalesRegisterWindow
from modules.ledger import LedgerWindow
from modules.payment import PaymentWindow
from modules.purchase_return import PurchaseReturnWindow
from modules.sales_return import SalesReturnWindow
from modules.stock_adjustment import StockAdjustmentWindow
from modules.purchase_register import PurchaseRegisterWindow
from modules.payment_register import PaymentRegisterWindow
from modules.product_master import ProductMasterWindow
from modules.party_master import PartyMasterWindow
from modules.company_profile import CompanyProfileWindow
from modules.backup import BackupWindow
from modules.restore import RestoreWindow
from modules.stock_ledger import StockLedgerWindow
from database.company_db import get_company
from PySide6.QtWidgets import (
    QWidget,
    QLabel,
    QPushButton,
    QVBoxLayout,
    QGridLayout,
)

from modules.purchase import PurchaseWindow


class Dashboard(QWidget):
    def __init__(self):
        super().__init__()

        self.purchase_window = None

        self.setWindowTitle(APP_NAME)
        self.resize(1200,800)

        main_layout = QVBoxLayout()

        company = get_company()

        if company and company["company_name"]:
            dashboard_title = company["company_name"]
        else:
            dashboard_title = "Company Name"

        self.title = QLabel(dashboard_title)
        self.title.setAlignment(Qt.AlignmentFlag.AlignCenter)
        self.title.setStyleSheet("""
        QLabel{
            font-size:30px;
            font-weight:bold;
            padding:15px;
        }
        """)

        main_layout.addWidget(self.title)


        def add_section(title_text, button_names):

            title = QLabel(title_text)
            title.setStyleSheet("""
                QLabel{
                    font-size:18px;
                    font-weight:bold;
                    padding-top:10px;
                    padding-bottom:5px;
                }
            """)

            main_layout.addWidget(title)

            grid = QGridLayout()

            row = 0
            col = 0

            for text in button_names:

                button = QPushButton(text)

                button.setFixedHeight(55)

                button.setStyleSheet("""
                    QPushButton{
                        font-size:15px;
                    }
                """)

                if text == "Purchase Bill":
                    button.clicked.connect(self.open_purchase_window)

                elif text == "Sales Bill":
                    button.clicked.connect(self.open_sales_window)

                elif text == "Payment":
                    button.clicked.connect(self.open_payment)

                elif text == "Purchase Return":
                    button.clicked.connect(self.open_purchase_return)

                elif text == "Sales Return":
                    button.clicked.connect(self.open_sales_return)

                elif text == "Inventory":
                    button.clicked.connect(self.open_inventory)

                elif text == "Stock Adjustment":
                    button.clicked.connect(self.open_stock_adjustment)

                elif text == "Purchase Register":
                    button.clicked.connect(self.open_purchase_register)

                elif text == "Sales Register":
                    button.clicked.connect(self.open_sales_register)

                elif text == "Payment Register":
                    button.clicked.connect(self.open_payment_register)

                elif text == "Stock Ledger":
                    button.clicked.connect(self.open_stock_ledger)

                elif text == "Party Ledger":
                    button.clicked.connect(self.open_party_ledger)

                elif text == "Product Master":
                    button.clicked.connect(self.open_product_master)

                elif text == "Party Master":
                    button.clicked.connect(self.open_party_master)

                elif text == "Company Profile":
                    button.clicked.connect(self.open_company_profile)

                elif text == "Backup":
                    button.clicked.connect(self.open_backup)

                elif text == "Restore":
                    button.clicked.connect(self.open_restore)

                grid.addWidget(button, row, col)

                col += 1

                if col == 3:
                    col = 0
                    row += 1

            main_layout.addLayout(grid)


        add_section(
            "Transactions",
            [
                "Sales Bill",
                "Purchase Bill",
                "Payment",
                "Purchase Return",
                "Sales Return"
            ]
        )

        add_section(
            "Inventory",
            [
                "Inventory",
                "Stock Adjustment"
            ]
        )

        add_section(
            "Registers",
            [
                "Purchase Register",
                "Sales Register",
                "Payment Register",
                "Stock Ledger",
                "Party Ledger"
            ]
        )

        add_section(
            "Masters",
            [
                "Product Master",
                "Party Master"
            ]
        )

        add_section(
            "Utilities",
            [
                "Company Profile",
                "Backup",
                "Restore"
            ]
        )

        self.setLayout(main_layout)

    def open_purchase_window(self):
        self.purchase_window = PurchaseWindow()
        self.purchase_window.show()

    def open_inventory(self):
        self.inventory_window = InventoryWindow()
        self.inventory_window.show()

    def open_sales_window(self):

        self.sales_window = SalesWindow()
        self.sales_window.show()

    def open_sales_register(self):

        self.sales_register = SalesRegisterWindow()
        self.sales_register.show()

    def open_party_ledger(self):

        self.party_ledger = LedgerWindow()
        self.party_ledger.show()

    def open_payment(self):

        self.payment_window = PaymentWindow()
        self.payment_window.show()

    def open_purchase_return(self):

        self.purchase_return = PurchaseReturnWindow()
        self.purchase_return.show()

    def open_sales_return(self):

        self.sales_return = SalesReturnWindow()
        self.sales_return.show()

    def open_stock_adjustment(self):

        self.stock_adjustment = StockAdjustmentWindow()
        self.stock_adjustment.show()

    def open_purchase_register(self):

        self.purchase_register = PurchaseRegisterWindow()
        self.purchase_register.show()

    def open_payment_register(self):

        self.payment_register = PaymentRegisterWindow()
        self.payment_register.show()

    def open_product_master(self):

        self.product_master = ProductMasterWindow()
        self.product_master.show()

    def open_party_master(self):

        self.party_master = PartyMasterWindow()
        self.party_master.show()

    def open_company_profile(self):

        self.company_profile = CompanyProfileWindow()
        self.company_profile.company_updated.connect(
            self.refresh_company_name
        )
        self.company_profile.show()

    def open_backup(self):

        self.backup_window = BackupWindow()
        self.backup_window.show()

    def open_restore(self):

        self.restore_window = RestoreWindow()
        self.restore_window.show()

    def open_stock_ledger(self):

        self.stock_ledger=StockLedgerWindow()
        self.stock_ledger.show()


    def refresh_company_name(self):

        company = get_company()

        if company and company["company_name"]:
            self.title.setText(company["company_name"])
        else:
            self.title.setText("Company Name")