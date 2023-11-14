"CreateApps Module"
from typing import Any
from PyQt5.QtGui import QIcon
from PyQt5 import uic

from utils import cwd, SubWindow, elementType
from utils.config import setConfig
from utils.setters import setText, connect
from utils.others import getText, updateWindow

from logic import database as l_database
from logic.apps import cls as apps


class CreateAppsMenu(SubWindow):
    """
    Subclass of `SubWindow` that represents a window for creating and managing applications.

    Attributes:
    - icon (QIcon): The icon for the window.
    - mp (Any): The parent object of the window.
    - db (l_database.BrainDatabase): The database object used for storing application information.
    - appsMenu (apps.AppsMenu): The `AppsMenu` object that this window is associated with.
    - actual_name (str): The current name of the application being displayed.
    - actual_path (str): The current path of the application being displayed.
    """

    def __init__(self, parent: elementType, icon: QIcon, database: l_database.BrainDatabase, appsMenu: apps.AppsMenu):
        super().__init__(size=(760, 680))
        self.icon = icon
        self.my_parent = parent
        self.database = database
        self.appsMenu = appsMenu
        uic.loadUi(fr"{cwd}logic\createApps\create_apps_menu.ui", self)
        setConfig(self, "Apps Create", self.icon, (760, 680))
        self.actual_name = str(self.database.get_current_apps_name()[0])
        self.actual_path = str(self.database.get_current_apps_path()[0])
        return None

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
        return None

    def avanzar(self):
        "Loops front through the paths in database and sets it up in QLineEdit"
        with self.connection:
            self.database.right_create_apps_menu()
            self.actual_name = str(self.database.get_current_apps_name()[0])
            self.actual_path = str(self.database.get_current_apps_path()[0])
            setText(self, {
                "name_input": self.actual_name,
                "path_input": self.actual_path
            })

    def retroceder(self):
        "Loops back through the paths in database and sets it up in QLineEdit"
        with self.connection:
            self.database.left_create_apps_menu()
            self.actual_name = str(self.database.get_current_apps_name()[0])
            self.actual_path = str(self.database.get_current_apps_path()[0])
            setText(self, {
                "name_input": self.actual_name,
                "path_input": self.actual_path
            })

    def add_to_db(self):
        "Adds info to database"
        current_name = getText(self, "name_input") # type: ignore
        current_path = getText(self, "path_input") # type: ignore
        current_name: str = f"{current_name}"
        current_path: str = fr"{current_path}"
        self.database.create_log_apps(
            (current_name, current_path), self) # type: ignore
        updateWindow(self)
        updateWindow(self.appsMenu)
        return None

    def delete_from_db(self):
        "Deletes info from database."
        current_name = getText(self, "name_input") # type: ignore
        current_path = getText(self, "path_input") # type: ignore
        current_name: str = f"{current_name}"
        current_path: str = fr"{current_path}"
        self.database.delete_log_apps(
            (current_name, current_path), self)
        updateWindow(self)
        updateWindow(self.appsMenu)
        return None

    def update_from_db(self):
        "Updates info to database"
        current_name = getText(self, "name_input") # type: ignore
        current_path = getText(self, "path_input") # type: ignore
        current_name: str = f"{current_name}"
        current_path: str = fr"{current_path}"
        self.database.update_log_apps(
            current_path, current_name, self)
        updateWindow(self)
        updateWindow(self.appsMenu)
        return None
