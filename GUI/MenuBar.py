from PyQt6.QtWidgets import *
from PyQt6.QtCore import *
from PyQt6.QtGui import *
from GUI.GridScene import *

class MenuBar(QMenuBar):
    def __init__(self, parent=None):
        super().__init__(parent)

        # File Menu
        file_menu = self.addMenu("File")
        file_menu.addAction("New")
        file_menu.addAction("Open")
        file_menu.addAction("Save")
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