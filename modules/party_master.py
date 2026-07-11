from PySide6.QtWidgets import *
from config import APP_NAME

from database.party_master_db import (
    get_parties,
    update_party,
    delete_party
)


class PartyMasterWindow(QWidget):

    def __init__(self):

        super().__init__()

        self.setWindowTitle(f"{APP_NAME} - Party Master")

        self.resize(1200,700)

        layout = QVBoxLayout()

        self.txt_search = QLineEdit()
        self.txt_search.setPlaceholderText("Search Party...")
        layout.addWidget(self.txt_search)

        self.table = QTableWidget()

        self.table.setColumnCount(5)

        self.table.setHorizontalHeaderLabels([
            "Party",
            "Mobile",
            "GSTIN",
            "Address",
            "ID"
        ])

        self.table.horizontalHeader().setSectionResizeMode(
            QHeaderView.Stretch
        )

        layout.addWidget(self.table)

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
        self.btn_edit.clicked.connect(self.edit_party)
        self.btn_delete.clicked.connect(self.delete_selected)
        self.btn_close.clicked.connect(self.close)
        self.txt_search.textChanged.connect(self.search)

        self.load_data()

    def load_data(self):

        self.rows = get_parties()

        self.table.setRowCount(len(self.rows))

        for r,row in enumerate(self.rows):

            self.table.setItem(r,0,QTableWidgetItem(row["party_name"]))
            self.table.setItem(r,1,QTableWidgetItem(row["mobile"] or ""))
            self.table.setItem(r,2,QTableWidgetItem(row["gstin"] or ""))
            self.table.setItem(r,3,QTableWidgetItem(row["address"] or ""))
            self.table.setItem(r,4,QTableWidgetItem(str(row["id"])))

    def search(self):

        text = self.txt_search.text().lower()

        for row in range(self.table.rowCount()):

            party = self.table.item(row,0).text().lower()

            self.table.setRowHidden(
                row,
                text not in party
            )

    def edit_party(self):

        row = self.table.currentRow()

        if row < 0:
            return

        pid = int(self.table.item(row,4).text())

        party = self.table.item(row,0).text()
        mobile = self.table.item(row,1).text()
        gst = self.table.item(row,2).text()
        address = self.table.item(row,3).text()

        party,ok = QInputDialog.getText(
            self,
            APP_NAME,
            "Party",
            text=party
        )

        if not ok:
            return

        mobile,ok = QInputDialog.getText(
            self,
            APP_NAME,
            "Mobile",
            text=mobile
        )

        if not ok:
            return

        gst,ok = QInputDialog.getText(
            self,
            APP_NAME,
            "GSTIN",
            text=gst
        )

        if not ok:
            return

        address,ok = QInputDialog.getText(
            self,
            APP_NAME,
            "Address",
            text=address
        )

        if not ok:
            return

        update_party(
            pid,
            party,
            mobile,
            gst,
            address
        )

        self.load_data()

    def delete_selected(self):

        row = self.table.currentRow()

        if row < 0:
            return

        reply = QMessageBox.question(
            self,
            APP_NAME,
            "Delete Party?",
            QMessageBox.Yes |
            QMessageBox.No
        )

        if reply != QMessageBox.Yes:
            return

        pid = int(self.table.item(row,4).text())

        delete_party(pid)

        self.load_data()