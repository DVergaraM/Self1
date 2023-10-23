from pystray import (Menu, MenuItem as Item, Icon)
from winotify import Notification as _Notifier
from winotify import audio as sounds
from datetime import datetime as _datetime
import schedule as _schedule
from typing import Optional, Callable, Any, Union, List
import os
from datetime import datetime
from PyQt5.QtCore import QThread as QThread
from PyQt5.QtWidgets import QMessageBox, QApplication
from PyQt5.QtGui import QIcon, QPixmap
from itertools import count
import PIL.Image as Img
import time

from logic.login import cls as login


class Notification(_Notifier):
    "Subclass of `winotify.Notification`"
    def __init__(self, app_id: str = "Second Brain", title: str = "Notifier", msg: str = "", icon: str = "", launch: str | Callable | None = "",  duration='long', sound=sounds.Reminder) -> None:
        super().__init__(app_id, title, msg, icon, duration)
        self.set_audio(sound, loop=False)
        if launch is not None:
            self.add_actions("Click Here!", launch)

    def run(self) -> None:
        self.show()
        date = _datetime.now()
        print(f"[{date.day}-{date.month}-{date.year} {date.hour}:{date.minute}:{date.second}] - Task: '{self.msg}'")


class Schedule:
    """
    Class that allows the user to schedule tasks according to a time and timezone
    """
    def __init__(self, time: Union[str, List[str]], task: Union[Callable[[], Any], List[Callable[[], Any]]], tz: Optional[str] = "America/Bogota") -> None:        
        if isinstance(time, str) and isinstance(task, Callable):
            _schedule.every().day.at(time, tz).do(task)
        elif isinstance(time, list) and all(isinstance(t, str) for t in time) and isinstance(task, list) and all(isinstance(t, Callable) for t in task):
            if len(time) == len(task):
                for i in range(len(time)):
                    _schedule.every().day.at(time[i], tz).do(task[i])
            else:
                raise ValueError(
                    "'time' and 'task' params must have the same length of items")
        else:
            raise TypeError(
                "'time' and 'task' params must have the correct type")


def run_pending() -> None:
    "Runs the tasks that are pending."
    _schedule.run_pending()


def stop() -> None:
    "Clears the tasks in Queue"
    _schedule.clear()


class MQThread(QThread):
    "Subclass of `PyQt5.QtCore.QThread`"
    def __init__(self, targets: Callable[[], Any] | tuple[Callable[[], Any]], bucles: bool | tuple[bool]) -> None:
        super().__init__()
        self.isTuple = False
        if isinstance(targets, Callable) and isinstance(bucles, bool):
            self.target = targets
            self.name = targets.__name__
            self.tuple = False
            self.bucle = bucles
        elif isinstance(targets, tuple) and isinstance(bucles, tuple) and (isinstance(target, Callable) for target in targets) and (isinstance(bucle, bool) for bucle in bucles):
            self.targets = targets
            self.names: tuple[str] = tuple()
            for target in targets:
                self.names += (target.__name__, )
            self.isTuple = True
            self.bucles = bucles
        self.counter = count()

    def run(self) -> None:
        "Runs the target(s) method(s) according to some variables initialized in __init__"
        if not self.isTuple:
            if self.bucle:
                if self.target:
                    date = datetime.now()
                    print(
                        f"[{date.day}-{date.month}-{date.year} {date.hour}:{date.minute}:{date.second}] - {(self.name if self.name != '' else f'Thread {next(self.counter)}')} (run)")

                    while not self.isFinished():
                        self.target()
            else:
                if self.target:
                    date = datetime.now()
                    print(
                        f"[{date.day}-{date.month}-{date.year} {date.hour}:{date.minute}:{date.second}] - {(self.name if self.name != '' else f'Thread {next(self.counter)}')} (run)")

                    self.target()
        else:
            for bucle in self.bucles:
                for target in self.targets:
                    if bucle:
                        if target:
                            date = datetime.now()
                            for name in self.names:
                                print(
                                    f"[{date.day}-{date.month}-{date.year} {date.hour}:{date.minute}:{date.second}] - {name} (run)")
                                while not self.isFinished():
                                    target()
                    else:
                        if target:
                            date = datetime.now()
                            for name in self.names:
                                print(
                                    f"[{date.day}-{date.month}-{date.year} {date.hour}:{date.minute}:{date.second}] - {name} (run)")
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
        return self.icon_name

    @title.setter
    def title(self, value: str):
        if isinstance(value, str) and value != self.icon_name:
            self.icon_name = value
        else:
            raise ValueError(
                "'value' is not an instance of str or is the same")

    @property
    def image(self):
        return self._image

    @image.setter
    def image(self, value: Img):
        if isinstance(value, Img) and value != self._image:
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
        notifier_start, notifier_stop, open_config, show_ui, close_ui, exit = self.methods
        item = str(item)
        match item:
            case "Start System":
                date = datetime.now()
                print(
                    f"[{date.day}-{date.month}-{date.year} {date.hour}:{date.minute}:{date.second}] - Starting Notification System")
                notifier_start()
            case "Stop System":
                date = datetime.now()
                print(
                    f"[{date.day}-{date.month}-{date.year} {date.hour}:{date.minute}:{date.second}] - Stopping Notification System")
                notifier_stop()
            case "Config":
                date = datetime.now()
                print(
                    f"[{date.day}-{date.month}-{date.year} {date.hour}:{date.minute}:{date.second}] - Opening Config UI")
                open_config()
            case "Open UI":
                date = datetime.now()
                print(
                    f"[{date.day}-{date.month}-{date.year} {date.hour}:{date.minute}:{date.second}] - Opening UI")
                show_ui()
            case "Close UI":
                date = datetime.now()
                print(
                    f"[{date.day}-{date.month}-{date.year} {date.hour}:{date.minute}:{date.second}] - Closing UI")
                close_ui()
            case "Exit":
                date = datetime.now()
                print(
                    f"[{date.day}-{date.month}-{date.year} {date.hour}:{date.minute}:{date.second}] - Closing {self.icon_name}")
                time.sleep(5)
                icon.stop()


def msgBox(login: login.LoginSystem):
    """
    Creates a QMessageBox instance with some addons
    """
    msg = QMessageBox()
    msg.setWindowIcon(login.icon)
    msg.setWindowTitle("System Tray")
    msg.setText("Look at your Task Bar")
    msg.show()
    return msg


def App(argv: list[str]):
    """
    Creates a QApplication instance with default values.
    """
    cwdAssets = fr"{os.getcwd()}\assets"
    app = QApplication(argv)
    icon = QIcon()
    icon.addPixmap(QPixmap(fr"{cwdAssets}\default.png"),
                   QIcon.Mode.Selected, QIcon.State.On)
    app.setWindowIcon(icon)
    app.setDesktopFileName("Second Brain")
    app.setQuitOnLastWindowClosed(True)
    return app
