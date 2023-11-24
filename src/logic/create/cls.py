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

        :param parent: A reference to the parent object.
        :type parent: ElementType
        :param icon: The icon to be displayed in the GUI.
        :type icon: QIcon
        :param database: The database where items will be stored.
        :type database: l_database.BrainDatabase
        :param create_app: A menu for saving apps to the database.
        :type create_app: createApps.CreateAppsMenu
        :rtype: None
        """
        super().__init__(size=(760, 680))
        self.icon = icon
        self._my_parent = parent
        self.database = database
        self.createApps = create_app
        uic.loadUi(fr"{cwd}logic\create\create_menu.ui", self)
        set_config(self,
                   "Notification Menu", self.icon, (760, 680))

    def loadShow(self):
        """
        Loads the GUI, connects buttons with methods, and shows the window.
        """
        connect(self, {
            "exit_button": self.close,
            "create_apps_menu": self.createApps.loadShow
        })
        self.show()

    @property
    def my_parent(self):
        "Returns the parent of the current instance"
        return self._my_parent
