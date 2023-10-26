"Notification Module"
from datetime import datetime
from typing import Any
from PyQt5.QtGui import QIcon
from PyQt5 import uic

from utils import cwd, SubWindow
from utils.config import setConfig
from utils.others import get_time
from utils.setters import connect

from logic import database
from logic import MQThread
from logic.apps import cls as apps


class NotificationMenu(SubWindow):
    "Subclass of `SubWindow`"

    def __init__(self, parent: Any, icon: QIcon, db: database.Database, notifier: MQThread,
                 startT: MQThread, stopT: MQThread, appsMenu: apps.AppsMenu):
        super().__init__(size=(760, 680))
        self.icon = icon
        self.mp = parent
        self.db = db
        self.connection = self.db.connection
        self.notifier = notifier
        self.startT = startT
        self.stopT = stopT
        self.appsMenu = appsMenu
        uic.loadUi(fr"{cwd}logic\notification\notification_menu.ui", self)
        setConfig(self,
                  "Notification Menu", self.icon, (760, 680))

    def loadShow(self):
        "Loads, connects and shows the buttons with methods"
        connect(self, {
            "start_popups_button": self._start_thread,
            "stop_popups_button": self._stop_popups,
            "exit_button": self.close,
            "apps_button_menu": self.appsMenu.loadShow
        })
        self.show()

    def _stop_popups(self):
        "Stops Notification System"
        self.stopT.start()
        self.notifier.finished = True
        format_date_all = get_time()
        condition = (self.notifier.name if self.notifier.name != '' else
                     f'Thread {next(self.notifier.counter)}')
        print(
            f"{format_date_all} - {condition} (stop)")
        self.notifier.exit()

    def _start_thread(self):
        "Starts Notification System"
        self.notifier.start()
        self.startT.start()
