import os
from PyQt5.QtWidgets import QMainWindow, QApplication, QDialog, QMessageBox
from PyQt5.QtCore import QProcess, QTimer
from PyQt5 import uic
from PyQt5.QtGui import QIcon, QPixmap
import PIL.Image as Img
from logic.apps.cls import AppsMenu
from logic.config.cls import ConfigMenu
from logic.create.cls import CreateMenu
from logic.createApps.cls import CreateAppsMenu
from logic.notification.cls import NotificationMenu

from utils import SubWindow
from utils.config import setConfig
from utils.setters import connect
from logic import Notification, Stray, MQThread, run_pending
from logic.login.cls import LoginSystem
from logic.database import Database

cwd = fr"{os.getcwd()}\src\\"
DB_PATH = fr"{cwd}brain_mine.db"


class Gui(QMainWindow):
    def __init__(self) -> None:
        import sys
        super(Gui, self).__init__()
        uic.loadUi(fr'{cwd}main_window.ui', self)
        self.db: Database = Database(DB_PATH)
        self.connection = self.db.connection
        icon, self.title = self.db.get_config()
        Pil = Img.open(icon)
        self.icon: QIcon = QIcon(icon)
        setConfig(self, str(self.title), self.icon, (760, 680))
        self.config_menu = ConfigMenu(self, self.icon, self.db)

        self.notifier = MQThread(run_pending, True)
        self.othread = QProcess()
        self.apps_menu = AppsMenu(self, self.icon, self.db, self.othread)
        self.create_apps_menu = CreateAppsMenu(
            self, self.icon, self.db, self.apps_menu)

        Start_Notifications = Notification(
            self.title, "Pop-Ups", "Notification System ON", icon, duration="short")
        Stop_Notifications = Notification(
            self.title, "Pop-Ups", "Notification System OFF", icon, duration='short')
        self.start_thread = MQThread(Start_Notifications.run, False)
        self.stop_thread = MQThread(Stop_Notifications.run, False)
        self.notification_menu = NotificationMenu(
            self, self.icon, self.db, self.notifier, self.start_thread, self.stop_thread, self.apps_menu)
        self.create_menu = CreateMenu(
            self, self.icon, self.db, self.create_apps_menu)
        connect(self, {
            "notification_menu_button": self.notification_menu.loadShow,
            "apps_menu_button": self.apps_menu.loadShow,
            "exit_button": self.close,
            "create_menu_button": self.create_menu.loadShow,
            "config_button": self.config_menu.loadShow
        })
        self.stray = Stray(str(self.title), Pil, (self.notification_menu._start_thread,
                           self.notification_menu._stop_popups, self.config_menu.loadShow, self.show, self.hide, sys.exit))
        self.stray.create_menu()
        sys.exit()


def msgBox(login: LoginSystem):
    msg = QMessageBox()
    msg.setWindowIcon(login.icon)
    msg.setWindowTitle("System Tray")
    msg.setText("Look at your Task Bar")
    msg.show()
    return msg


def ms(i: int):
    return i*1000


def main(argv: list[str]):
    import sys
    from datetime import datetime
    app: QApplication = QApplication(argv)
    icon = QIcon()
    icon.addPixmap(QPixmap(fr"{cwd}\images\aries.png"),
                   QIcon.Mode.Selected, QIcon.State.On)
    app.setWindowIcon(icon)
    app.setDesktopFileName("Second Brain")
    app.setQuitOnLastWindowClosed(True)
    login = LoginSystem()
    if login.exec_() == QDialog.DialogCode.Accepted:
        date = datetime.now()
        print(
            f"[{date.day}-{date.month}-{date.year} {date.hour}:{date.minute}:{date.second}] - Opening Stray...")

        msg = msgBox(login)
        QTimer.singleShot(ms(3), lambda: msg.done(0))
        gui = Gui()
        sys.exit(app.exec_())


if __name__ == '__main__':
    import sys
    main(sys.argv[1:])
