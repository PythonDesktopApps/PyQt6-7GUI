import sys
from PyQt6.QtWidgets import (
    QApplication,
    QWidget,
    QVBoxLayout,
    QComboBox,
    QLineEdit,
    QPushButton,
    QDateEdit,
)
from PyQt6.QtCore import Qt, QDate
from PyQt6.QtGui import QIntValidator


class FlightBookerApp(QWidget):
    def __init__(self):
        super().__init__()

        self.initUI()

    def initUI(self):
        self.flightType = QComboBox(self)
        self.flightType.addItems(["one-way flight", "return flight"])
        self.flightType.setCurrentText("one-way flight")

        self.startDate = QDateEdit(self, calendarPopup=True)
        self.startDate.setDate(QDate.currentDate())

        self.returnDate = QDateEdit(self, calendarPopup=True)
        self.returnDate.setDate(QDate.currentDate())

        self.book = QPushButton("Book", self)

        self.returnDate.setEnabled(False)

        self.flightType.currentTextChanged.connect(self.toggleReturnDate)
        self.startDate.dateChanged.connect(self.validateStartDate)
        self.returnDate.dateChanged.connect(self.validateReturnDate)

        layout = QVBoxLayout(self)
        layout.addWidget(self.flightType)
        layout.addWidget(self.startDate)
        layout.addWidget(self.returnDate)
        layout.addWidget(self.book)

        self.setLayout(layout)

        self.setWindowTitle("FlightBooker")
        self.setGeometry(100, 100, 300, 200)

    def toggleReturnDate(self):
        self.returnDate.setEnabled(self.flightType.currentText() == "return flight")

    def validateStartDate(self):
        # since we used date picker, there's really no need to validate
        # but just in case
        is_valid = self.isDateString(self.startDate.text())
        self.startDate.setStyleSheet("" if is_valid else "background-color: lightcoral")

    def validateReturnDate(self):
        is_valid = self.isDateString(self.returnDate.text())
        self.returnDate.setStyleSheet(
            "" if is_valid else "background-color: lightcoral"
        )

    def isDateString(self, date_str):
        try:
            QDate.fromString(date_str, "yyyy-MM-dd")
            return True
        except:
            return False


if __name__ == "__main__":
    app = QApplication(sys.argv)
    ex = FlightBookerApp()
    ex.show()
    sys.exit(app.exec())
