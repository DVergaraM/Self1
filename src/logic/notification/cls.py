"Notification Module"
# pylint: disable=invalid-name
# pylint: disable=no-name-in-module
# pylint: disable=import-error
# pylint: disable=unused-import
# pylint: disable=too-many-arguments
from typing import Callable
from itertools import count
from threading import Thread
from PyQt5.QtGui import QIcon
from PyQt5 import uic

from utils import cwd, SubWindow, ElementType
from utils.config import set_config
from utils.others import get_time
from utils.setters import connect

from logic import database as l_database
from logic import MQThread
from logic.apps import cls as apps


class NotificationMenu(SubWindow):
    """
    Subclass of `SubWindow` that represents the notification menu.

    Args:
        parent (ElementType): The parent element of the notification menu.
        icon (QIcon): The icon to be displayed on the notification menu.
        db (l_database.BrainDatabase): The database object used by the notification menu.
        notifier (MQThread): The message queue thread used by the notification menu.
        start_t (Thread): The thread used to start the notification system.
        stop_t (MQThread): The message queue thread used to stop the notification system.
        apps_menu (apps.AppsMenu): The apps menu object used by the notification menu.
    """

    def __init__(self, parent: ElementType, icon: QIcon,
                 database: l_database.BrainDatabase, notifier: MQThread | Callable,
                 start_t: Thread | MQThread | Callable, stop_t: MQThread, apps_menu: apps.AppsMenu):
        """
        Initialize the NotificationMenu class.
        
        :param parent: The parent element.
        :type parent: ElementType
        :param icon: The icon for the notification menu.
        :type icon: QIcon
        :param database: The BrainDatabase object.
        :type database: l_database.BrainDatabase
        :param notifier: The MQThread or Callable object for notification.
        :type notifier: MQThread | Callable
        :param start_t: The Thread, MQThread, or Callable object for starting the notification.
        :type start_t: Thread | MQThread | Callable
        :param stop_t: The MQThread object for stopping the notification.
        :type stop_t: MQThread
        :param apps_menu: The AppsMenu object.
        :type apps_menu: apps.AppsMenu
        :rtype: None
        """
        super().__init__(size=(760, 680))
        self.icon = icon
        self.my_parent = parent
        self.database = database
        self.notifier = notifier
        self.threads = (start_t, stop_t)
        self.apps_menu = apps_menu
        self.counter = count()
        uic.loadUi(fr"{cwd}logic\notification\notification_menu.ui", self)
        set_config(self,
                   "Notification Menu", self.icon, (760, 680))

    def loadShow(self):
        "Loads, connects and shows the buttons with methods"
        connect(self, {
            "start_popups_button": self.start_thread,
            "stop_popups_button": self._stop_popups,
            "exit_button": self.close,
            "apps_button_menu": self.apps_menu.loadShow
        })
        self.show()

    def _stop_popups(self):
        "Stops Notification System"
        self.threads[1].start()
        format_date_all = get_time()
        print(
            f"{format_date_all} - Thread-{next(self.counter)} (stop)")

    def start_thread(self):
        "Starts Notification System"
        thread = self.threads[0]
        notifier = self.notifier

        if callable(thread):
            thread()
        elif isinstance(thread, (MQThread, Thread)):
            thread.start()
        else:
            raise TypeError(f"Expected MQThread or Thread for start_t, got {type(thread)} instead.")

        if callable(notifier):
            notifier()
        elif isinstance(notifier, (MQThread, Thread)):
            notifier.start()
        else:
            raise TypeError(
                f"Expected MQThread or Thread for notifier, got {type(notifier)} instead.")
