from PyQt5 import uic
from PyQt5.QtWidgets import QDialog, QMessageBox
from PyQt5.QtGui import QIcon
from PyQt5.QtCore import QEvent

from logic.database import Database

from utils import cwd
from utils.config import setConfig
from utils.setters import textChangedConnect, connect, enableButton
from utils.others import updateWindow, getText, sha, compare

class RegisterSystem(QDialog):
    "Subclass of `PyQt5.QtWidgets.QDialog`"
    def __init__(self) -> None:
        super(RegisterSystem, self).__init__()
        uic.loadUi(fr"{cwd}logic\register\register_window.ui", self)
        DB_PATH_CONFIG = fr"{cwd}brain_mine.db"
        DB_PATH_LOGIN = fr"{cwd}login.db"
        self.db = Database(DB_PATH_CONFIG)
        self.db_login = Database(DB_PATH_LOGIN)
        icon, _ = self.db.get_config()
        self.icon = QIcon(icon)
        self.connection = self.db.connection
        setConfig(self, "Register", self.icon, (650, 400))
        textChangedConnect(self, {
            self.validate: [
                "username_input",
                "password_input"
            ]
        })
        connect(self, {
            "register_button": self._add_to_db,
            "exit_button": self.close
        })
        updateWindow(self)

    def validate(self, e: QEvent):
        if all(compare(getText(self, ("username_input", "password_input")), ("", ""))):
            enableButton(self, {"register_button": True})
        else:
            enableButton(self, {"register button": False})
        updateWindow(self)

    def _add_to_db(self):
        iusername, ipassword = sha(self, ("username_input", "password_input"))
        login = self.db_login.fetch_all_logins(iusername, ipassword)

        if len(login) >= 1:
            updateWindow(self)
            QMessageBox.warning(
                self, "Error", "Username already exists\nTry a new one")
        else:
            self.db_login.add_user_logins(iusername, ipassword)
            QMessageBox.information(
                self, "Success", "Username and password created.")
            updateWindow(self)
            self.accept()