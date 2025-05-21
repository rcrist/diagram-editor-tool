from PyQt6.QtWidgets import *
from PyQt6.QtCore import *
from PyQt6.QtGui import *

GRID_SIZE = 10
GRID_COLOR = QColor("#333333")

class GridScene(QGraphicsScene):
    def drawBackground(self, painter, rect):
        super().drawBackground(painter, rect)
        left = int(rect.left()) - (int(rect.left()) % GRID_SIZE)
        top = int(rect.top()) - (int(rect.top()) % GRID_SIZE)
        lines = []
        for x in range(left, int(rect.right()), GRID_SIZE):
            lines.append(QLineF(x, rect.top(), x, rect.bottom()))
        for y in range(top, int(rect.bottom()), GRID_SIZE):
            lines.append(QLineF(rect.left(), y, rect.right(), y))
        painter.setPen(QPen(GRID_COLOR, 1))
        painter.drawLines(lines)

def snap_to_grid(point, grid_size=20):
    # If point is QPointF or QPoint
    if hasattr(point, 'x') and hasattr(point, 'y'):
        x = round(point.x() / grid_size) * grid_size
        y = round(point.y() / grid_size) * grid_size
        return QPointF(x, y)
    # If point is a number (int or float)
    elif isinstance(point, (int, float)):
        return round(point / grid_size) * grid_size
    else:
        raise TypeError("snap_to_grid expects QPointF, QPoint, int, or float")