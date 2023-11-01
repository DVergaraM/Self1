from typing import Callable, Any, Iterator, Union, Tuple
import os
from datetime import datetime
from itertools import count
import time as tm
from PyQt5.QtCore import QThread
from PyQt5.QtWidgets import QMessageBox, QApplication
from PyQt5.QtGui import QIcon, QPixmap
from pystray import (Menu, MenuItem as Item, Icon)
import pytz
from winotify import Notification as _Notifier
from winotify import audio
import schedule as _schedule
import PIL.Image as Img
from threading import Thread

from logic.login import cls as login
from utils.others import get_time


class Notification(_Notifier):
    """
    Subclass of `winotify.Notification`.

    Args:
        app_id (str): The ID of the application sending the notification.
        title (str): The title of the notification.
        msg (str): The message to display in the notification.
        icon (str): The path to the icon to display in the notification.
        launch (str | Callable | None): The action to take when the notification is clicked.
        duration (str): The duration for which to display the notification.
        sound (audio.Sound): The sound to play when the notification is displayed.

    Attributes:
        app_id (str): The ID of the application sending the notification.
        title (str): The title of the notification.
        msg (str): The message to display in the notification.
        icon (str): The path to the icon to display in the notification.
        launch (str | Callable | None): The action to take when the notification is clicked.
        duration (str): The duration for which to display the notification.
        sound (audio.Sound): The sound to play when the notification is displayed.

    Methods:
        run(): Shows Notification with log.
    """
    def __init__(self, app_id: str = "Second Brain", title: str = "Notifier",
                 msg: str = "", icon: str = "", launch: str | Callable | None = None,
                 duration='long', sound: audio.Sound = audio.Reminder) -> None:
        super().__init__(app_id, title, msg, icon, duration)
        self.set_audio(sound, loop=False)
        if launch is not None:
            self.add_actions("Click Here!", launch)

    def run(self) -> None:
        "Shows Notification with log"
        self.show()
        format_date_all = get_time()
        print(f"{format_date_all} - Task: '{self.msg}'")
        return None


class MQThread(QThread):
    """
    Subclass of `PyQt5.QtCore.QThread`
    A subclass of `PyQt5.QtCore.QThread` that allows for running one or more target methods in a loop or once.

    :param targets: A callable or a tuple of callables to be run.
    :type targets: Callable[[], Any] | tuple[Callable[[], Any]]
    :param bucles: A boolean or a tuple of booleans indicating whether each target should be run in a loop or once.
    :type bucles: bool | tuple[bool]
    """

    def __init__(self, targets: Callable[[], Any] | tuple[Callable[[], Any]],
                 bucles: bool | tuple[bool]):
        super().__init__()
        self.is_tuple = False
        if isinstance(targets, Callable) and isinstance(bucles, bool):
            self.targets = (targets,)
            self.names = (targets.__name__,)
            self.bucles = (bucles,)
        elif isinstance(targets, tuple) and isinstance(bucles, tuple) and all(isinstance(target, Callable) for target in targets) and all(isinstance(bucle, bool) for bucle in bucles):
            self.targets = targets
            self.names = tuple(target.__name__ for target in targets)
            self.bucles = bucles
            self.is_tuple = True
        else:
            raise TypeError(
                "'targets' must be a callable or a tuple of callables, and 'bucles' must be a bool or a tuple of bools")
        self.counter = count()

    def run(self):
            """
            Runs the target(s) method(s) according to some variables initialized in __init__

            Loops through the targets and names, and if the corresponding bucle is True, runs the target method in a loop
            until the isFinished method returns True. Otherwise, runs the target method once.
            """
            for bucle, target, name in zip(self.bucles, self.targets, self.names):
                if bucle:
                    format_date_all = get_time()
                    print(f"{format_date_all} - {name} (run)")
                    while not self.isFinished():
                        target()
                else:
                    format_date_all = get_time()
                    print(f"{format_date_all} - {name} (run)")
                    target()


class Stray:
    "This class slows the user to create a Windows Stray Icon with some methods, icon and title"

    def __init__(self, icon_name: str, image: Img, methods: tuple[Callable, ...]):
        self.icon_name = icon_name
        self._image = image
        self.methods = methods
        self.icon = None

    @property
    def title(self):
        "Title"
        return self.icon_name

    @title.setter
    def title(self, value: str):
        "Title setter"
        if isinstance(value, str) and value != self.icon_name:
            self.icon_name = value
        else:
            raise ValueError(
                "'value' is not an instance of str or is the same")

    @property
    def image(self):
        "Image property"
        return self._image

    @image.setter
    def image(self, value):
        if isinstance(value, Img.Image) and value != self._image:
            self._image = value
        else:
            raise ValueError(
                "'value' is not an instance of PIL.Image or is the same")

    def create_menu(self):
        "Creates the menu for the Stray with some buttons and run it"
        menu = Menu(
            Item("Notifier", Menu(
                Item("Start System", self.__helper__),
                Item("Stop System", self.__helper__)
            )),
            Item("Config", self.__helper__),
            Item("Open UI", self.__helper__),
            Item("Close UI", self.__helper__),
            Item("Exit", self.__helper__)
        )
        self.icon = Icon(self.title, self.image, menu=menu, title=self.title)
        self.icon.run()

    def __helper__(self, icon, item):
        notifier_start, notifier_stop, open_config, show_ui, close_ui, *_ = self.methods
        item = str(item)
        match item:
            case "Start System":
                format_date_all = get_time()
                print(
                    f"{format_date_all} - Starting Notification System")
                notifier_start()
            case "Stop System":
                format_date_all = get_time()
                print(
                    f"{format_date_all} - Stopping Notification System")
                notifier_stop()
            case "Config":
                format_date_all = get_time()
                print(
                    f"{format_date_all} - Opening Config UI")
                open_config()
            case "Open UI":
                format_date_all = get_time()
                print(
                    f"{format_date_all} - Opening UI")
                show_ui()
            case "Close UI":
                format_date_all = get_time()
                print(
                    f"{format_date_all} - Closing UI")
                close_ui()
            case "Exit":
                format_date_all = get_time()
                print(
                    f"{format_date_all} - Closing {self.icon_name}")
                tm.sleep(5)
                icon.stop()


def msgBox(log: login.LoginSystem):
    """
    Creates a QMessageBox instance with some addons
    """
    msg = QMessageBox()
    msg.setWindowIcon(log.icon)
    msg.setWindowTitle("System Tray")
    msg.setText("Look at your Task Bar")
    msg.show()
    return msg


def App(argv: list[str]):
    """
    Creates a QApplication instance with default values.
    """
    cwd_assets = fr"{os.getcwd()}\assets"
    app = QApplication(argv)
    icon = QIcon()
    icon.addPixmap(QPixmap(fr"{cwd_assets}\default.png"),
                   QIcon.Mode.Selected, QIcon.State.On)
    app.setWindowIcon(icon)
    app.setDesktopFileName("Second Brain")
    app.setQuitOnLastWindowClosed(True)
    return app
