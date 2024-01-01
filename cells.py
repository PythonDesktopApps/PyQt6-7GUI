from PyQt6.QtWidgets import (
    QApplication,
    QWidget,
    QTableWidget,
    QVBoxLayout,
    QListView,
    QAbstractItemView,
    QHeaderView,
    QTableView,
)
from PyQt6.QtCore import Qt


class Cell:
    def __init__(self, row, col):
        self.row = row
        self.col = col
        self.formula = ""
        self.value = ""
        self.text = ""
        self.user_data = ""


class Spreadsheet(QWidget):
    def __init__(self, height, width):
        super().__init__()

        self.cells = [[Cell(i, j) for j in range(width)] for i in range(height)]

        self.table = QTableWidget(height, width, self)

        self.init_ui()

    def init_ui(self):
        layout = QVBoxLayout(self)

        self.table.setSelectionMode(QTableView.SelectionMode.SingleSelection)
        self.table.setSelectionBehavior(QTableView.SelectionBehavior.SelectRows)
        self.table.setHorizontalHeaderLabels(
            [chr(ord("A") + i) for i in range(len(self.cells[0]))]
        )

        layout.addWidget(self.table)
        self.setLayout(layout)

        self.table.itemChanged.connect(self.cell_changed)

    def cell_changed(self, item):
        row, col = item.row(), item.column()
        cell = self.cells[row][col]

        cell.raw_text = item.text()

        cell.value = self.evaluate(cell.raw_text)
        item.setText(str(cell.value))

    def row_header_clicked(self, index):
        self.table.selectRow(index.row())

    def evaluate(self, raw_text):
        # Add your evaluation logic here
        if raw_text.startswith("=") or raw_text.startswith("+"):
            return eval(raw_text[1:].replace("=", "=="))
        else:
            return raw_text


def main():
    app = QApplication([])
    spreadsheet = Spreadsheet(100, 26)
    spreadsheet.show()
    app.exec()


if __name__ == "__main__":
    main()
