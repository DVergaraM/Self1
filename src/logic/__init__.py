from pystray import (Menu, MenuItem as Item, Icon)
from winotify import Notification as _Notifier
from winotify import audio as sounds
from datetime import datetime as _datetime
import schedule as _schedule
from typing import Optional, Callable, Any, Union, List, TypeVar, TypeAlias
import os
from datetime import datetime
from PyQt5.QtCore import (QEvent, QThread as QThread, QSize)
from itertools import count
import PIL.Image as Img
import time




db: tuple[tuple[int, str, str, str]] = (
    (1, "https:/i.imgur.com/J6LeoUb.png", "@DVergaraM", "DVergaraM"),
    (2, "https://i.imgur.com/AX1yx9x.png",
     "Programming a Notifier", "Creating a Desktop App"),
    (3, "https://i.imgur.com/6QzKhtx.png", "@dvergaram_", "@dvergaram_")
)


class Notification(_Notifier):
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
    _schedule.run_pending()


def stop() -> None:
    _schedule.clear()


class MQThread(QThread):
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