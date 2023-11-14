from typing import Any
from PyQt5.QtGui import QIcon
from PyQt5 import uic

from utils import cwd, SubWindow, elementType
from utils.config import setConfig
from utils.setters import connect

from logic import database as l_database
from logic.createApps import cls as createApps


class CreateMenu(SubWindow):
    """
    A subclass of `SubWindow` that represents a GUI window for creating new items.

    Attributes:
        icon (QIcon): The icon to be displayed in the GUI.
        mp (Any): A reference to the parent object.
        db (l_database.BrainDatabase): The database where items will be stored.
        createApps (createApps.CreateAppsMenu): A menu for saving apps to the database.
    """

    def __init__(self, parent: elementType, icon: QIcon, database: l_database.BrainDatabase,
                 createApp: createApps.CreateAppsMenu):
        """
        Initializes a new instance of the `CreateMenu` class.

        Args:
            parent (Any): A reference to the parent object.
            icon (QIcon): The icon to be displayed in the GUI.
            db (l_database.BrainDatabase): The database where items will be stored.
            createApp (createApps.CreateAppsMenu): A menu for saving apps to the database.
        """
        super().__init__(size=(760, 680))
        self.icon = icon
        self.my_parent = parent
        self.database = database
        self.createApps = createApp
        uic.loadUi(fr"{cwd}logic\create\create_menu.ui", self)
        setConfig(self,
                  "Notification Menu", self.icon, (760, 680))
        return None

    def loadShow(self):
        """
        Loads the GUI, connects buttons with methods, and shows the window.
        """
        connect(self, {
            "exit_button": self.close,
            "create_apps_menu": self.createApps.loadShow
        })
        self.show()
        return None
    