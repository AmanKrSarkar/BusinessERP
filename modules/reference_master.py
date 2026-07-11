from PySide6.QtWidgets import (
    QWidget,
    QLabel,
    QLineEdit,
    QPushButton,
    QVBoxLayout,
    QHBoxLayout,
    QComboBox,
    QTableWidget,
    QTableWidgetItem,
    QMessageBox
)

from database.reference_db import (
    save_reference,
    get_references,
    reference_exists,
    update_reference,
    delete_reference
)

class ReferenceMaster(QWidget):

    def __init__(self):

        super().__init__()

        self.setWindowTitle("Reference Master")
        self.resize(700,500)

        self.create_ui()

        self.load_data()
        self.selected_id = None

    def create_ui(self):

        layout = QVBoxLayout()

        # -----------------------------
        # Category
        # -----------------------------

        row1 = QHBoxLayout()

        row1.addWidget(QLabel("Category"))

        self.cmb_category = QComboBox()

        self.cmb_category.addItems([
            "OTHER_INCOME",
            "EXPENSE"
        ])

        row1.addWidget(self.cmb_category)

        layout.addLayout(row1)

        # -----------------------------
        # Name
        # -----------------------------

        row2 = QHBoxLayout()

        row2.addWidget(QLabel("Name"))

        self.txt_name = QLineEdit()

        row2.addWidget(self.txt_name)

        layout.addLayout(row2)

        # -----------------------------
        # Save Button
        # -----------------------------

        self.btn_save = QPushButton("Save")
        self.btn_delete = QPushButton("Delete")

        layout.addWidget(self.btn_save)
        layout.addWidget(self.btn_delete)

        # -----------------------------
        # Search
        # -----------------------------

        row3 = QHBoxLayout()

        row3.addWidget(QLabel("Search"))

        self.txt_search = QLineEdit()

        row3.addWidget(self.txt_search)

        layout.addLayout(row3)

        # -----------------------------
        # Table
        # -----------------------------

        self.table = QTableWidget()

        self.table.setColumnCount(3)

        self.table.setHorizontalHeaderLabels([
            "ID",
            "Category",
            "Name"
        ])

        self.table.setColumnHidden(0, True)

        layout.addWidget(self.table)

        self.setLayout(layout)

        # -----------------------------
        # Signals
        # -----------------------------

        self.btn_save.clicked.connect(self.save_data)

        self.cmb_category.currentIndexChanged.connect(
            self.load_data
        )

        self.txt_search.textChanged.connect(
            self.load_data
        )

        self.table.cellDoubleClicked.connect(
            self.edit_reference
        )

        self.btn_delete.clicked.connect(
            self.delete_data
        )

    def save_data(self):

        category = self.cmb_category.currentText()

        name = self.txt_name.text().strip()

        if name == "":

            QMessageBox.warning(
                self,
                "Warning",
                "Enter Name."
            )

            return

        # -----------------------
        # UPDATE
        # -----------------------

        if self.selected_id is not None:

            update_reference(
                self.selected_id,
                category,
                name
            )

            QMessageBox.information(
                self,
                "Success",
                "Updated Successfully."
            )

        # -----------------------
        # ADD
        # -----------------------

        else:

            if reference_exists(category, name):

                QMessageBox.information(
                    self,
                    "Information",
                    "Already Exists."
                )

                return

            save_reference(
                category,
                name
            )

            QMessageBox.information(
                self,
                "Success",
                "Saved Successfully."
            )

        self.selected_id = None

        self.txt_name.clear()
        self.cmb_category.setCurrentIndex(0)

        self.load_data()

    def load_data(self):

        category = self.cmb_category.currentText()

        rows = get_references(category)

        search = self.txt_search.text().strip().lower()

        self.table.setRowCount(0)

        for data in rows:

            if search and search not in data["name"].lower():
                continue

            row = self.table.rowCount()

            self.table.insertRow(row)

            self.table.setItem(
                row,
                0,
                QTableWidgetItem(str(data["id"]))
            )

            self.table.setItem(
                row,
                1,
                QTableWidgetItem(data["category"])
            )

            self.table.setItem(
                row,
                2,
                QTableWidgetItem(data["name"])
            )

        self.table.resizeColumnsToContents()

    def edit_reference(self, row, column):

        self.selected_id = int(
            self.table.item(row,0).text()
        )

        self.cmb_category.setCurrentText(
            self.table.item(row,1).text()
        )

        self.txt_name.setText(
            self.table.item(row,2).text()
        )

        self.txt_name.setFocus()
        self.txt_name.selectAll()

    def delete_data(self):

        if self.selected_id is None:

            QMessageBox.warning(
                self,
                "Warning",
                "Select a record first."
            )

            return

        reply = QMessageBox.question(

            self,

            "Delete",

            "Delete selected record?",

            QMessageBox.Yes | QMessageBox.No

        )

        if reply == QMessageBox.Yes:

            delete_reference(self.selected_id)

            self.selected_id = None

            self.txt_name.clear()

            self.load_data()

            QMessageBox.information(

                self,

                "Success",

                "Deleted Successfully."

            )