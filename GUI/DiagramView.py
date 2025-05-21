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
    def __init__(self, scene, right_dock, parent=None):
        super().__init__(scene, parent)
        self.right_dock = right_dock
        self.current_item = None
        self.drawing_line = False
        self.temp_line = None
        self.line_start = None
        self.grid_visible = True
        self.snap_enabled = True
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
        super().mouseMoveEvent(event)
        if self.snap_enabled:
            for item in self.scene().selectedItems():
                if hasattr(item, 'setPos') and hasattr(item, 'pos'):
                    pos = item.pos()
                    snapped_pos = snap_to_grid(pos)
                    if pos != snapped_pos:
                        item.setPos(snapped_pos)

    def mouseReleaseEvent(self, event):
        super().mouseReleaseEvent(event)
        if self.snap_enabled:
            for item in self.scene().selectedItems():
                if hasattr(item, 'setPos'):
                    pos = item.pos()
                    snapped_pos = snap_to_grid(pos)
                    item.setPos(snapped_pos)
                if hasattr(item, 'rect') and hasattr(item, 'setRect'):
                    rect = item.rect()
                    snapped_rect = QRectF(
                        snap_to_grid(rect.topLeft()),
                        snap_to_grid(rect.bottomRight())
                    )
                    item.setRect(snapped_rect)

    def drawBackground(self, painter, rect):
        super().drawBackground(painter, rect)
        if self.grid_visible:
            # Draw grid lines
            left = int(rect.left())
            right = int(rect.right())
            top = int(rect.top())
            bottom = int(rect.bottom())
            grid_size = 10
            painter.setPen(QPen(QColor(100, 100, 100), 1))
            for x in range(left - left % grid_size, right, grid_size):
                painter.drawLine(x, top, x, bottom)
            for y in range(top - top % grid_size, bottom, grid_size):
                painter.drawLine(left, y, right, y)

    def toggle_grid(self):
        self.grid_visible = not self.grid_visible
        self.snap_enabled = self.grid_visible
        self.viewport().update()