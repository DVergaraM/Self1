"Login Module"
# pylint: disable=invalid-name
# pylint: disable=no-name-in-module
# pylint: disable=import-error
from PyQt5 import uic
from PyQt5.QtWidgets import QDialog, QMessageBox
from PyQt5.QtGui import QIcon
from PyQt5.QtCore import QEvent

from logic.database import BrainDatabase, LoginDatabase
from logic.register import cls as reg
from utils import cwd
from utils.config import set_config
from utils.others import compare, update_window, get_text, sha
from utils.setters import text_changed_connect, connect, enable_button


class LoginSystem(QDialog):
    """
    Subclass of `PyQt5.QtWidgets.QDialog` that provides a login window for the application.
    """

    def __init__(self) -> None:
        super().__init__()
        uic.loadUi(fr'{cwd}logic\login\login_window.ui', self)
        # pylint: disable=invalid-name
        self.DB_PATH_CONFIG = fr"{cwd}brain_mine.db"
        # pylint: disable=invalid-name
        self.DB_PATH_LOGIN = fr"{cwd}login.db"
        db_config = BrainDatabase(self.DB_PATH_CONFIG)
        self.db_login = LoginDatabase(self.DB_PATH_LOGIN)
        icon, _ = db_config.get_config()
        self.icon = QIcon(icon)
        update_window(self)
        set_config(self, "Login", self.icon, (760, 680))  # )(1240, 780))
        text_changed_connect(self, {
            self.validate: [
                "username_input",
                "password_input"
            ]
        })
        connect(self, {
            "login_button": self.handle_login,
            "create_form": self._open_register
        })

    def validate(self, _: QEvent):
        "Checks if the values of both QLineEdit are different from \"\", and enables a button if so"
        if all(compare(
            get_text(self, ("username_input", "password_input")), # type: ignore
            ("", ""))): # type: ignore
            enable_button(self, ("login_button", True))
        else:
            enable_button(self, ("login_button", False))
        update_window(self)

    def handle_login(self):
        """Fetches database to look for the username and password and if they are there, 
        closes window and continues with the App"""
        attrs = ("username_input", "password_input")
        i_username, i_password = sha(self, attrs)

        login = self.db_login.fetch_all_logins(i_username, i_password)

        if 0 < len(login) < 3:
            self.accept()
            update_window(self)
            return None
        update_window(self)
        QMessageBox.warning(
                self, 'Error', 'Bad user or password')
        return None

    def _open_register(self):
        "Opens Register Window if needed by the user."
        register = reg.RegisterSystem()
        update_window(self)
        if register.exec_() == QDialog.DialogCode.Accepted:
            update_window(self)
            return True
        return False
