from typing import Any
from PyQt5.QtGui import QIcon
from PyQt5 import uic

from utils import cwd, SubWindow
from utils.config import setConfig
from utils.setters import connect

from logic import database
from logic.createApps import cls as createApps


class CreateMenu(SubWindow):
    "Subclass of `SubWindow`"
    def __init__(self, parent: Any , icon: QIcon, db: database.BrainDatabase,
                 createApp: createApps.CreateAppsMenu):
        '''

        Args:
            parent (Self): Different of of `self` but to implement inside other class with `self`
            icon (QIcon): Icon to be setted up in the GUI
            db (database.Database): Db where is going to look for items
            createApp (createApps.CreateAppsMenu): Menu for saving apps to database
        '''
        super().__init__(size=(760, 680))
        self.icon = icon
        self.mp = parent
        self.db = db
        self.createApps = createApp
        uic.loadUi(fr"{cwd}logic\create\create_menu.ui", self)
        setConfig(self,
                  "Notification Menu", self.icon, (760, 680))


    def loadShow(self):
        "Loads, connects buttons with methods and shows GUI"
        connect(self, {
            "exit_button": self.close,
            "create_apps_menu": self.createApps.loadShow
        })
        self.show()
