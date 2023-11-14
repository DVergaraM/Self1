"Create Menu Module"
# pylint: disable=invalid-name
# pylint: disable=no-name-in-module
# pylint: disable=import-error
from PyQt5.QtGui import QIcon
from PyQt5 import uic

from utils import cwd, SubWindow, ElementType
from utils.config import set_config
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

    def __init__(self, parent: ElementType, icon: QIcon, database: l_database.BrainDatabase,
                 create_app: createApps.CreateAppsMenu):
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
        # pylint: disable=invalid-name
        self.createApps = create_app
        uic.loadUi(fr"{cwd}logic\create\create_menu.ui", self)
        set_config(self,
                   "Notification Menu", self.icon, (760, 680))

    # pylint: disable=invalid-name
    def loadShow(self):
        """
        Loads the GUI, connects buttons with methods, and shows the window.
        """
        connect(self, {
            "exit_button": self.close,
            "create_apps_menu": self.createApps.loadShow
        })
        self.show()

    def add_to_db(self):
        """
        Adds the current instance of the App class to the database.
        """
        # TODO: Create the logic part to save apps to database in the App table
