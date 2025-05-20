from PyQt6.QtWidgets import *
from PyQt6.QtCore import *
from PyQt6.QtGui import *

class Image(QGraphicsPixmapItem):
    def __init__(self, x, y, w, h, image_path=None):
        super().__init__()
        self.setFlag(QGraphicsItem.GraphicsItemFlag.ItemIsMovable, True)
        self.setFlag(QGraphicsItem.GraphicsItemFlag.ItemIsSelectable, True)
        self.setPos(x, y)
        default_path = "C:\\python_projects\\images\\earth.jpg"
        if image_path:
            self.image_path = image_path
            self.set_image(image_path, w, h)
        else:
            self.image_path = default_path
            self.set_image(default_path, w, h)

    def set_image(self, image_path, w, h):
        pixmap = QPixmap(image_path)
        if not pixmap.isNull():
            pixmap = pixmap.scaled(int(w), int(h), Qt.AspectRatioMode.KeepAspectRatio, Qt.TransformationMode.SmoothTransformation)
            self.setPixmap(pixmap)
            self.image_path = image_path

    def rect(self):
        return QRectF(self.pos().x(), self.pos().y(), self.pixmap().width(), self.pixmap().height())

    def setRect(self, rect):
        # Rescale the image to the new rect size
        if self.image_path:
            self.set_image(self.image_path, int(rect.width()), int(rect.height()))
        self.setPos(rect.left(), rect.top())

    def brush(self):
        # Not used, but for compatibility
        return QBrush()

    def setBrush(self, brush):
        pass

    def pen(self):
        # Not used, but for compatibility
        return QPen()

    def setPen(self, pen):
        pass