import sys
from PyQt6.QtWidgets import (
    QApplication,
    QWidget,
    QGraphicsScene,
    QGraphicsEllipseItem,
    QGraphicsView,
    QVBoxLayout,
    QPushButton,
    QSlider,
    QLabel,
    QDialog,
)
from PyQt6.QtCore import Qt, QRectF
from PyQt6.QtGui import QPainter, QPen


class CircleDrawer(QWidget):
    def __init__(self):
        super().__init__()

        self.initUI()

    def initUI(self):
        self.btn_undo = QPushButton("Undo", self)
        self.btn_redo = QPushButton("Redo", self)
        self.canvas = CircleDrawerCanvas()

        self.btn_undo.clicked.connect(self.canvas.undo)
        self.btn_redo.clicked.connect(self.canvas.redo)

        layout = QVBoxLayout(self)
        layout.addWidget(self.btn_undo)
        layout.addWidget(self.btn_redo)
        layout.addWidget(self.canvas)

        self.setLayout(layout)

        self.setWindowTitle("Circle Drawer")
        self.setGeometry(100, 100, 400, 400)


class CircleDrawerCanvas(QGraphicsView):
    def __init__(self):
        super().__init__()

        self.scene = QGraphicsScene(self)
        self.setScene(self.scene)
        self.circles = []
        self.hovered = None
        # self.btn_diameter = QPushButton("Diameter...")

        # self.btn_diameter.clicked.connect(self.showDialog)

        self.popup = QDialog(self)
        layout = QVBoxLayout(self.popup)
        # layout.addWidget(self.btn_diameter)
        # self.setLayout(layout)

        self.setRenderHint(QPainter.RenderHint.Antialiasing)
        self.setSceneRect(0, 0, 400, 400)

        self.history = [[]]
        self.historyCursor = 0

    def draw(self):
        self.scene.clear()

        for c in self.circles:
            rect = QRectF(c.x - c.d / 2, c.y - c.d / 2, c.d, c.d)
            item = QGraphicsEllipseItem(rect)
            item.setPen(QPen(Qt.black))

            if c == self.hovered:
                item.setBrush(Qt.lightGray)

            self.scene.addItem(item)

    def addCircle(self, circle):
        self.circles.append(circle)
        self.addSnapshot()

    def getNearestCircleAt(self, x, y):
        circle = None
        minDist = float("inf")

        for c in self.circles:
            d = ((x - c.x) ** 2 + (y - c.y) ** 2) ** 0.5

            if d <= c.d / 2 and d < minDist:
                circle = c
                minDist = d

        return circle

    def showDialog(self):
        # if self.hovered:
        dialog = QDialog(self)
        info = QLabel(
            f"Adjust diameter of circle at ({self.hovered.x}, {self.hovered.y})"
        )
        slider = QSlider(Qt.Horizontal)
        slider.setRange(10, 50)
        slider.setValue(self.hovered.d)

        slider.valueChanged.connect(lambda value: self.adjustDiameter(value))

        dialog.setWindowTitle("Adjust Diameter")
        dialog.layout = QVBoxLayout(dialog)
        dialog.layout.addWidget(info)
        dialog.layout.addWidget(slider)
        dialog.exec()

    def adjustDiameter(self, value):
        if self.hovered:
            index = self.circles.index(self.hovered)
            self.circles[index] = self.hovered._replace(d=value)
            self.draw()

    def addSnapshot(self):
        self.history = self.history[: self.historyCursor + 1] + [self.circles]
        self.historyCursor += 1

    def undo(self):
        if self.historyCursor > 0:
            self.historyCursor -= 1
            self.circles = self.history[self.historyCursor]
            self.draw()

    def redo(self):
        if self.historyCursor < len(self.history) - 1:
            self.historyCursor += 1
            self.circles = self.history[self.historyCursor]
            self.draw()

    def mousePressEvent(self, event):
        if event.button() == Qt.MouseButton.LeftButton:
            painter = QPainter(self)
            pen = QPen()
            pen.setWidth(5)
            painter.setPen(pen)
            painter.drawEllipse(300, 300, 70, 70)

            self.addCircle(painter.drawEllipse(event.pos(), 5, 5))
            self.mouseMoveEvent(event)

        elif event.button() == Qt.MouseButton.RightButton and self.hovered:
            self.popup.setGeometry(event.pos().x(), event.pos().y(), 0, 0)
            self.popup.exec()

    def mouseMoveEvent(self, event):
        try:
            self.hovered = self.getNearestCircleAt(event.pos().x(), event.pos().y())
            self.draw()
        except:
            print("No circle yet")


if __name__ == "__main__":
    app = QApplication(sys.argv)
    ex = CircleDrawer()
    ex.show()
    sys.exit(app.exec())
