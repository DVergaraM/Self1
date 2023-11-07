"Notification Module"
from typing import Any
from itertools import count
from PyQt5.QtGui import QIcon
from PyQt5 import uic

from utils import cwd, SubWindow, elementType
from utils.config import setConfig
from utils.others import get_time
from utils.setters import connect

from logic import database
from logic import MQThread, Thread
from logic.apps import cls as apps


class NotificationMenu(SubWindow):
    """
    Subclass of `SubWindow` that represents the notification menu.

    Args:
        parent (elementType): The parent element of the notification menu.
        icon (QIcon): The icon to be displayed on the notification menu.
        db (database.BrainDatabase): The database object used by the notification menu.
        notifier (MQThread): The message queue thread used by the notification menu.
        startT (Thread): The thread used to start the notification system.
        stopT (MQThread): The message queue thread used to stop the notification system.
        appsMenu (apps.AppsMenu): The apps menu object used by the notification menu.
    """

    def __init__(self, parent: elementType, icon: QIcon, db: database.BrainDatabase, notifier: MQThread,
                 startT: Thread, stopT: MQThread, appsMenu: apps.AppsMenu):
        super().__init__(size=(760, 680))
        self.icon = icon
        self.mp = parent
        self.db = db
        self.notifier = notifier
        self.startT = startT
        self.stopT = stopT
        self.appsMenu = appsMenu
        self.counter = count()
        uic.loadUi(fr"{cwd}logic\notification\notification_menu.ui", self)
        setConfig(self,
                  "Notification Menu", self.icon, (760, 680))
        return None

    def loadShow(self):
        "Loads, connects and shows the buttons with methods"
        connect(self, {
            "start_popups_button": self._start_thread,
            "stop_popups_button": self._stop_popups,
            "exit_button": self.close,
            "apps_button_menu": self.appsMenu.loadShow
        })
        self.show()
        return None

    def _stop_popups(self):
        "Stops Notification System"
        self.stopT.start()
        format_date_all = get_time()
        print(
            f"{format_date_all} - Thread-{next(self.counter)} (stop)")
        self.notifier.exit()
        return None

    def _start_thread(self):
        "Starts Notification System"
        self.notifier()
        self.startT.start()
        return None
