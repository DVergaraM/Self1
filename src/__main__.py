"Main File of Second Brain"
import os
import sys
from io import BytesIO
from PyQt5.QtWidgets import QMainWindow, QDialog
from PyQt5.QtCore import QProcess, QTimer
from PyQt5 import uic
from PyQt5.QtGui import QIcon, QPixmap, QImage
import PIL.Image as Img
import requests

from logic import Notification, Stray, MQThread, App, msgBox
from logic.database import BrainDatabase
from logic.login.cls import LoginSystem
from logic.apps.cls import AppsMenu
from logic.config.cls import ConfigMenu
from logic.create.cls import CreateMenu
from logic.createApps.cls import CreateAppsMenu
from logic.notification.cls import NotificationMenu
from logic.schedule.cls import ScheduleMenu

from utils.config import set_config
from utils.others import get_time
from utils.setters import connect

cwd = fr"{os.getcwd()}\src\\"
DB_PATH = fr"{cwd}brain_mine.db"


class Gui(QMainWindow):
    """
    Subclass of `PyQt5.QtWidgets.QMainWindow`.
    This class represents the main graphical user interface of the Second Brain application.
    It loads the main GUI, sets the title, icon and fixed size for GUI, creates threads for 
    running executables, creates menus, and makes the connections between buttons and methods.
    """

    def __init__(self) -> None:
        super().__init__()
        # Loads Main GUI
        default = "https://i.imgur.com/PgUSXzh.png"
        uic.loadUi(fr'{cwd}main_window.ui', self)
        self.database = BrainDatabase(DB_PATH)
        self.connection = self.database.connection
        icon, self.__title = None, None
        icon, self.__title = self.database.get_config()
        self.__title = str(self.__title)
        if self.__title and os.path.exists(self.__title):
            self.__title = "Second Brain"
        if icon and os.path.exists(icon):
            pil = Img.open(icon)
            self.icon = QIcon(icon)
            print("With Icon")
        else:
            try:
                default = "https://i.imgur.com/PgUSXzh.png"
                response = requests.get(default, timeout=5000)
                if response.status_code == 200:
                    pil = Img.open(BytesIO(response.content))
                    print(pil.format)
                    if pil.mode != 'RGB':
                        pil = pil.convert('RGB')
                    img = QImage(pil.tobytes(), pil.width,
                                 pil.height, QImage.Format.Format_RGB888)
                    self.icon = QIcon(QPixmap().convertFromImage(img))
                    print("With URL")
                else:
                    pil = Img.open(fr"{os.getcwd()}\assets\default.png")
                    self.icon = QIcon(fr"{os.getcwd()}\assets\default.png")
                    print("With path")
            except requests.ConnectTimeout as excp:
                raise requests.ConnectTimeout(excp) from excp
        # Sets title, icon and fixed size for GUI
        set_config(self, self.title, self.icon, (760, 680))

        # Creates a Windows Pop-Up that displays that the system is on
        start_notifications = Notification(
            self.title, "Pop-Ups", "Notification System ON", icon, duration="short")  # type: ignore
        # Creates a Windows Pop-Up that displays that the system is off
        stop_notifications = Notification(self.title,  # type: ignore
            "Pop-Ups", "Notification System OFF", icon, duration='short')  # type: ignore
        # Thread for running the "Start Notifications" Pop-Up
        start_thread = MQThread(start_notifications.run, False)
        # Thread for running the "Stop Notifications" Pop-Up
        stop_thread = MQThread(stop_notifications.run, False)
        # Creates a Thread for running executables that are in Database
        o_thread = QProcess()

        # Loads Schedule Menu
        self.schedule_menu = ScheduleMenu(
            self, self.icon, self.database, notifier=start_thread)


        # # # # # # # #
        #    Menus    #
        # # # # # # # #

        # Loads Config Menu GUI
        self.config_menu = ConfigMenu(self, self.icon, self.database)
        # Loads Apps Menu GUI
        self.apps_menu = AppsMenu(
            self, self.icon, self.database, o_thread)
        # Loads Create Apps Menu GUI
        self.create_apps_menu = CreateAppsMenu(
            self, self.icon, self.database, self.apps_menu)
        # Loads Notification Menu GUI
        self.notification_menu = NotificationMenu(
            self, self.icon, self.database, start_notifications.run,
            self.schedule_menu.start, stop_thread, self.apps_menu)
        # Loads Create Menu GUI
        self.create_menu = CreateMenu(
            self, self.icon, self.database, self.create_apps_menu)

        # Makes the connections between buttons and methods
        connect(self, {
            "notification_menu_button": self.notification_menu.loadShow,
            "apps_menu_button": self.apps_menu.loadShow,
            "exit_button": self.close,
            "create_menu_button": self.create_menu.loadShow,
            "config_button": self.config_menu.loadShow,
            "schedule_menu_button": self.schedule_menu.loadShow
        })

        # Creates the System Tray [Stray] with some buttons and runs as main thread of the program
        stray = Stray(self.title, pil, (self.schedule_menu.start,  # type: ignore
                                        self.schedule_menu.stop,
                                        self.config_menu.loadShow, self.show,
                                        self.hide, sys.exit))
        stray.create_menu()
        sys.exit()

    @property
    def title(self):
        "Title"
        return self.__title

    def __repr__(self):
        return "Gui()"


def main(argv: list[str]):
    "Main function"
    app = App(argv)
    login = LoginSystem()
    if login.exec_() == QDialog.DialogCode.Accepted:
        format_date_all = get_time()
        print(
            f"{format_date_all} - Opening Stray...")

        msg = msgBox(login)
        QTimer.singleShot(3*1000, lambda: msg.done(0))
        _ = Gui()
        sys.exit(app.exec_())


if __name__ == '__main__':
    main(sys.argv[1:])
