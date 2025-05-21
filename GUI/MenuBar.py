from PyQt6.QtWidgets import *
from PyQt6.QtCore import *
from PyQt6.QtGui import *
from PyQt6.QtPrintSupport import QPrinter, QPrintDialog
from GUI.GridScene import *
from Shapes.Rectangle import Rectangle
from Shapes.Ellipse import Ellipse
from Shapes.Triangle import Triangle
from Shapes.Line import Line
from Shapes.Text import Text
from Shapes.Image import Image
import json

class MenuBar(QMenuBar):
    def __init__(self, parent=None):
        super().__init__(parent)

        # File Menu
        file_menu = self.addMenu("File")
        new_action = file_menu.addAction("New")
        new_action.triggered.connect(self.new_file)
        open_action = file_menu.addAction("Open")
        open_action.triggered.connect(self.open_file)
        save_action = file_menu.addAction("Save")
        save_action.triggered.connect(self.save_file)
        print_action = file_menu.addAction("Print")
        print_action.triggered.connect(self.print_diagram)
        file_menu.addSeparator()
        exit_action = file_menu.addAction("Exit")
        exit_action.triggered.connect(QApplication.instance().quit)

        # Edit Menu
        edit_menu = self.addMenu("Edit")
        cut_action = edit_menu.addAction("Cut")
        cut_action.triggered.connect(self.cut)
        copy_action = edit_menu.addAction("Copy")
        copy_action.triggered.connect(self.copy)
        paste_action = edit_menu.addAction("Paste")
        paste_action.triggered.connect(self.paste)

        # Settings Menu
        settings_menu = self.addMenu("Settings")
        toggle_grid_action = settings_menu.addAction("Toggle Grid")
        toggle_grid_action.triggered.connect(self.toggle_grid)
        toggle_theme_action = settings_menu.addAction("Toggle Theme")
        toggle_theme_action.triggered.connect(self.toggle_theme)

        # Help Menu
        help_menu = self.addMenu("Help")
        about_action = help_menu.addAction("About")
        about_action.triggered.connect(self.show_about_dialog)

    def show_about_dialog(self):
        QMessageBox.about(
            self,
            "About Diagram Editor Tool",
            "Diagram Editor Tool\nVersion 1.0\n\nA simple diagram editor built with PyQt6."
        )

    def toggle_theme(self):
        # Simple dark/light mode toggle using QApplication palette
        app = QApplication.instance()
        palette = app.palette()
        if palette.color(QPalette.ColorRole.Window) == QColor(53, 53, 53):
            # Switch to light mode
            app.setPalette(QApplication.style().standardPalette())
            # Set menubar and menu drop downs to light mode
            self.setStyleSheet("""
                QMenuBar, QMenu, QMenuBar::item, QMenu::item {
                    background: #f0f0f0;
                    color: #000;
                }
                QMenuBar::item:selected, QMenu::item:selected {
                    background: #d0d0d0;
                }
            """)
        else:
            # Switch to dark mode
            dark_palette = QPalette()
            dark_palette.setColor(QPalette.ColorRole.Window, QColor(53, 53, 53))
            dark_palette.setColor(QPalette.ColorRole.WindowText, Qt.GlobalColor.white)
            dark_palette.setColor(QPalette.ColorRole.Base, QColor(35, 35, 35))
            dark_palette.setColor(QPalette.ColorRole.AlternateBase, QColor(53, 53, 53))
            dark_palette.setColor(QPalette.ColorRole.ToolTipBase, Qt.GlobalColor.white)
            dark_palette.setColor(QPalette.ColorRole.ToolTipText, Qt.GlobalColor.white)
            dark_palette.setColor(QPalette.ColorRole.Text, Qt.GlobalColor.white)
            dark_palette.setColor(QPalette.ColorRole.Button, QColor(53, 53, 53))
            dark_palette.setColor(QPalette.ColorRole.ButtonText, Qt.GlobalColor.white)
            dark_palette.setColor(QPalette.ColorRole.BrightText, Qt.GlobalColor.red)
            dark_palette.setColor(QPalette.ColorRole.Highlight, QColor(42, 130, 218))
            dark_palette.setColor(QPalette.ColorRole.HighlightedText, Qt.GlobalColor.black)
            app.setPalette(dark_palette)
            # Set menubar and menu drop downs to dark mode
            self.setStyleSheet("""
                QMenuBar, QMenu, QMenuBar::item, QMenu::item {
                    background: #353535;
                    color: #fff;
                }
                QMenuBar::item:selected, QMenu::item:selected {
                    background: #2a82da;
                }
            """)

    def toggle_grid(self):
        # Toggle grid visibility in the scene if it supports it
        main_window = self.parent()
        if hasattr(main_window, "view") and hasattr(main_window.view, "toggle_grid"):
            main_window.view.toggle_grid()
        else:
            QMessageBox.information(self, "Toggle Grid", "Grid toggling is not implemented in the view.")

    def cut(self):
        main_window = self.parent()
        if hasattr(main_window, "view") and hasattr(main_window.view, "cut"):
            main_window.view.cut()
        else:
            QMessageBox.information(self, "Cut", "Cut operation is not implemented in the view.")

    def copy(self):
        main_window = self.parent()
        if hasattr(main_window, "view") and hasattr(main_window.view, "copy"):
            main_window.view.copy()
        else:
            QMessageBox.information(self, "Copy", "Copy operation is not implemented in the view.")

    def paste(self):
        main_window = self.parent()
        if hasattr(main_window, "view") and hasattr(main_window.view, "paste"):
            main_window.view.paste()
        else:
            QMessageBox.information(self, "Paste", "Paste operation is not implemented in the view.")

    def new_file(self):
        main_window = self.parent()
        if hasattr(main_window, "scene"):
            main_window.scene.clear()
        else:
            QMessageBox.information(self, "New", "Scene clearing is not implemented.")

    def open_file(self):
        main_window = self.parent()
        if not hasattr(main_window, "scene"):
            QMessageBox.information(self, "Open", "Scene loading is not implemented.")
            return
        file_name, _ = QFileDialog.getOpenFileName(self, "Open Diagram", "", "Diagram Files (*.json);;All Files (*)")
        if file_name:
            try:
                with open(file_name, "r", encoding="utf-8") as f:
                    items_data = json.load(f)
                main_window.scene.clear()
                for item_data in items_data:
                    item = self.deserialize_item(item_data)
                    if item:
                        main_window.scene.addItem(item)
            except Exception as e:
                QMessageBox.warning(self, "Open", f"Failed to open file:\n{e}")

    def save_file(self):
        main_window = self.parent()
        if not hasattr(main_window, "scene"):
            QMessageBox.information(self, "Save", "Scene saving is not implemented.")
            return
        file_name, _ = QFileDialog.getSaveFileName(self, "Save Diagram", "", "Diagram Files (*.json);;All Files (*)")
        if file_name:
            try:
                items_data = [self.serialize_item(item) for item in main_window.scene.items()]
                # Remove None items (if any)
                items_data = [item for item in items_data if item is not None]
                with open(file_name, "w", encoding="utf-8") as f:
                    json.dump(items_data, f, indent=2)
            except Exception as e:
                QMessageBox.warning(self, "Save", f"Failed to save file:\n{e}")

    def serialize_item(self, item):
        # Rectangle
        if isinstance(item, Rectangle):
            rect = item.rect()
            color = item.brush().color()
            pos = item.pos()
            return {
                "type": "rect",
                "x": rect.x(),
                "y": rect.y(),
                "w": rect.width(),
                "h": rect.height(),
                "color": color.name(QColor.NameFormat.HexArgb),
                "pos_x": pos.x(),
                "pos_y": pos.y()
            }
        # Ellipse
        if isinstance(item, Ellipse):
            rect = item.rect()
            color = item.brush().color()
            pos = item.pos()
            return {
                "type": "ellipse",
                "x": rect.x(),
                "y": rect.y(),
                "w": rect.width(),
                "h": rect.height(),
                "color": color.name(QColor.NameFormat.HexArgb),
                "pos_x": pos.x(),
                "pos_y": pos.y()
            }
        # Triangle (polygon version)
        if isinstance(item, Triangle):
            rect = item.rect()
            color = item.brush().color()
            pos = item.pos()
            return {
                "type": "triangle",
                "x": rect.x(),
                "y": rect.y(),
                "w": rect.width(),
                "h": rect.height(),
                "color": color.name(QColor.NameFormat.HexArgb),
                "pos_x": pos.x(),
                "pos_y": pos.y()
            }
        # Line
        if isinstance(item, Line):
            line = item.line()
            color = item.pen().color()
            pos = item.pos()
            return {
                "type": "line",
                "x1": line.x1(),
                "y1": line.y1(),
                "x2": line.x2(),
                "y2": line.y2(),
                "color": color.name(QColor.NameFormat.HexArgb),
                "pos_x": pos.x(),
                "pos_y": pos.y()
            }
        # Text
        if isinstance(item, Text):
            rect = item.boundingRect()
            pos = item.pos()
            return {
                "type": "text",
                "x": rect.x(),
                "y": rect.y(),
                "w": rect.width(),
                "h": rect.height(),
                "text": item.toPlainText(),
                "pos_x": pos.x(),
                "pos_y": pos.y()
            }
        # Image
        if isinstance(item, Image):
            rect = item.boundingRect()
            pos = item.pos()
            # Save image as base64 string
            pixmap = item.pixmap()
            ba = QByteArray()
            buffer = QBuffer(ba)
            buffer.open(QBuffer.OpenModeFlag.WriteOnly)
            pixmap.save(buffer, "PNG")
            img_b64 = ba.toBase64().data().decode()
            return {
                "type": "image",
                "x": rect.x(),
                "y": rect.y(),
                "w": rect.width(),
                "h": rect.height(),
                "image_data": img_b64,
                "pos_x": pos.x(),
                "pos_y": pos.y()
            }
        return None

    def deserialize_item(self, data):
        if not data:
            return None
        pos_x = data.get("pos_x", 0)
        pos_y = data.get("pos_y", 0)
        if data.get("type") == "rect":
            x, y, w, h = data["x"], data["y"], data["w"], data["h"]
            color = QColor(data["color"])
            item = Rectangle(x, y, w, h)
            item.setBrush(QBrush(color))
            item.setPos(pos_x, pos_y)
            return item
        if data.get("type") == "ellipse":
            x, y, w, h = data["x"], data["y"], data["w"], data["h"]
            color = QColor(data["color"])
            item = Ellipse(x, y, w, h)
            item.setBrush(QBrush(color))
            item.setPos(pos_x, pos_y)
            return item
        if data.get("type") == "triangle":
            x, y, w, h = data["x"], data["y"], data["w"], data["h"]
            color = QColor(data["color"])
            item = Triangle(x, y, w, h)
            item.setBrush(QBrush(color))
            item.setPos(pos_x, pos_y)
            return item
        if data.get("type") == "line":
            x1, y1, x2, y2 = data["x1"], data["y1"], data["x2"], data["y2"]
            color = QColor(data["color"])
            item = Line(x1, y1, x2, y2)
            item.setPen(QPen(color))
            item.setPos(pos_x, pos_y)
            return item
        if data.get("type") == "text":
            x, y, w, h = data["x"], data["y"], data["w"], data["h"]
            text = data.get("text", "")
            item = Text(x, y, w, h)
            item.setPlainText(text)
            item.setPos(pos_x, pos_y)
            return item
        if data.get("type") == "image":
            from PyQt6.QtGui import QPixmap
            import base64
            x, y, w, h = data["x"], data["y"], data["w"], data["h"]
            img_b64 = data.get("image_data", "")
            pixmap = QPixmap()
            if img_b64:
                ba = QByteArray.fromBase64(img_b64.encode())
                pixmap.loadFromData(ba, "PNG")
            item = Image(x, y, w, h, pixmap)
            item.setPos(pos_x, pos_y)
            return item
        return None
    
    def print_diagram(self):
        main_window = self.parent()
        if not hasattr(main_window, "view"):
            QMessageBox.information(self, "Print", "Nothing to print.")
            return
        # Hide grid before printing if it exists
        view = getattr(main_window, "view", None)
        view.grid_visible = False

        printer = QPrinter()
        dialog = QPrintDialog(printer, self)
        if dialog.exec():
            painter = QPainter(printer)
            main_window.view.render(painter)
            painter.end()

        # Restore grid visibility
        view.grid_visible = True