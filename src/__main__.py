"Main File of Second Brain"
import os
import sys
from datetime import datetime
from PyQt5.QtWidgets import QMainWindow, QDialog
from PyQt5.QtCore import QProcess, QTimer
from PyQt5 import uic
from PyQt5.QtGui import QIcon, QPixmap
import PIL.Image as Img
import requests

from logic import Notification, Stray, MQThread, run_pending, App, msgBox
from logic.database import Database
from logic.login.cls import LoginSystem
from logic.apps.cls import AppsMenu
from logic.config.cls import ConfigMenu
from logic.create.cls import CreateMenu
from logic.createApps.cls import CreateAppsMenu
from logic.notification.cls import NotificationMenu

from utils.config import setConfig
from utils.setters import connect

cwd = fr"{os.getcwd()}\src\\"
DB_PATH = fr"{cwd}brain_mine.db"


class Gui(QMainWindow):
    "Subclass of `PyQt5.QtWidgets.QMainWindow`"

    def __init__(self) -> None:
        super(Gui, self).__init__()
        # Loads Main GUI
        icon_url = "https://daniel-vergara-m.github.io/images/media/default.png"
        uic.loadUi(fr'{cwd}main_window.ui', self)
        self.database = Database(DB_PATH)
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
                response = requests.get(icon_url, timeout=5000)
                pil = Img.open(response.content)
                pix = QPixmap()
                pix.loadFromData(response.content)
                self.icon = QIcon(pix)
                print("With URL")
            except requests.ConnectTimeout:
                pil = Img.open(fr"{os.getcwd()}\assets\default.png")
                self.icon = QIcon(fr"{os.getcwd()}\assets\default.png")
                print("With path")

        # Sets title, icon and fixed size for GUI
        setConfig(self, self.title, self.icon, (760, 680))

        # # # # # # # #
        #   Threads   #
        # # # # # # # #

        # Creates a Thread for 'run_pending' method with a while loop
        self.notifier = MQThread(run_pending, True)
        # Creates a Windows Pop-Up that displays that the system is on
        start_notifications = Notification(
            self.title, "Pop-Ups", "Notification System ON", icon, duration="short")
        # Creates a Windows Pop-Up that displays that the system is off
        stop_notifications = Notification(
            self.title, "Pop-Ups", "Notification System OFF", icon, duration='short')
        # Thread for running the "Start Notifications" Pop-Up
        self.start_thread = MQThread(start_notifications.run, False)
        # Thread for running the "Stop Notifications" Pop-Up
        self.stop_thread = MQThread(stop_notifications.run, False)
        # Creates a Thread for running executables that are in Database
        self.othread = QProcess()

        # # # # # # # #
        #    Menus    #
        # # # # # # # #

        # Loads Config Menu GUI
        self.config_menu = ConfigMenu(self, self.icon, self.database)
        # Loads Apps Menu GUI
        self.apps_menu = AppsMenu(self, self.icon, self.database, self.othread)
        # Loads Create Apps Menu GUI
        self.create_apps_menu = CreateAppsMenu(
            self, self.icon, self.database, self.apps_menu)
        # Loads Notification Menu GUI
        self.notification_menu = NotificationMenu(
            self, self.icon, self.database, self.notifier,
            self.start_thread, self.stop_thread, self.apps_menu)
        # Loads Create Menu GUI
        self.create_menu = CreateMenu(
            self, self.icon, self.database, self.create_apps_menu)

        # Makes the connections between buttons and methods
        connect(self, {
            "notification_menu_button": self.notification_menu.loadShow,
            "apps_menu_button": self.apps_menu.loadShow,
            "exit_button": self.close,
            "create_menu_button": self.create_menu.loadShow,
            "config_button": self.config_menu.loadShow
        })

        # Creates the System Tray [Stray] with some buttons and runs as main thread of the program
        stray = Stray(self.title, pil, (self.notification_menu._start_thread,
                                        self.notification_menu._stop_popups,
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
        date = datetime.now()
        format_date = f"[{date.day}-{date.month}-{date.year} "
        format_time = f"{date.hour}:{date.minute}:{date.second}]"
        format_date_all = format_date + format_time
        print(
            f"{format_date_all} - Opening Stray...")

        msg = msgBox(login)
        QTimer.singleShot(3*1000, lambda: msg.done(0))
        gui = Gui()
        sys.exit(app.exec_())


if __name__ == '__main__':
    main(sys.argv[1:])
