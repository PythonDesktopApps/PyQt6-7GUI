import sys
from PyQt6.QtWidgets import QApplication, QWidget, QHBoxLayout, QLabel, QPushButton
from PyQt6.QtCore import Qt


class CounterApp(QWidget):
    def __init__(self):
        super().__init__()

        self.initUI()

    def initUI(self):
        self.count = QLabel("0", self)
        self.count.setAlignment(Qt.AlignmentFlag.AlignCenter)
        self.countUp = QPushButton("Increment", self)
        self.countUp.clicked.connect(self.incrementCount)

        layout = QHBoxLayout(self)
        layout.addWidget(self.count)
        layout.addWidget(self.countUp)
        self.setLayout(layout)

        self.setWindowTitle("Counter")
        self.setGeometry(100, 100, 200, 100)

    def incrementCount(self):
        current_count = int(self.count.text())
        new_count = current_count + 1
        self.count.setText(str(new_count))


if __name__ == "__main__":
    app = QApplication(sys.argv)
    ex = CounterApp()
    ex.show()
    sys.exit(app.exec())
