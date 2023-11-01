"Login Module"
from PyQt5 import uic
from PyQt5.QtWidgets import QDialog, QMessageBox
from PyQt5.QtGui import QIcon
from PyQt5.QtCore import QEvent

from logic.database import BrainDatabase, LoginDatabase
from logic.register import cls as reg
from utils import cwd
from utils.config import setConfig
from utils.others import compare, updateWindow, getText, sha
from utils.setters import textChangedConnect, connect, enableButton


class LoginSystem(QDialog):
    """
    Subclass of `PyQt5.QtWidgets.QDialog` that provides a login window for the application.
    """

    def __init__(self) -> None:
        super(LoginSystem, self).__init__()
        uic.loadUi(fr'{cwd}logic\login\login_window.ui', self)
        self.DB_PATH_CONFIG = fr"{cwd}brain_mine.db"
        self.DB_PATH_LOGIN = fr"{cwd}login.db"
        db_config = BrainDatabase(self.DB_PATH_CONFIG)
        self.db_login = LoginDatabase(self.DB_PATH_LOGIN)
        icon, _ = db_config.get_config()
        self.icon = QIcon(icon)
        updateWindow(self)
        setConfig(self, "Login", self.icon, (760, 680))  # )(1240, 780))
        textChangedConnect(self, {
            self.validate: [
                "username_input",
                "password_input"
            ]
        })
        connect(self, {
            "login_button": self._handle_login,
            "create_form": self._open_register
        })

    def validate(self, e: QEvent):
        "Checks if the values of both QLineEdit are different from \"\", and enables a button if so"
        if all(compare(getText(self, ("username_input", "password_input")), ("", ""))):
            enableButton(self, ("login_button", True))
        else:
            enableButton(self, ("login_button", False))
        updateWindow(self)

    def _handle_login(self):
        """Fetches database to look for the username and password and if they are there, 
        closes window and continues with the App"""
        attrs = ("username_input", "password_input")
        i_username, i_password = sha(self, attrs)

        login = self.db_login.fetch_all_logins(i_username, i_password)

        if 0 < len(login) < 3:
            self.accept()
            updateWindow(self)
        else:
            updateWindow(self)
            QMessageBox.warning(
                self, 'Error', 'Bad user or password')

    def _open_register(self):
        "Opens Register Window if needed by the user."
        register = reg.RegisterSystem()
        updateWindow(self)
        if register.exec_() == QDialog.DialogCode.Accepted:
            updateWindow(self)
