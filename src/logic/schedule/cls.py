"Schedule Module"
from typing import Any
from PyQt5.QtGui import QIcon
from PyQt5.QtWidgets import QMessageBox
from PyQt5 import uic

from utils import cwd, SubWindow, elementType
from utils.config import setConfig
from utils.others import get_time, getText
from utils.setters import connect, setText

from logic import database
from logic import MQThread
from logic.apps import cls as apps
from logic.schedule.schedule import Schedule as LogicSchedule

class ScheduleMenu(SubWindow):
    """
    Subclass of `SubWindow` that represents a window for managing a schedule of tasks.

    Attributes:
        icon (QIcon): The icon to be displayed in the window title bar.
        mp (elementType): The parent element of the window.
        db (database.BrainDatabase): The database used to store the schedule data.
        schedule (LogicSchedule): The logic component responsible for managing the schedule.

    Methods:
        __init__(self, parent: elementType, icon: QIcon, db: database.BrainDatabase):
            Initializes a new instance of the `ScheduleMenu` class.
        loadShow(self):
            Loads, connects and shows the buttons with methods.
        _add_task(self):
            Adds a task to the schedule.
    """
   
    def __init__(self, parent: elementType, icon: QIcon, db: database.BrainDatabase):
        super().__init__(size=(760, 680))
        self.icon = icon
        self.mp = parent
        self.db = db
        self.schedule = LogicSchedule()
        uic.loadUi(fr"{cwd}logic\schedule\schedule_menu.ui", self)
        setConfig(self, "Schedule Menu", self.icon, (760, 680))

    def loadShow(self):
        "Loads, connects and show the buttons with methods"
        connect(self, {
            "save_button": self._add_task,
            "exit_button": self.close,
        })
        self.show()
        
    def _add_task(self):
        "Adds a task to the schedule"
        time = str(getText(self, "time_input"))
        method = str(getText(self, "url_input"))
        self.schedule.add_task(time, method)
        setText(self, {
            "time_input": "",
            "url_input": ""
        })
        QMessageBox.information(self.mp, "Schedule", "Task saved successfully")
        return None