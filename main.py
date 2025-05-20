from PyQt6.QtWidgets import *
from PyQt6.QtCore import *
from PyQt6.QtGui import *
import sys

from GUI.LeftDock import LeftDock

class MainWindow(QMainWindow):
    def __init__(self):
        super().__init__()
        self.setWindowTitle("Digram Editor Tool")
        self.setGeometry(200, 100, 1200, 600)

        # Create a QGraphicsScene
        self.scene = QGraphicsScene(self)
        self.scene.setSceneRect(0, 0, 1000, 500)

        # Create a QGraphicsView, set the scene, and set as central widget
        self.view = QGraphicsView(self.scene, self)
        self.view.setRenderHint(QPainter.RenderHint.Antialiasing)
        self.setCentralWidget(self.view)

        # Left Dock (Shapes)
        self.left_dock = LeftDock(self, self.scene, self.view)
        self.addDockWidget(Qt.DockWidgetArea.LeftDockWidgetArea, self.left_dock)       

if __name__ == "__main__":
    app = QApplication(sys.argv)
    window = MainWindow()
    window.show()
    sys.exit(app.exec())