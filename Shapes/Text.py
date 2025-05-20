from PyQt6.QtWidgets import *
from PyQt6.QtCore import *
from PyQt6.QtGui import *

class Text(QGraphicsTextItem):
    def __init__(self, x, y, w, h):
        super().__init__("Hello World!")
        self.setTextInteractionFlags(Qt.TextInteractionFlag.TextEditorInteraction)
        self.setDefaultTextColor(Qt.GlobalColor.blue)
        font = QFont()
        font.setPointSize(18)
        self.setFont(font)
        self.setPos(x, y)
        # Use setFlag, not setFlags, for QGraphicsTextItem
        self.setFlag(QGraphicsItem.GraphicsItemFlag.ItemIsMovable, True)
        self.setFlag(QGraphicsItem.GraphicsItemFlag.ItemIsSelectable, True)

    def rect(self):
        # Return a QRectF for compatibility
        return QRectF(self.pos().x(), self.pos().y(), self.boundingRect().width(), self.boundingRect().height())

    def setRect(self, rect):
        # Move the text to the new position
        self.setPos(rect.left(), rect.top())

    def brush(self):
        # For compatibility with color picker
        return QBrush(self.defaultTextColor())

    def setBrush(self, brush):
        self.setDefaultTextColor(brush.color())

    def pen(self):
        # Not used, but for compatibility
        return QPen(self.defaultTextColor())

    def setPen(self, pen):
        self.setDefaultTextColor(pen.color())