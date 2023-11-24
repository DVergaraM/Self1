"Schedule Module"
# pylint: disable=invalid-name
# pylint: disable=no-name-in-module
# pylint: disable=import-error
from PyQt5.QtGui import QIcon
from PyQt5.QtWidgets import QMessageBox
from PyQt5 import uic

from utils import cwd, SubWindow, ElementType
from utils.config import set_config
from utils.others import get_text
from utils.setters import connect, set_text

from logic import database as l_database
from logic import MQThread
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
                 database: l_database.BrainDatabase, **kwargs):
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
        self.my_parent = parent
        self.database = database
        notifier = kwargs["notifier"] if "notifier" in kwargs else None
        start_thread = kwargs["start_thread"] if "start_thread" in kwargs else None
        self.schedule = LogicSchedule(
            notifier=notifier, start_thread=start_thread)
        self._thread = MQThread(self.schedule.start, False)  # type: ignore
        uic.loadUi(fr"{cwd}logic\schedule\schedule_menu.ui", self)
        set_config(self, "Schedule Menu", self.icon, (760, 680))

    # pylint: disable=invalid-name
    def loadShow(self):
        "Loads, connects and show the buttons with methods"
        connect(self, {
            "save_button": self._add_task,
            "exit_button": self.close,
        })
        self.show()

    def _add_task(self):
        "Adds a task to the schedule"
        time = str(get_text(self, "time_input"))
        method = str(get_text(self, "url_input"))
        self.schedule.add_task(time, method)
        set_text(self, {
            "time_input": "",
            "url_input": ""
        })
        QMessageBox.information(self, "Schedule", "Task saved successfully")

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
            self.schedule.stop() # type: ignore
