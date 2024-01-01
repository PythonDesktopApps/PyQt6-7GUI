import sys
from PyQt6.QtWidgets import (
    QApplication,
    QWidget,
    QListView,
    QVBoxLayout,
    QHBoxLayout,
    QLabel,
    QLineEdit,
    QPushButton,
    QGridLayout,
)
from PyQt6.QtCore import Qt, QStringListModel, QSortFilterProxyModel
from PyQt6.QtGui import QStandardItemModel, QStandardItem


class CRUDApp(QWidget):
    def __init__(self):
        super().__init__()

        self.initUI()

    def initUI(self):
        self.prefix = QLineEdit(self)
        self.name = QLineEdit(self)
        self.surname = QLineEdit(self)
        self.create_btn = QPushButton("Create", self)
        self.update_btn = QPushButton("Update", self)
        self.delete_btn = QPushButton("Delete", self)
        self.entries = QListView(self)
        self.entries.setSelectionMode(QListView.SelectionMode.SingleSelection)

        self.externDb = ["Emil, Hans", "Mustermann, Max", "Tisch, Roman"]
        self.db = QStandardItemModel()
        for entry in self.externDb:
            item = QStandardItem(entry)
            self.db.appendRow(item)

        self.dbView = QSortFilterProxyModel(self)
        self.dbView.setSourceModel(self.db)
        self.dbView.setFilterKeyColumn(-1)
        self.entries.setModel(self.dbView)

        # self.selectedIndex = self.entries.selectionModel().currentIndex()
        self.prefix.textChanged.connect(self.filterEntries)
        self.create_btn.clicked.connect(self.addToDb)
        self.delete_btn.clicked.connect(self.removeFromDb)
        self.update_btn.clicked.connect(self.updateDb)

        layout = QVBoxLayout(self)
        layout.setContentsMargins(10, 10, 10, 10)

        filter_layout = QHBoxLayout()
        filter_layout.addWidget(QLabel("Filter prefix: "))
        filter_layout.addWidget(self.prefix)

        form_layout = QGridLayout()
        form_layout.addWidget(QLabel("Name: "), 0, 0)
        form_layout.addWidget(self.name, 0, 1)
        form_layout.addWidget(QLabel("Surname: "), 1, 0)
        form_layout.addWidget(self.surname, 1, 1)

        button_layout = QHBoxLayout()
        button_layout.addWidget(self.create_btn)
        button_layout.addWidget(self.update_btn)
        button_layout.addWidget(self.delete_btn)

        layout.addLayout(filter_layout)
        layout.addWidget(self.entries)
        layout.addLayout(form_layout)
        layout.addLayout(button_layout)

        self.setLayout(layout)

        self.setWindowTitle("CRUD")
        self.setGeometry(100, 100, 400, 400)

    def filterEntries(self):
        prefix = self.prefix.text()
        self.dbView.setFilterFixedString(prefix)

    def addToDb(self):
        self.fullname = self.surname.text() + ", " + self.name.text()
        self.db.appendRow(QStandardItem(self.fullname))

    def removeFromDb(self):
        selected_row = self.entries.selectionModel().currentIndex().row()
        self.db.removeRow(selected_row)

    def updateDb(self):
        self.fullname = self.surname.text() + ", " + self.name.text()
        selected_row = self.entries.selectionModel().currentIndex().row()
        self.db.setData(self.db.index(selected_row, 0), self.fullname)


if __name__ == "__main__":
    app = QApplication(sys.argv)
    ex = CRUDApp()
    ex.show()
    sys.exit(app.exec())
