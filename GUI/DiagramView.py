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
    clipboard_items = []
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
                    # Update x and y in the shape class if attributes exist
                    if hasattr(item, 'x') and hasattr(item, 'y'):
                        try:
                            item.x = item.pos().x()
                            item.y = item.pos().y()
                        except Exception:
                            pass

    def mouseReleaseEvent(self, event):
        super().mouseReleaseEvent(event)
        if self.snap_enabled:
            for item in self.scene().selectedItems():
                if hasattr(item, 'setPos'):
                    pos = item.pos()
                    snapped_pos = snap_to_grid(pos)
                    item.setPos(snapped_pos)

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

    def cut(self):
            self.copy()
            for item in self.scene().selectedItems():
                self.scene().removeItem(item)

    def copy(self):
        DiagramView.clipboard_items = []
        for item in self.scene().selectedItems():
            # Basic serialization: store type and geometry
            if isinstance(item, Rectangle):
                DiagramView.clipboard_items.append(('Rectangle', item.rect(), item.pos(), item.brush().color()))
            elif isinstance(item, Ellipse):
                DiagramView.clipboard_items.append(('Ellipse', item.rect(), item.pos(), item.brush().color()))
            elif isinstance(item, Triangle):
                DiagramView.clipboard_items.append(('Triangle', item.polygon(), item.pos(), item.brush().color()))
            elif isinstance(item, Line):
                DiagramView.clipboard_items.append(('Line', item.line(), item.pos(), item.pen().color()))
            elif isinstance(item, Text):
                rect = item.boundingRect()
                DiagramView.clipboard_items.append(('Text', item.toPlainText(), rect, item.pos()))
            elif isinstance(item, Image):
                rect = item.boundingRect()
                DiagramView.clipboard_items.append(('Image', item.pixmap(), rect, item.pos()))

    def paste(self):
        pasted_items = []
        offset = QPointF(20, 20)  # Offset pasted items so they're visible
        for data in DiagramView.clipboard_items:
            item_type = data[0]
            if item_type == 'Rectangle':
                rect, pos, color = data[1], data[2], data[3]
                new_item = Rectangle(rect.x(), rect.y(), rect.width(), rect.height())
                new_item.setBrush(QBrush(color))
                new_item.setPos(pos + offset)
            elif item_type == 'Ellipse':
                rect, pos, color = data[1], data[2], data[3]
                new_item = Ellipse(rect.x(), rect.y(), rect.width(), rect.height())
                new_item.setBrush(QBrush(color))
                new_item.setPos(pos + offset)
            elif item_type == 'Triangle':
                polygon, pos, color = data[1], data[2], data[3]
                new_item = Triangle(rect.x(), rect.y(), rect.width(), rect.height())
                new_item.setBrush(QBrush(color))
                new_item.setPos(pos + offset)
            elif item_type == 'Line':
                line, pos, color = data[1], data[2], data[3]
                new_item = Line(line.x1(), line.y1(), line.x2(), line.y2())
                new_item.setPen(QPen(color))
                new_item.setPos(pos + offset)
            elif item_type == 'Text':
                text, rect, pos = data[1], data[2], data[3]
                new_item = Text(rect.x(), rect.y(), rect.width(), rect.height())
                new_item.setPos(pos + offset)
            elif item_type == 'Image':
                pixmap, rect, pos = data[1], data[2], data[3]
                new_item = Image(rect.x(), rect.y(), rect.width(), rect.height(), pixmap)
                new_item.setPos(pos + offset)
            else:
                continue
            self.scene().addItem(new_item)
            pasted_items.append(new_item)
        # Select newly pasted items
        for item in pasted_items:
            item.setSelected(True)