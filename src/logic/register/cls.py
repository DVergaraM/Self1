"Register module"
# pylint: disable=invalid-name
# pylint: disable=no-name-in-module
# pylint: disable=import-error
from PyQt5 import uic
from PyQt5.QtWidgets import QDialog, QMessageBox
from PyQt5.QtGui import QIcon
from PyQt5.QtCore import QEvent

from logic.database import BrainDatabase, LoginDatabase

from utils import cwd
from utils.config import set_config
from utils.setters import text_changed_connect, connect, enable_button
from utils.others import update_window, get_text, sha, compare

class RegisterSystem(QDialog):
    """
    Subclass of `PyQt5.QtWidgets.QDialog` that provides a user interface for
    registering a new user in the system.
    """

    def __init__(self) -> None:
        super().__init__()
        uic.loadUi(fr"{cwd}logic\register\register_window.ui", self)
        DB_PATH_CONFIG = fr"{cwd}brain_mine.db" # pylint: disable=invalid-name
        DB_PATH_LOGIN = fr"{cwd}login.db" # pylint: disable=invalid-name
        database = BrainDatabase(DB_PATH_CONFIG)
        self.db_login = LoginDatabase(DB_PATH_LOGIN)
        icon, _ = database.get_config()
        self.icon = QIcon(icon)
        set_config(self, "Register", self.icon, (650, 400))
        text_changed_connect(self, {
            self.validate: [
                "username_input",
                "password_input"
            ]
        })
        connect(self, {
            "register_button": self.add_to_db,
            "exit_button": self.close
        })
        update_window(self)

    def validate(self, _: QEvent):
        """Checks if the values of both QLineEdit are different from \"\", 
        and enables a button if so."""
        if all(compare(
                get_text(self, ("username_input", "password_input")),  #type: ignore
                    ("", ""))): # type: ignore
            enable_button(self, {"register_button": True})
        else:
            enable_button(self, {"register button": False})
        update_window(self)

    def add_to_db(self):
        "Adds the QLineEdit values to database if not exists"
        i_username, i_password = sha(self, ("username_input", "password_input"))
        login = self.db_login.fetch_all_logins(i_username, i_password)

        if len(login) >= 1:
            update_window(self)
            QMessageBox.warning(
                self, "Error", "Username already exists\nTry a new one")
        else:
            self.db_login.add_user_logins(i_username, i_password)
            QMessageBox.information(
                self, "Success", "Username and password created.")
            update_window(self)
            self.accept()
            return None
        return None
