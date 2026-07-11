from PySide6.QtWidgets import (
    QStyledItemDelegate,
    QLineEdit
)


class ProductDelegate(QStyledItemDelegate):

    def __init__(self, completer, parent=None):
        super().__init__(parent)
        self.completer = completer

    def createEditor(self, parent, option, index):

        editor = QLineEdit(parent)

        editor.setCompleter(self.completer)

        return editor