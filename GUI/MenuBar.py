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
        edit_menu.addAction("Undo")
        edit_menu.addAction("Redo")
        edit_menu.addSeparator()
        edit_menu.addAction("Cut")
        edit_menu.addAction("Copy")
        edit_menu.addAction("Paste")

        # Help Menu
        help_menu = self.addMenu("Help")
        help_menu.addAction("About")