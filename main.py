from PyQt6.QtWidgets import *
from PyQt6.QtCore import *
from PyQt6.QtGui import *
import sys

from Shapes.Rectangle import Rectangle

class MainWindow(QMainWindow):
    def __init__(self):
        super().__init__()
        self.setWindowTitle("Digram Editor Tool")
        self.setGeometry(200, 100, 1200, 600)

        # Create a QGraphicsScene
        self.scene = QGraphicsScene(self)
        self.scene.setSceneRect(0, 0, 1000, 500)

        # Add a rectangle item to the scene
        self.shape_item = Rectangle(50, 50, 200, 100)
        self.scene.addItem(self.shape_item)

        # Create a QGraphicsView, set the scene, and set as central widget
        self.view = QGraphicsView(self.scene, self)
        self.setCentralWidget(self.view)
        

if __name__ == "__main__":
    app = QApplication(sys.argv)
    window = MainWindow()
    window.show()
    sys.exit(app.exec())