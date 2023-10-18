from typing import Any
from PyQt5.QtGui import QIcon
from PyQt5 import uic

from utils import cwd, SubWindow
from utils.config import setConfig
from utils.setters import connect

from logic import database
from logic.createApps import cls as createApps


class CreateMenu(SubWindow):
    def __init__(self, parent: Any , icon: QIcon, db: database.Database, createApp: createApps.CreateAppsMenu):
        super().__init__(size=(760, 680))
        self.icon = icon
        self.mp = parent
        self.db = db
        self.connection = self.db.connection
        self.createApps = createApp
        uic.loadUi(fr"{cwd}logic\create\create_menu.ui", self)
        setConfig(self,
                  "Notification Menu", self.icon, (760, 680))


    def loadShow(self):
        connect(self, {
            "exit_button": self.close,
            "create_apps_menu": self.createApps.loadShow
        })
        self.show()
