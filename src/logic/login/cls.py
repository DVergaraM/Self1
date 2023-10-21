from PyQt5 import uic
from PyQt5.QtWidgets import QDialog, QMessageBox
from PyQt5.QtGui import QIcon
from PyQt5.QtCore import QEvent

from logic.database import Database
from logic.register import cls as reg
from utils import cwd
from utils.config import setConfig
from utils.others import compare, updateWindow, getText, sha
from utils.setters import textChangedConnect, connect, enableButton

class LoginSystem(QDialog):
    "Subclass of `PyQt5.QtWidgets.QDialog`"
    def __init__(self) -> None:
        super(LoginSystem, self).__init__()
        uic.loadUi(fr'{cwd}logic\login\login_window.ui', self)
        self.DB_PATH_CONFIG = fr"{cwd}brain_mine.db"
        self.DB_PATH_LOGIN = fr"{cwd}login.db"
        self.db_config = Database(self.DB_PATH_CONFIG)
        self.db_login = Database(self.DB_PATH_LOGIN)
        icon, _ = self.db_config.get_config()
        self.icon = QIcon(icon)
        self.connection_config = self.db_config.connection
        self.connection_login = self.db_login.connection
        # self.setStyleSheet('background-color: black')
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
        if all(compare(getText(self, ("username_input", "password_input")), ("", ""))):
            enableButton(self, ("login_button", True))
        else:
            enableButton(self, ("login_button", False))
        updateWindow(self)

    def _handle_login(self):
        attrs = ("username_input", "password_input")
        iusername, ipassword = sha(self, attrs)

        login = self.db_login.fetch_all_logins(iusername, ipassword)

        if 0 < len(login) < 3:
            self.accept()
            updateWindow(self)
        else:
            updateWindow(self)
            QMessageBox.warning(
                self, 'Error', 'Bad user or password')

    def _open_register(self):
        register = reg.RegisterSystem()
        updateWindow(self)
        if register.exec_() == QDialog.DialogCode.Accepted:
            updateWindow(self)