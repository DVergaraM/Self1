from typing import Callable, Any
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
from winotify import audio as sounds
import schedule as _schedule
import PIL.Image as Img

from logic.login import cls as login
from utils.others import get_time


class Notification(_Notifier):
    "Subclass of `winotify.Notification`"

    def __init__(self, app_id: str = "Second Brain", title: str = "Notifier",
                 msg: str = "", icon: str = "", launch: str | Callable | None = "",
                 duration='long', sound=sounds.Reminder) -> None:
        super().__init__(app_id, title, msg, icon, duration)
        self.set_audio(sound, loop=False)
        if launch is not None:
            self.add_actions("Click Here!", launch)

    def run(self) -> None:
        "Shows Notification with log"
        self.show()
        format_date_all = get_time()
        print(f"{format_date_all} - Task: '{self.msg}'")


class Schedule:
    """
    Class that allows the user to schedule tasks according to a time and timezone
    """

    def __init__(self, timezone: str | pytz.BaseTzInfo = "America/Bogota") -> None:
        '''

        Args:
            timezone (str, pytz.BaseTzInfo, opt): Current timezone. Defaults to`America/Bogota`.
        '''
        if isinstance(timezone, str):
            self.timezone = pytz.timezone(timezone)  # type: ignore
        elif isinstance(timezone, pytz.BaseTzInfo):
            self.timezone = timezone
        else:
            raise ValueError(
                "'timezone' is not an instance of str or pytz.BaseTzInfo")

    def add_task(self, time: str, method: Callable, args: tuple[Any] = (...)):
        '''Adds a task to the schedule

        Args:
            time (str): Time where the method will be executed
            method (Callable): Instance of the method
            args (tuple[Any], optional): Arguments to be used in the method.
        '''
        _schedule.every().day.at(time, self.timezone).do(method, args)

    @staticmethod
    def start():
        "Runs the tasks that are pending."
        _schedule.run_pending()

    @staticmethod
    def stop():
        "Clears the tasks in Queue"
        _schedule.clear()


class MQThread(QThread):
    "Subclass of `PyQt5.QtCore.QThread`"

    def __init__(self, targets: Callable[[], Any] | tuple[Callable[[], Any]],
                 bucles: bool | tuple[bool]) -> None:
        super().__init__()
        self.is_tuple = False
        if isinstance(targets, Callable) and isinstance(bucles, bool):
            self.target = targets
            self.name = targets.__name__
            self.is_tuple = False
            self.bucle = bucles
        elif isinstance(targets, tuple) and isinstance(bucles, tuple) and\
            (isinstance(target, Callable) for target in targets) and\
                (isinstance(bucle, bool) for bucle in bucles):
            self.targets = targets
            self.names: tuple[str] = tuple()
            for target in targets:
                self.names += (target.__name__, )
            self.is_tuple = True
            self.bucles = bucles
        self.counter = count()

    def run(self) -> None:
        "Runs the target(s) method(s) according to some variables initialized in __init__"
        if not self.is_tuple:
            if self.bucle:
                if self.target:
                    format_date_all = get_time()
                    condition = (self.name if self.name != '' else
                                 f'Thread {next(self.counter)} (run)')
                    print(
                        f"{format_date_all} - {condition}")

                    while not self.isFinished():
                        self.target()
            else:
                if self.target:
                    format_date_all = get_time()
                    condition = (self.name if self.name != '' else
                                 f'Thread {next(self.counter)} (run)')
                    print(
                        f"{format_date_all} - {condition}")

                    self.target()
        else:
            for bucle in self.bucles:
                for target in self.targets:
                    if bucle:
                        if target:
                            for name in self.names:
                                format_date_all = get_time()
                                print(
                                    f"{format_date_all} - {name} (run)")
                                while not self.isFinished():
                                    target()
                    else:
                        if target:
                            for name in self.names:
                                format_date_all = get_time()
                                print(
                                    f"{format_date_all} - {name} (run)")
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
        self.icon = Icon(self.title, self.image, menu=Menu(
            Item("Notifier", Menu(
                Item("Start System", self.__helper__),
                Item("Stop System", self.__helper__)
            )),
            Item("Config", self.__helper__),
            Item("Open UI", self.__helper__),
            Item("Close UI", self.__helper__),
            Item("Exit", self.__helper__)
        ), title=self.title)
        self.icon.run()

    def __helper__(self, icon, item):
        notifier_start, notifier_stop, open_config, show_ui, close_ui, icon_exit = self.methods
        item = str(item)
        match item:
            case "Start System":
                format_date_all = self.get_time()
                print(
                    f"{format_date_all} - Starting Notification System")
                notifier_start()
            case "Stop System":
                format_date_all = self.get_time()
                print(
                    f"{format_date_all} - Stopping Notification System")
                notifier_stop()
            case "Config":
                format_date_all = self.get_time()
                print(
                    f"{format_date_all} - Opening Config UI")
                open_config()
            case "Open UI":
                format_date_all = self.get_time()
                print(
                    f"{format_date_all} - Opening UI")
                show_ui()
            case "Close UI":
                format_date_all = self.get_time()
                print(
                    f"{format_date_all} - Closing UI")
                close_ui()
            case "Exit":
                format_date_all = self.get_time()
                print(
                    f"{format_date_all} - Closing {self.icon_name}")
                tm.sleep(5)
                icon.stop()
                icon.exit()

    @staticmethod
    def get_time():
        "Gets the date formatted for easy usage as a print log"
        date = datetime.now()
        format_date = f"[{date.day}-{date.month}-{date.year} "
        format_time = f"{date.hour}:{date.minute}:{date.second}]"
        return format_date + format_time


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
