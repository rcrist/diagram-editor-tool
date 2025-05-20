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

def snap_to_grid(value):
    return round(value / GRID_SIZE) * GRID_SIZE