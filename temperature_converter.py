import sys
from PyQt6.QtWidgets import QApplication, QWidget, QHBoxLayout, QLabel, QLineEdit
from PyQt6.QtCore import Qt
from PyQt6.QtGui import QDoubleValidator


class TemperatureConverterApp(QWidget):
    def __init__(self):
        super().__init__()

        self.initUI()

    def initUI(self):
        self.celsius = QLineEdit(self)
        self.fahrenheit = QLineEdit(self)

        # Set up double validators to ensure valid numeric input
        double_validator = QDoubleValidator(-100, 100, 2, self)
        self.celsius.setValidator(double_validator)
        self.fahrenheit.setValidator(double_validator)

        self.celsius.textChanged.connect(self.updateFahrenheit)
        self.fahrenheit.textChanged.connect(self.updateCelsius)

        layout = QHBoxLayout(self)
        layout.addWidget(QLabel("Celsius"))
        layout.addWidget(self.celsius)
        layout.addWidget(QLabel("Fahrenheit"))
        layout.addWidget(self.fahrenheit)

        self.setLayout(layout)

        self.setWindowTitle("Temperature Converter")
        self.setGeometry(100, 100, 400, 50)

    def updateFahrenheit(self):
        if self.celsius.hasAcceptableInput():
            c = float(self.celsius.text())
            self.fahrenheit.setText(str(self.celsiusToFahrenheit(c)))

    def updateCelsius(self):
        if self.fahrenheit.hasAcceptableInput():
            f = float(self.fahrenheit.text())
            self.celsius.setText(str(self.fahrenheitToCelsius(f)))

    def celsiusToFahrenheit(self, c):
        return (9 / 5 * c) + 32

    def fahrenheitToCelsius(self, f):
        return 5 / 9 * (f - 32)


if __name__ == "__main__":
    app = QApplication(sys.argv)
    ex = TemperatureConverterApp()
    ex.show()
    sys.exit(app.exec())
