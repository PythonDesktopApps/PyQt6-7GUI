import sys
from PyQt6.QtWidgets import (
    QApplication,
    QWidget,
    QVBoxLayout,
    QHBoxLayout,
    QLabel,
    QProgressBar,
    QSlider,
    QPushButton,
)
from PyQt6.QtCore import Qt, QTimer


class TimerApp(QWidget):
    def __init__(self):
        super().__init__()

        self.initUI()

    def initUI(self):
        self.progress_bar = QProgressBar(self)
        self.elapsed_label = QLabel(self)
        self.duration_slider = QSlider(Qt.Orientation.Horizontal, self)
        self.reset_btn = QPushButton("Reset", self)

        self.elapsed = 0
        self.duration_slider.valueChanged.connect(self.updateProgressBar)
        self.reset_btn.clicked.connect(self.resetTimer)

        self.timer = QTimer(self)
        self.timer.timeout.connect(self.updateElapsed)
        self.timer.start(100)

        layout = QVBoxLayout(self)
        layout.addWidget(QLabel("Elapsed Time:"))
        layout.addWidget(self.elapsed_label)
        layout.addWidget(self.progress_bar)
        layout.addWidget(QLabel("Duration:"))
        layout.addWidget(self.duration_slider)
        layout.addWidget(self.reset_btn)
        self.setLayout(layout)

        self.setWindowTitle("Timer")
        self.setGeometry(100, 100, 300, 200)

    def updateProgressBar(self, value):
        self.progress_bar.setValue(
            int(self.elapsed / self.duration_slider.value() * 100)
        )

    def resetTimer(self):
        self.elapsed = 0
        self.elapsed_label.setText(self.formatElapsed())

    def updateElapsed(self):
        self.elapsed += 1
        self.elapsed_label.setText(self.formatElapsed())

    def formatElapsed(self):
        seconds = int(self.elapsed / 10.0)
        dezipart = int(self.elapsed % 10)
        return f"{seconds}.{dezipart}s"


if __name__ == "__main__":
    app = QApplication(sys.argv)
    ex = TimerApp()
    ex.show()
    sys.exit(app.exec())
