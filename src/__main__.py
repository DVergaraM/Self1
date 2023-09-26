import os
from typing import Self, Union, Any, Callable, List, overload
# from logic.organizador_materias import Organizador_Materias
from logic.threads import ThreadNotifier, OSThread
# from gui.visor_materias import Aplicacion_Gui
from logic import SubWindow, LoginSystem, Database, setConfig, connect, setText, updateWindow, MyCallable
from PyQt5.QtWidgets import *
from PyQt5.QtCore import *
from PyQt5 import uic
from PyQt5.QtGui import *

cwd = fr"{os.getcwd()}\src\\"
DB_PATH = fr"{cwd}brain_mine.db"
ICON_PATH = fr"{cwd}images\aries.png"


class Gui(QMainWindow):
    def __init__(self) -> None:
        import sys
        super(Gui, self).__init__()
        uic.loadUi(fr'{cwd}ui\main_window.ui', self)
        self.db: Database = Database(DB_PATH)
        self.connection = self.db.connection
        self.icon: QIcon = QIcon(ICON_PATH)
        setConfig(self, "Second Brain", self.icon, (760, 680))
        self.notification_menu: SubWindow = SubWindow()
        self.apps_menu: SubWindow = SubWindow()
        self.create_menu: SubWindow = SubWindow()
        self.create_apps_menu: SubWindow = SubWindow()
        self.config_menu: SubWindow = SubWindow()
        d = {
            "notification_menu_button": self._notification_menu,
            "apps_menu_button": self._apps_menu,
            "exit_button": sys.exit,
            "create_menu_button": self._create_menu,
            "config_button": self._config_menu
        }
        connect(self, d)
        self.notifier: ThreadNotifier = ThreadNotifier()
        self.othread: OSThread = OSThread()
        self.show()

    def _config_menu(self):
        uic.loadUi(fr"{cwd}ui\config_menu.ui", self.config_menu)
        setConfig(self.config_menu, "Config Menu", self.icon, (510, 460))
        d = {
            "icon_selector_button": self._config_menu_icon_selector,
            "title_selector_button": self._config_menu_title_selector
        }
        connect(self.config_menu, d)
        self.config_menu.show()
        #connect(self.config_menu, d)
    def _config_menu_icon_selector(self):
        print("Icon selector")
    
    def _config_menu_title_selector(self):
        print("Title selector")

    def _notification_menu(self):
        uic.loadUi(fr"{cwd}ui\notification_menu.ui",
                   self.notification_menu)
        setConfig(self.notification_menu,
                  "Notification Menu", self.icon, (760, 680))
        d = {
            "start_popups_button": self.notifier.start,
            "stop_popups_button": self.notifier.stop,
            "exit_button": self.notification_menu.close,
            "apps_button_menu": self._apps_menu
        }

        connect(self.notification_menu, d)
        self.notification_menu.show()

    def _apps_menu(self):
        uic.loadUi(fr"{cwd}ui\apps_menu.ui", self.apps_menu)
        setConfig(self.apps_menu, "Apps Menu", self.icon, (760, 680))

        actual: Any = self.db.get_current_apps_path_apps()[0]
        setText(self.apps_menu, ("path_line", fr'"{actual}"'))
        d = {
            "exit_button": self.apps_menu.close,
            "right_button": self._apps_menu_path_avanzar,
            "left_button": self._apps_menu_path_retroceder,
            "run_button": self._apps_menu_path_run
        }
        connect(self.apps_menu, d)
        self.apps_menu.show()

    def _apps_menu_path_avanzar(self):
        with self.connection:
            self.db.right_path()
            actual: Any = self.db.get_current_apps_path_apps()[0]
            self.apps_menu.path_line.setText(fr'"{actual}"')

    def _apps_menu_path_retroceder(self):
        with self.connection:
            self.db.left_path()
            actual: Any = self.db.get_current_apps_path_apps()[0]
            self.apps_menu.path_line.setText(fr'"{actual}"')

    def _apps_menu_path_run(self):
        self.othread.path: Any = self.apps_menu.path_line.text()
        self.othread.start()

    def _create_menu(self):
        uic.loadUi(fr"{cwd}ui\create_menu.ui", self.create_menu)
        setConfig(self.create_menu, "Create Menu", self.icon, (760, 680))
        d = {
            "exit_button": self.create_menu.close,
            "create_apps_menu": self._create_apps_menu
        }
        connect(self.create_menu, d)
        self.create_menu.show()

    def _create_apps_menu(self):
        uic.loadUi(fr"{cwd}ui\create_apps_menu.ui", self.create_apps_menu)
        setConfig(self.create_apps_menu, "Apps Create", self.icon, (760, 680))
        actual_name = str(self.db.get_current_apps_name()[0])
        actual_path = str(self.db.get_current_apps_path()[0])
        d = {
            "name_input": actual_name,
            "path_input": actual_path
        }
        setText(self.create_apps_menu, d)
        d = {
            "exit_button": self.create_apps_menu.close,
            "right_button": self._create_apps_menu_avanzar,
            "left_button": self._create_apps_menu_retroceder,
            "add_button": self._create_apps_menu_add_to_db,
            "delete_button": self._create_apps_menu_delete_from_db,
            "edit_button": self._create_apps_menu_update_from_db
        }
        connect(self.create_apps_menu, d)
        self.create_apps_menu.show()

    def _create_apps_menu_avanzar(self):
        with self.connection:
            self.db.right_create_apps_menu()
            # actual_id = int(self.db.get_current_apps_id()[0])
            actual_name = str(self.db.get_current_apps_name()[0])
            actual_path = str(self.db.get_current_apps_path()[0])
            d = {
                "name_input": actual_name,
                "path_input": actual_path
            }
            setText(self.create_apps_menu, d)

    def _create_apps_menu_retroceder(self):
        with self.connection:
            self.db.left_create_apps_menu()
            actual_name = str(self.db.get_current_apps_name()[0])
            actual_path = str(self.db.get_current_apps_path()[0])
            d = {
                "name_input": actual_name,
                "path_input": actual_path
            }
            setText(self.create_apps_menu, d)

    def _create_apps_menu_add_to_db(self):
        current_name: str = f"{self.create_apps_menu.name_input.text()}"
        current_path: str = fr"{self.create_apps_menu.path_input.text()}"
        self.db.create_log_apps(
            (current_name, current_path), self.create_apps_menu)
        updateWindow(self.create_apps_menu)
        updateWindow(self.apps_menu)

    def _create_apps_menu_delete_from_db(self):
        current_name: str = f"{self.create_apps_menu.name_input.text()}"
        current_path: str = fr"{self.create_apps_menu.path_input.text()}"
        self.db.delete_log_apps(
            (current_name, current_path), self.create_apps_menu)
        updateWindow(self.create_apps_menu)
        updateWindow(self.apps_menu)

    def _create_apps_menu_update_from_db(self):
        current_name: str = f"{self.create_apps_menu.name_input.text()}"
        current_path: str = fr"{self.create_apps_menu.path_input.text()}"
        self.db.update_log_apps(
            current_path, current_name, self.create_apps_menu)
        updateWindow(self.create_apps_menu)
        updateWindow(self.apps_menu)


def main(argv: list[str]):
    import sys
    app: QApplication = QApplication(argv)
    login: LoginSystem = LoginSystem()
    if login.exec_() == QDialog.DialogCode.Accepted:
        gui: Gui = Gui()
        sys.exit(app.exec_())


if __name__ == '__main__':
    import sys
    main(sys.argv)
