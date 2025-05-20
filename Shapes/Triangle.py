from PyQt6.QtWidgets import *
from PyQt6.QtCore import *
from PyQt6.QtGui import *

class Triangle(QGraphicsPolygonItem):
    def __init__(self, x, y, w, h):
        super().__init__()
        # Define the three points of the triangle
        points = [
            QPointF(x + w / 2, y),           # Top center
            QPointF(x, y + h),               # Bottom left
            QPointF(x + w, y + h)            # Bottom right
        ]
        polygon = QPolygonF(points)
        self.setPolygon(polygon)
        self.setBrush(QBrush(Qt.GlobalColor.blue))
        self.setPen(QPen(Qt.GlobalColor.white, 3))
        self.setFlags(
            QGraphicsItem.GraphicsItemFlag.ItemIsMovable |
            QGraphicsItem.GraphicsItemFlag.ItemIsSelectable
        )

    def rect(self):
        # Return the bounding rectangle for compatibility
        return self.polygon().boundingRect()

    def setRect(self, rect):
        # Update the triangle's points based on the new rect
        x, y, w, h = rect.left(), rect.top(), rect.width(), rect.height()
        points = [
            QPointF(x + w / 2, y),
            QPointF(x, y + h),
            QPointF(x + w, y + h)
        ]
        self.setPolygon(QPolygonF(points))