from PyQt6.QtWidgets import *
from PyQt6.QtCore import *
from PyQt6.QtGui import *
from GUI.GridScene import *
from Shapes.Rectangle import Rectangle
from Shapes.Ellipse import Ellipse
from Shapes.Triangle import Triangle
from Shapes.Line import Line
from Shapes.Text import Text
from Shapes.Image import Image

class DiagramView(QGraphicsView):
    def __init__(self, scene, right_dock):
        super().__init__(scene)
        self.right_dock = right_dock
        self.current_item = None
        self.drawing_line = False
        self.temp_line = None
        self.line_start = None
        self.scene().selectionChanged.connect(self.on_selection_changed)

    def on_selection_changed(self):
        selected_items = self.scene().selectedItems()
        if selected_items:
            item = selected_items[0]
            # Show properties for all supported item types
            if isinstance(item, (Rectangle, Ellipse, Triangle, Line, Text, Image)):
                self.current_item = item
                self.right_dock.set_controls(item)
                self.right_dock.show()
        else:
            self.right_dock.hide()
            self.current_item = None

    def set_draw_line_mode(self, enabled):
        self.drawing_line = enabled
        if not enabled and self.temp_line:
            self.scene().removeItem(self.temp_line)
            self.temp_line = None

    def mousePressEvent(self, event):
        if self.drawing_line and event.button() == Qt.MouseButton.LeftButton:
            self.line_start = self.mapToScene(event.pos())
            self.temp_line = QGraphicsLineItem(QLineF(self.line_start, self.line_start))
            self.temp_line.setPen(QPen(QColor("red"), 3, Qt.PenStyle.DashLine))
            self.scene().addItem(self.temp_line)
        else:
            super().mousePressEvent(event)

    def mousePressEvent(self, event):
        if self.drawing_line and event.button() == Qt.MouseButton.LeftButton:
            raw_point = self.mapToScene(event.pos())
            # Snap start point to grid
            self.line_start = QPointF(snap_to_grid(raw_point.x()), snap_to_grid(raw_point.y()))
            self.temp_line = QGraphicsLineItem(QLineF(self.line_start, self.line_start))
            self.temp_line.setPen(QPen(QColor("white"), 3, Qt.PenStyle.SolidLine))
            self.scene().addItem(self.temp_line)
        else:
            super().mousePressEvent(event)

    def mouseMoveEvent(self, event):
        if self.drawing_line and self.temp_line:
            raw_end = self.mapToScene(event.pos())
            # Snap end point to grid
            snapped_end = QPointF(snap_to_grid(raw_end.x()), snap_to_grid(raw_end.y()))
            self.temp_line.setLine(QLineF(self.line_start, snapped_end))
        else:
            super().mouseMoveEvent(event)

    def mouseReleaseEvent(self, event):
        if self.drawing_line and self.temp_line and event.button() == Qt.MouseButton.LeftButton:
            raw_end = self.mapToScene(event.pos())
            # Snap end point to grid
            snapped_end = QPointF(snap_to_grid(raw_end.x()), snap_to_grid(raw_end.y()))
            final_line = Line(QLineF(self.line_start, snapped_end))
            final_line.setPos(0, 0)
            self.scene().addItem(final_line)
            final_line.setSelected(True)
            self.scene().removeItem(self.temp_line)
            self.temp_line = None
            self.line_start = None
            # Optionally, exit draw mode after one line:
            self.set_draw_line_mode(False)
        else:
            super().mouseReleaseEvent(event)