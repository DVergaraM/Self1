"Change Password module"
# pylint: disable=invalid-name
# pylint: disable=no-name-in-module
# pylint: disable=import-error
# pylint: disable=duplicate-code
from PyQt5 import uic
from PyQt5.QtWidgets import QDialog, QMessageBox
from PyQt5.QtGui import QIcon
from PyQt5.QtCore import QEvent

from logic.database import BrainDatabase, LoginDatabase

from utils import cwd
from utils.config import set_config
from utils.setters import text_changed_connect, connect, enable_button, set_text
from utils.others import update_window, get_text, sha, compare


class ChangeCredentials(QDialog):
    """
    Subclass of `PyQt5.QtWidgets.QDialog` that provides a user interface for
    registering a new user in the system.
    """

    def __init__(self, username: str | None = None) -> None:  # type: ignore
        print("Opened")
        super().__init__()
        uic.loadUi(
            fr"{cwd}logic\changeCredentials\change_password_window.ui", self)
        self._username = username
        DB_PATH_CONFIG = fr"{cwd}brain_mine.db"
        DB_PATH_LOGIN = fr"{cwd}login.db"
        database = BrainDatabase(DB_PATH_CONFIG)
        self.db_login = LoginDatabase(DB_PATH_LOGIN)
        icon, _ = database.get_config()
        self.icon = QIcon(icon)
        set_config(self, "Change Password", self.icon, (760, 680))
        text_changed_connect(self, {
            self.validate_inputs: [
                "username_input",
                "password_input",
                "new_password_input"
            ]
        })
        connect(self, {
            "save_button": self.update_from_db,
            "exit_button": self.close
        })
        update_window(self)

    def validate_inputs(self, _: QEvent):
        """Checks if the values of both QLineEdit are different from \"\", 
        and enables a button if so."""
        if all(compare(
                get_text(self, ("username_input", "password_input",
                         "new_password_input")),  # type: ignore
                ("", "", ""))):  # type: ignore
            enable_button(self, {"save_button": True})
        else:
            enable_button(self, {"save_button": False})
        update_window(self)

    def update_from_db(self):
        "Adds the QLineEdit values to database if not exists"
        i_password, new_password, *_ = sha(  # type: ignore
            self, ("password_input", "new_password_input"))  # type: ignore
        if not self._username:
            self._username = f"{get_text(self, 'username_input')}"
        result = self.db_login.fetch_all_logins(
            self._username, i_password, encrypted=False)  # type: ignore
        if 0 < len(result) < 2:
            self.db_login.update_user_password_logins(new_password,
                                                      self._username, i_password)  # type: ignore
            QMessageBox.information(
                self, "Password changed", "Your password has been updated")
            set_text(self, {
                "username_input": "",
                "password_input": "",
                "new_password_input": ""
            })
            update_window(self)
            self.accept()
        else:
            QMessageBox.critical(
                self, "Error", "No username found in database.\nCreate an username and try again.")
