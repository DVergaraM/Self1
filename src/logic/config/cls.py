import os
from typing import Any
from PyQt5.QtGui import QIcon, QImageReader
from PyQt5.QtWidgets import QFileDialog
from PyQt5 import uic

from utils import elementType, cwd, SubWindow
from utils.config import setConfig, setMultipleConfig
from utils.setters import setText, textChangedConnect, connect, enableButton
from utils.others import updateWindow, getText

from logic import database


class ConfigMenu(SubWindow):
    def __init__(self, parent: Any | None, icon: QIcon, db: database.Database):
        super().__init__(size=(510, 460))
        self.icon = icon
        self.mp = parent
        self.db = db
        self._config = ()
        uic.loadUi(fr"{cwd}logic\config\config_menu.ui", self)
        setConfig(self, "Config Menu", self.icon)

    def loadShow(self):
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
        self.show()

    def validate_all(self):
        if all([getText(self, "title_input") != "", getText(self, "path_input") != ""]):
            enableButton(self, {"save_all_button": True})
        else:
            enableButton(self, {"save_all_button": False})
        updateWindow(self)

    def browse_icon(self):
        realpath = os.path.realpath("C:/Users")
        supportedFormats = QImageReader.supportedImageFormats()
        formats = []
        for sF in supportedFormats:
            formats.append(f"*.{sF.data().decode()}")
        formated = " ".join(formats)
        text_filter = f"Images ({formated})"
        image_path, _ = QFileDialog.getOpenFileName(
            self, "Open an image", realpath, text_filter)
        print(image_path)
        self._config = tuple(set(self._config))
        self._config += (image_path, )
        setText(self, ("path_input", image_path))
        updateWindow(self)

    def save_title(self):
        title = str(getText(self, "title_input"))
        self._config = tuple(set(self._config))
        self._config += (title, )
        updateWindow(self)

    def add_to_db(self):
        self._config = tuple(set(self._config))
        if len(self._config) == 2:
            self.db.delete_config()
            self.db.set_config(self, self._config)
            icon, title = self.db.get_config()
            icon = QIcon(icon)
            setMultipleConfig(
                (self.mp, self, self.mp.apps_menu, self.mp.create_menu,
                 self.mp.create_apps_menu, self.mp.apps_menu, self.mp.notification_menu),
                (str(title), self.mp.config_menu.windowTitle(), self.mp.apps_menu.windowTitle(), self.mp.create_menu.windowTitle(
                ), self.mp.create_apps_menu.windowTitle(), self.mp.apps_menu.windowTitle(), self.mp.notification_menu.windowTitle()),
                icon,
                (self.mp.size(), self.size(), self.mp.apps_menu.size(), self.mp.create_menu.size(), self.mp.create_apps_menu.size(), self.mp.apps_menu.size(), self.mp.notification_menu.size()))
            # setConfig(self.config_menu, self.config_menu.windowTitle(), icon, self.config_menu.size())
        else:
            raise ValueError("'Config' only need 2 items inside")
