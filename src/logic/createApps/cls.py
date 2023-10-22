from typing import Any
from PyQt5.QtGui import QIcon
from PyQt5 import uic

from utils import cwd, SubWindow
from utils.config import setConfig
from utils.setters import setText, connect
from utils.others import getText, updateWindow

from logic import database
from logic.apps import cls as apps


class CreateAppsMenu(SubWindow):
    "Subclass of `SubWindow`"
    def __init__(self, parent: Any , icon: QIcon, db: database.Database, appsMenu: apps.AppsMenu):
        super().__init__(size=(760, 680))
        self.icon = icon
        self.mp = parent
        self.db = db
        self.appsMenu = appsMenu
        self.connection = self.db.connection
        uic.loadUi(fr"{cwd}logic\createApps\create_apps_menu.ui", self)
        setConfig(self, "Apps Create", self.icon, (760, 680))
        self.actual_name = str(self.db.get_current_apps_name()[0])
        self.actual_path = str(self.db.get_current_apps_path()[0])


    def loadShow(self):
        "Loads, connects buttons with methods, sets text in path lines and shows it"
        setText(self, {
            "name_input": self.actual_name,
            "path_input": self.actual_path
        })
        connect(self, {
            "exit_button": self.close,
            "right_button": self.avanzar,
            "left_button": self.retroceder,
            "add_button": self.add_to_db,
            "delete_button": self.delete_from_db,
            "edit_button": self.update
        })
        self.show()
    
    def avanzar(self):
        "Loops front through the paths in database and sets it up in QLineEdit"
        with self.connection:
            self.db.right_create_apps_menu()
            self.actual_name = str(self.db.get_current_apps_name()[0])
            self.actual_path = str(self.db.get_current_apps_path()[0])
            setText(self, {
                "name_input": self.actual_name,
                "path_input": self.actual_path
            })

    
    def retroceder(self):
        "Loops back through the paths in database and sets it up in QLineEdit"
        with self.connection:
            self.db.left_create_apps_menu()
            self.actual_name = str(self.db.get_current_apps_name()[0])
            self.actual_path = str(self.db.get_current_apps_path()[0])
            setText(self, {
                "name_input": self.actual_name,
                "path_input": self.actual_path
            })
    
    def add_to_db(self):
        "Adds info to database"
        cn = getText(self, "name_input")
        cp = getText(self, "path_input")
        current_name: str = f"{cn}"
        current_path: str = fr"{cp}"
        self.db.create_log_apps(
            (current_name, current_path), self)
        updateWindow(self)
        updateWindow(self.appsMenu)
    
    def delete_from_db(self):
        "Deletes info from database."
        cn = getText(self, "name_input")
        cp = getText(self, "path_input")
        current_name: str = f"{cn}"
        current_path: str = fr"{cp}"
        self.db.delete_log_apps(
            (current_name, current_path), self)
        updateWindow(self)
        updateWindow(self.appsMenu)
        
    def update_from_db(self):
        "Updates info to database"
        cn = getText(self, "name_input")
        cp = getText(self, "path_input")
        current_name: str = f"{cn}"
        current_path: str = fr"{cp}"
        self.db.update_log_apps(
            current_path, current_name, self)
        updateWindow(self)
        updateWindow(self.appsMenu)
    