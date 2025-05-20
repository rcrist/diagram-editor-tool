from PyQt6.QtWidgets import *
from PyQt6.QtCore import *
from PyQt6.QtGui import *
from Shapes.BaseShapeItem import BaseShapeItem

class Line(QGraphicsLineItem, BaseShapeItem):
    def __init__(self, x1, y1, x2, y2):
        super().__init__(x1, y1, x2, y2)
        self.setPen(QPen(Qt.GlobalColor.white, 3))
        self.setFlags(
            QGraphicsItem.GraphicsItemFlag.ItemIsMovable |
            QGraphicsItem.GraphicsItemFlag.ItemIsSelectable
        )
        self.handle_size = 8
        self.handles = [QRectF(), QRectF()]
        self.handle_selected = None
        self.setAcceptHoverEvents(True)  # Ensure hover events for proper updates
        self.update_handles()

    def update_handles(self):
        line = self.line()
        self.handles[0] = QRectF(line.x1() - self.handle_size/2, line.y1() - self.handle_size/2, self.handle_size, self.handle_size)
        self.handles[1] = QRectF(line.x2() - self.handle_size/2, line.y2() - self.handle_size/2, self.handle_size, self.handle_size)
        self.prepareGeometryChange()
        self.update()

    def paint(self, painter, option, widget):
        super().paint(painter, option, widget)
        if self.isSelected():
            painter.setBrush(QBrush(Qt.GlobalColor.blue))
            painter.setPen(Qt.GlobalColor.blue)
            for handle in self.handles:
                painter.drawRect(handle)

    def mousePressEvent(self, event):
        if self.isSelected():
            for idx, handle in enumerate(self.handles):
                if handle.contains(event.pos()):
                    self.handle_selected = idx
                    event.accept()
                    return
        super().mousePressEvent(event)

    def mouseMoveEvent(self, event):
        if self.handle_selected is not None:
            line = self.line()
            if self.handle_selected == 0:
                new_line = QLineF(event.pos(), line.p2())
            else:
                new_line = QLineF(line.p1(), event.pos())
            self.setLine(new_line)
            self.update_handles()
            self.scene().update()  # Force scene redraw to clear artifacts
            event.accept()
            return
        super().mouseMoveEvent(event)
        self.update_handles()
        self.scene().update()  # Force scene redraw to clear artifacts

    def mouseReleaseEvent(self, event):
        self.handle_selected = None
        super().mouseReleaseEvent(event)
        self.scene().update()  # Force scene redraw to clear artifacts

    def rect(self):
        return self.boundingRect()

    def setRect(self, rect):
        # Not used for lines
        pass

    def brush(self):
        return QBrush(self.pen().color())

    def setBrush(self, brush):
        pen = self.pen()
        pen.setColor(brush.color())
        self.setPen(pen)

    def pen(self):
        return super().pen()

    def setPen(self, pen):
        super().setPen(pen)
        self.update()