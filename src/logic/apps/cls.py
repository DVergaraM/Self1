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
from utils.others import get_time_log, get_text

from logic import database as l_database


class AppsMenu(SubWindow):
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

    def __init__(self, parent: ElementType, icon: QIcon, database: l_database.BrainDatabase,
                 thread: QProcess):
        """
        Adds a new task to the schedule.

        :param parent: Main instance of the Menu.
        :type parent: ElementType
        :param icon: Icon to be set in the config.
        :type icon: QIcon
        :param database: The BrainDatabase instance used for database operations.
        :type database: l_database.BrainDatabase
        :param thread: The QProcess instance used for running the task.
        :type thread: QProcess
        :rtype: None
        """
        super().__init__(size=(760, 680))
        self.my_parent = parent
        self.database = database
        self.o_thread = thread
        self.connection = self.database.connection
        uic.loadUi(fr"{cwd}logic\apps\apps_menu.ui", self)
        set_config(self, "Apps Menu", icon, (760, 680))
        self.actual = str(self.database.get_current_apps_path_apps()[0])

    def loadShow(self):
        "Loads, connects, sets and show GUI"
        set_text(self, ("path_line", fr'"{self.actual}"'))
        connect(self, {
            "exit_button": self.close,
            "right_button": self.avanzar,
            "left_button": self.retroceder,
            "run_button": self.run,
        })
        self.show()

    def avanzar(self):
        "Loops front through the paths in database and sets it up in QLineEdit"
        with self.connection:
            self.database.right_path()
            self.actual: Any = self.database.get_current_apps_path_apps()[0]
            self.path_line.setText(fr'"{self.actual}"')
            return None

    def retroceder(self):
        "Loops back through the paths in database and sets it up in QLineEdit"
        with self.connection:
            self.database.left_path()
            self.actual: Any = self.database.get_current_apps_path_apps()[0]
            self.path_line.setText(fr'"{self.actual}"')
            return None

    def run(self):
        "Runs the program displayed in QLineEdit"
        text = get_text(self, "path_line")
        path = fr"{text}"
        cwd_log = os.getcwd()
        format_date_all = get_time_log()
        name = path.split("\\")[-1].removesuffix('.exe"').title().strip()
        self.o_thread.setProgram(path)
        if name == "Code":
            self.o_thread.start(self.o_thread.program())
        else:
            self.o_thread.start(self.o_thread.program(), [
                               fr"> {cwd_log}\logs\log-{format_date_all}.log"])
        format_date_all = format_date_all.replace("_", " ")
        print(
            f"[{format_date_all}] - {name} (run)")
