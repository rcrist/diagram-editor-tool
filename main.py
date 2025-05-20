from PyQt6.QtWidgets import *
from PyQt6.QtCore import *
from PyQt6.QtGui import *
import sys

from GUI.LeftDock import LeftDock
from GUI.RightDock import RightDock
from GUI.DiagramView import DiagramView
from GUI.MenuBar import MenuBar

class MainWindow(QMainWindow):
    def __init__(self):
        super().__init__()
        self.setWindowTitle("Digram Editor Tool")
        self.setGeometry(200, 100, 1200, 600)

        # Add MenuBar
        self.setMenuBar(MenuBar(self))

        # Create a QGraphicsScene
        self.scene = QGraphicsScene(self)
        self.scene.setSceneRect(0, 0, 1000, 500)

        # Create a QGraphicsView, set the scene, and set as central widget
        self.right_dock = RightDock(self)
        self.view = DiagramView(self.scene, self.right_dock)
        self.view.setRenderHint(QPainter.RenderHint.Antialiasing)
        self.setCentralWidget(self.view)

        # Left Dock (Shapes)
        self.left_dock = LeftDock(self, self.scene, self.view)
        self.addDockWidget(Qt.DockWidgetArea.LeftDockWidgetArea, self.left_dock)

        # Right Dock (Properties)
        self.addDockWidget(Qt.DockWidgetArea.RightDockWidgetArea, self.right_dock)
        self.right_dock.hide()      

if __name__ == "__main__":
    app = QApplication(sys.argv)
    window = MainWindow()
    window.show()
    sys.exit(app.exec())