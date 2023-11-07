import os
from typing import Any
from PyQt5.QtGui import QIcon, QImageReader
from PyQt5.QtWidgets import QFileDialog, QMessageBox
from PyQt5 import uic

from utils import cwd, SubWindow, elementType, props
from utils.config import setConfig, setMultipleConfig
from utils.setters import setText, textChangedConnect, connect, enableButton
from utils.others import updateWindow, getText, remove

from logic import database


class ConfigMenu(SubWindow):
    """
    A subwindow for configuring the application's settings.

    Args:
        parent (Any): The parent widget.
        icon (QIcon): The icon to be displayed in the GUI.
        db (database.BrainDatabase): The database where the items are stored.
    """

    def __init__(self, parent: elementType, icon: QIcon, db: database.BrainDatabase):
        '''
        Initializes the ConfigMenu class.
        '''
        super().__init__(size=(510, 460))
        self.icon = icon
        self.mp = parent
        self.database = db
        self._config = ()
        self.image_path = str()
        uic.loadUi(fr"{cwd}logic\config\config_menu.ui", self)
        setConfig(self, "Config Menu", self.icon)

    def loadShow(self):
        "Loads, connects buttons with methods and shows GUI"
        textChangedConnect(self, {
            self.validate_all: [
                "title_input",
                "path_input"
            ]
        })
        connect(self, {
            "browse_button": self.browse_icon,
            "save_title_button": self.save_title,
            "save_all_button": self.add_to_db,
            "exit_button": self.close
        })
        self._config = ()
        self.show()

    def validate_all(self):
        if all([getText(self, "title_input") != "", getText(self, "path_input") != ""]):
            enableButton(self, {"save_all_button": True})
        else:
            enableButton(self, {"save_all_button": False})
        updateWindow(self)

    def browse_icon(self):
        "Looks for an image to set up as App Icon"
        realpath = os.path.realpath("C:/Users")
        supportedFormats = QImageReader.supportedImageFormats()
        formats = []
        for sF in supportedFormats:
            formats.append(f"*.{sF.data().decode()}")
        formatted = " ".join(formats)
        text_filter = f"Images ({formatted})"
        self.image_path, _ = QFileDialog.getOpenFileName(
            self, "Open an image", realpath, text_filter)
        if (len(self._config) % 2 == 1 or len(self._config) >= 3) and self.image_path != "":
            self._config = remove(self._config)
            self._config += (self.image_path, )
            print(self._config)
        else:
            self._config = ()
            self._config += (self.image_path, )
            print(self._config)
        setText(self, {"path_input": self.image_path})
        updateWindow(self)
        print(self._config)

    def save_title(self):
        "Saves the title displayed in QLineEdit"
        title = str(getText(self, "title_input"))
        if (len(self._config) % 2 == 1 or len(self._config) >= 3) and\
                title != "" and os.path.exists(self._config[0]):
            self._config = remove(self._config)
            self._config += (title, )
            print(self._config)
        else:
            self._config = ()
            self._config += (self.image_path, title)
            print(self._config)
        updateWindow(self)
        print(self._config)

    def add_to_db(self):
        """Adds the information to Database and 
        raises ValueError if the config length is different of 2"""
        self._config = remove(self._config)
        if len(self._config) == 2:
            self.database.delete_config()
            self.database.set_config(self, self._config)
            icon, title = self.database.get_config()
            icon = QIcon(icon)
            properties = props(self.mp)
            menus = [obj for obj in properties if "menu" in obj]
            print(menus)
            for menu in menus:
                obj = getattr(self.mp, menu)
                setConfig(obj)
            print("Config setted for all windows")
            # setMultipleConfig(
            #    (self.mp, self, self.mp.apps_menu, self.mp.create_menu,
            #     self.mp.create_apps_menu, self.mp.apps_menu, self.mp.notification_menu, self.mp.schedule_menu),
            #    (str(title), self.mp.config_menu.windowTitle(), self.mp.apps_menu.windowTitle(), self.mp.create_menu.windowTitle(
            #    ), self.mp.create_apps_menu.windowTitle(), self.mp.apps_menu.windowTitle(), self.mp.notification_menu.windowTitle(), self.mp.schedule_menu.windowTitle()),
            #    icon,
            #    (self.mp.size(), self.size(), self.mp.apps_menu.size(), self.mp.create_menu.size(), self.mp.create_apps_menu.size(), self.mp.apps_menu.size(), self.mp.notification_menu.size(), self.mp.schedule_menu.size()))
            return None
        QMessageBox.warning(
            self, "Error", "Config only need 2 items inside!\nReopen GUI and try it again.")
        return None
