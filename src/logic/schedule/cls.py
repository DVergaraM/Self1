"Schedule Module"
# pylint: disable=invalid-name
# pylint: disable=no-name-in-module
# pylint: disable=import-error
from collections import deque
from PyQt5.QtGui import QIcon
from PyQt5.QtCore import QEvent
from PyQt5 import uic

from utils import cwd, SubWindow, ElementType
from utils.config import set_config
from utils.others import get_text, get_time_status
from utils.setters import connect, set_text

from logic import (MQThread, database as l_database)
from logic.deleteTask.cls import DeleteTaskMenu as Manager
from logic.schedule.schedule import Schedule as LogicSchedule


class ScheduleMenu(SubWindow):
    """
    Subclass of `SubWindow` that represents a window for managing a schedule of tasks.

    Attributes:
        icon (QIcon): The icon to be displayed in the window title bar.
        mp (ElementType): The parent element of the window.
        db (l_database.BrainDatabase): The database used to store the schedule data.
        schedule (LogicSchedule): The logic component responsible for managing the schedule.

    Methods:
        __init__(self, parent: ElementType, icon: QIcon, database: l_database.BrainDatabase):
            Initializes a new instance of the `ScheduleMenu` class.
        loadShow(self):
            Loads, connects and shows the buttons with methods.
        _add_task(self):
            Adds a task to the schedule.
    """
    _running = False

    def __init__(self, parent: ElementType, icon: QIcon,
                 database: l_database.BrainDatabase, manager: Manager, **kwargs):
        """
        Initializes an instance of the class.

        :param parent: The parent element.
        :type parent: ElementType
        :param icon: The icon.
        :type icon: QIcon
        :param database: The database.
        :type database: l_database.BrainDatabase
        :param kwargs: Additional keyword arguments.
        :type kwargs: dict
        :rtype: None
        """
        super().__init__(size=(760, 680))
        self.icon = icon
        notifier = kwargs["notifier"] if "notifier" in kwargs else None
        start_thread = kwargs["start_thread"] if "start_thread" in kwargs else None
        self.database = database
        self.manager = manager
        self.schedule = LogicSchedule(
            notifier=notifier, start_thread=start_thread, database=database, parent=parent)
        self._thread = MQThread(self.schedule.start, False)
        self.load_tasks()
        uic.loadUi(fr"{cwd}logic\schedule\schedule_menu.ui", self)
        set_config(self, "Schedule Menu", self.icon, (760, 680))

    def loadShow(self):
        "Loads, connects and show the buttons with methods"
        connect(self, {
            "save_button": self._add_task,
            "exit_button": self.close,
            "delete_menu_button": self.open_manager
        })
        self.show()

    def _add_task(self):
        "Adds a task to the schedule"
        time = str(get_text(self, "time_input"))
        method = str(get_text(self, "url_input"))
        self.schedule.add_task_to_db(time, method)
        set_text(self, {
            "time_input": "",
            "url_input": ""
        })

    def start(self):
        """
        Starts the thread and sets the running flag to True.
        """
        self._thread.start()
        self._running = True

    def stop(self):
        """
        Stops the schedule if it is running.
        """
        if self._running:
            self._running = False
            self.schedule.stop()  # type: ignore

    def load_tasks(self):
        """
        Loads the tasks from the database.
        """
        tasks = deque(self.schedule.database.fetch_all_tasks()) # type: ignore
        for task in tasks:
            self.schedule.add_task(task[0], task[1])
        print(f"{get_time_status('INFO | Schedule')} - Tasks loaded")

    def _closeEvent(self, event: QEvent):
        """
        Overrides the `closeEvent` method of the `QWidget` class.

        :param event: The event.
        :type event: QCloseEvent
        :rtype: None
        """
        self.stop()
        self._thread.wait()
        event.accept()

    def open_manager(self):
        "Opens Tasks Manager"
        self.manager.loadShow()
