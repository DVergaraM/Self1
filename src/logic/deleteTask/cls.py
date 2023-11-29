"Apps Menu Module"
# pylint: disable=invalid-name
# pylint: disable=no-name-in-module
# pylint: disable=import-error
import os
from typing import Any
from PyQt5.QtGui import QIcon
from PyQt5.QtCore import QProcess
from PyQt5 import uic

from utils import cwd, SubWindow, ElementType
from utils.config import set_config
from utils.setters import set_text, connect
from utils.others import get_time_log, get_text, update_window

from logic import database as l_database


class DeleteTaskMenu(SubWindow):
    """
    Subclass of `SubWindow` that represents the applications menu window.

    Attributes:
        icon (QIcon): The icon to be displayed in the GUI.
        mp (Any): A reference to the parent object.
        db (l_database.BrainDatabase): The database where the items are stored.
        o_thread (QProcess): The thread where the programs will run from the database.
        connection: The connection to the database.
        actual (str): The current path selected in the database.

    Methods:
        __init__(self, parent: Any, icon: QIcon, database: BrainDatabase, thread: QProcess):
            Initializes the `AppsMenu` object.
        loadShow(self):
            Loads, connects, sets and shows the GUI.
        avanzar(self):
            Loops front through the paths in the database and sets it up in QLineEdit.
        retroceder(self):
            Loops back through the paths in the database and sets it up in QLineEdit.
        run(self):
            Runs the program displayed in QLineEdit.
    """

    def __init__(self, parent: ElementType, icon: QIcon, database: l_database.BrainDatabase):
        """
        Adds a new task to the schedule.

        :param parent: Main instance of the Menu.
        :type parent: ElementType
        :param icon: Icon to be set in the config.
        :type icon: QIcon
        :param database: The BrainDatabase instance used for database operations.
        :type database: l_database.BrainDatabase
        :rtype: None
        """
        super().__init__(size=(760, 680))
        self.my_parent = parent
        self.database = database
        self.connection = self.database.connection
        uic.loadUi(fr"{cwd}logic\deleteTask\delete_task_menu.ui", self)
        set_config(self, "Tasks Menu", icon, (760, 680))
        self.actual_time = str(
            self.database.get_current_delete_task_menu_time()[0])
        self.actual_url = str(
            self.database.get_current_delete_task_menu_url()[0])

    def loadShow(self):
        "Loads, connects, sets and show GUI"
        print("Open")
        set_text(self, {
            "time_line": self.actual_time,
            "url_line": self.actual_url
        })
        connect(self, {
            "exit_button": self.close,
            "right_button": self.avanzar,
            "left_button": self.retroceder,
            "delete_button": self.delete_from_db,
        })
        self.show()

    def avanzar(self):
        "Loops front through the paths in database and sets it up in QLineEdit"
        with self.connection:
            self.database.right_delete_task_menu()
            self.actual_time = str(
                self.database.get_current_delete_task_menu_time()[0])
            self.actual_url = str(
                self.database.get_current_delete_task_menu_url()[0])
            set_text(self, {
                "time_line": self.actual_time,
                "url_line": self.actual_url
            })
        return self.actual_time, self.actual_url

    def retroceder(self):
        "Loops back through the paths in database and sets it up in QLineEdit"
        with self.connection:
            self.database.left_delete_task_menu()
            self.actual_time = str(
                self.database.get_current_delete_task_menu_time()[0])
            self.actual_url = str(
                self.database.get_current_delete_task_menu_url()[0])
            set_text(self, {
                "time_line": self.actual_time,
                "url_line": self.actual_url
            })
        return self.actual_time, self.actual_url

    def delete_from_db(self):
        "Deletes the task displayed in QLineEdit"
        current_time = str(get_text(self, "time_line"))
        cwd = os.getcwd()
        self.database.remove_task(current_time)
        update_window(self)
        self.database = l_database.BrainDatabase(fr"{cwd}\src\brain_mine.db")
        next_time, next_url = self.avanzar()
        set_text(self, {
            "time_line": next_time,
            "url_line": next_url
        })
        update_window(self)
        self.database = l_database.BrainDatabase(fr"{cwd}\src\brain_mine.db")
