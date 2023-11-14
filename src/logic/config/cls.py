import os
from PyQt5.QtGui import QIcon, QImageReader
from PyQt5.QtWidgets import QFileDialog, QMessageBox
from PyQt5 import uic

from utils import cwd, SubWindow, elementType
from utils.config import setConfig, setMultipleConfig
from utils.setters import setText, enableButton, textChangedConnect, connect
from utils.others import remove, updateWindow, getText

from logic import database as l_database


class ConfigMenu(SubWindow):
    """
    A subwindow for configuring the application's settings.

    Args:
        parent (Any): The parent widget.
        icon (QIcon): The icon to be displayed in the GUI.
        db (l_database.BrainDatabase): The database where the items are stored.
    """

    def __init__(self, parent: elementType, icon: QIcon, database: l_database.BrainDatabase):
        '''
        Initializes the ConfigMenu class.
        '''
        super().__init__(size=(510, 460))
        self.icon = icon
        self.my_parent = parent
        self.database = database
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
                title != "" and os.path.exists(self._config[0]): # type: ignore
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
            setMultipleConfig(self.my_parent, icon, None, default_title=title)
            print("Config setted for all windows")
            return None
        QMessageBox.warning(
            self, "Error", "Config only need 2 items inside!\nReopen GUI and try it again.")
        return None
