from winotify import Notification as _Notifier
from winotify import audio as sounds
from datetime import datetime as _datetime
import schedule as _schedule
from typing import Optional, Callable, Any, Union, List, TypeVar, Self, TypeAlias
import os
from hashlib import sha256
from PyQt5.QtWidgets import QLabel, QWidget, QDialog,  QMainWindow, QMessageBox
from PyQt5 import uic, QtGui


QIcon: TypeAlias = QtGui.QIcon

MyCallable: TypeAlias = Callable[[], Any]

cwdui = fr"{os.getcwd()}\src\\"
otuple_str = TypeVar("otuple_str", tuple[str], tuple[tuple[str]], None)
cwddb = fr"{os.getcwd()}\src\login.db"

db: tuple[tuple[int, str, str, str]] = (
    (1, "https:/i.imgur.com/J6LeoUb.png", "@DVergaraM", "DVergaraM"),
    (2, "https://i.imgur.com/AX1yx9x.png",
     "Programming a Notifier", "Creating a Desktop App"),
    (3, "https://i.imgur.com/6QzKhtx.png", "@dvergaram_", "@dvergaram_")
)


class Notification(_Notifier):
    def __init__(self, app_id: str = "Second Brain", title: str = "Notifier", msg: str = "", icon: str = "", launch: str | Callable | None = "",  duration='long', sound=sounds.Reminder) -> None:
        super().__init__(app_id, title, msg, icon, duration)
        self.set_audio(sound, loop=False)
        if launch is not None:
            self.add_actions("Click Here!", launch)

    def run(self) -> None:
        self.show()
        date = _datetime.now()
        print(f"[{date.year}-{date.month}-{date.day} {date.hour}:{date.minute}:{date.second}] - Task: '{self.msg}'")


class Schedule:
    def __init__(self, time: Union[str, List[str]], task: Union[Callable[[], Any], List[Callable[[], Any]]], tz: Optional[str] = "America/Bogota") -> None:
        if isinstance(time, str) and isinstance(task, Callable):
            _schedule.every().day.at(time, tz).do(task)
        elif isinstance(time, list) and all(isinstance(t, str) for t in time) and isinstance(task, list) and all(isinstance(t, Callable) for t in task):
            if len(time) == len(task):
                for i in range(len(time)):
                    _schedule.every().day.at(time[i], tz).do(task[i])
            else:
                raise ValueError(
                    "'time' and 'task' params must have the same length of items")
        else:
            raise TypeError(
                "'time' and 'task' params must have the correct type")


def run_pending() -> None:
    _schedule.run_pending()


def stop() -> None:
    _schedule.clear()


class SubWindow(QWidget):
    def __init__(self, parent: Any = None):
        super(SubWindow, self).__init__(parent)
        label: QLabel = QLabel(self)
        label.setGeometry(0, 0, 760, 680)


elementType = TypeVar("elementType", QMainWindow, SubWindow, QWidget, QDialog)
"""
`TypeVar` of:
- `QMainWindow`
- `SubWindow`
- `QWidget`
- `QDialog`
"""


def sha(element: elementType, objs: tuple[str]) -> tuple[str, str]:
    if isinstance(objs, tuple):
        if len(objs) == 2:
            objs_in_sha = ()
            for i in range(len(objs)):
                obj: Any = getattr(element, objs[i])
                objsha: str = sha256(obj.text().encode('utf-8')).hexdigest()
                objs_in_sha += (objsha, )
            return objs_in_sha
        else:
            raise IndexError("Only 2 items are allowed in the tuple")
    else:
        raise TypeError("'objs' param must be str or tuple of str")


def connect(element: elementType, objs: tuple[str, Callable[[], Any]] | dict[str, Callable[[], Any]]):
    if isinstance(objs, tuple) and len(objs) == 2:
        attribute, method = objs
        if (isinstance(attribute, str) and isinstance(method, Callable)) and hasattr(element, attribute):
            obj = getattr(element, attribute)
            obj.clicked.connect(method)
    elif isinstance(objs, dict) and all(isinstance(key, str) and isinstance(value, Callable) for key, value in objs.items()):
        for key, value in objs.items():
            if hasattr(element, key):
                obj = getattr(element, key)
                obj.clicked.connect(value)
            else:
                continue
    else:
        raise TypeError(
            fr"'obj' and/or 'method' params must have the correct type")


def setConfig(element: elementType, title: str, icon: QtGui.QIcon, size: tuple[int, int]) -> None:
    element.setWindowTitle(title)
    element.setWindowIcon(icon)
    if len(size) == 2:
        element.setFixedSize(size[0], size[1])
    else:
        element.setFixedSize(760, 680)


def setText(element: elementType, objs: dict[str, int | str] | tuple[str, int | str]):
    if isinstance(objs, tuple) and len(objs) == 2:
        attribute, data = objs
        if (isinstance(attribute, str) and (isinstance(data, int) or isinstance(data, str))) and hasattr(element, attribute):
            obj = getattr(element, attribute)
            obj.setText(f"{data}")
    elif isinstance(objs, dict) and all(isinstance(key, str) and (isinstance(value, int) or isinstance(value, str))for key, value in objs.items()):
        for key, value in objs.items():
            if hasattr(element, key):
                obj = getattr(element, key)
                obj.setText(f"{value}")
            else:
                continue
    else:
        raise TypeError(
            fr"'objs' and/or 'data' params must have the correct type")


def getText(element: elementType, attrs: tuple[str] | str):
    if isinstance(attrs, tuple):
        getter = ()
        for attr in attrs:
            if hasattr(element, attr):
                obj = getattr(element, attr)
                getter += (obj.text(), )
            else:
                continue
        return getter
    elif isinstance(attrs, str):
        if hasattr(element, attrs):
            obj = getattr(element, attrs)
            return obj.text()


def updateWindow(element: elementType):
    try:
        if hasattr(element, "db") and hasattr(element, "DB_PATH"):
            db: Database = getattr(element, "db")
            DB_PATH: str = getattr(element, "DB_PATH")
            if hasattr(db, "connection"):
                connection: Any = getattr(db, "connection")
                element.update()
                element.db = Database(DB_PATH)
                element.connection = connection
            else:
                element.update()
        else:
            element.update()
    except Exception as e:
        raise Exception(e)


class RegisterSystem(QDialog):
    def __init__(self) -> None:
        super(RegisterSystem, self).__init__()
        uic.loadUi(fr"{cwdui}ui\register_window.ui", self)
        self.DB_PATH: str = fr"{cwdui}login.db"
        self.db: Database = Database(self.DB_PATH)
        icon, _ = self.db.get_config()
        self.icon: QtGui.QIcon = QtGui.QIcon(icon)
        self.connection = self.db.connection
        setConfig(self, "Register", self.icon, (650, 400))
        d = {
            "register_button": self._add_to_db,
            "exit_button": self.close
        }
        connect(self, d)
        updateWindow(self)

    def _add_to_db(self):
        attrs = ("username_input", "password_input")
        result = sha(self, attrs)
        iusername, ipassword = result

        login = self.db.fetch_all_logins(iusername, ipassword)

        if len(login) >= 1:
            self._update_window(self)
            QMessageBox.warning(
                self, "Error", "Username already exists\nTry a new one")
        else:
            self.db.add_user_logins(iusername, ipassword)
            QMessageBox.information(
                self, "Success", "Username and password created.")
            self._update_window(self)
            self.accept()


class LoginSystem(QDialog):
    def __init__(self) -> None:
        super(LoginSystem, self).__init__()
        uic.loadUi(fr'{cwdui}ui\login_window.ui', self)
        self.DB_PATH = fr"{cwdui}login.db"
        self.db = Database(self.DB_PATH)
        self.config = self.db.get_config()
        icon, _ = self.config
        self.icon = QtGui.QIcon(icon)
        self.connection = self.db.connection
        # self.setStyleSheet('background-color: black')
        updateWindow(self)
        setConfig(self, "Login", self.icon, (760, 680))  # )(1240, 780))
        d = {
            "login_button": self._handle_login,
            "create_form": self._open_register
        }
        connect(self, d)
        # self.show()

    def _handle_login(self):
        attrs = ("username_input", "password_input")
        iusername, ipassword = sha(self, attrs)

        login = self.db.fetch_all_logins(iusername, ipassword)

        if 0 < len(login) < 3:
            self.accept()
            updateWindow(self)
        else:
            updateWindow(self)
            QMessageBox.warning(
                self, 'Error', 'Bad user or password')

    def _open_register(self):
        register: RegisterSystem = RegisterSystem()
        updateWindow(self)
        if register.exec_() == QDialog.DialogCode.Accepted:
            updateWindow(self)


class Database:
    def __init__(self, path_to_db: str, log: otuple_str = None):
        try:
            from sqlite3 import (Connection,
                                 connect, DatabaseError)
        except ImportError:
            raise ImportError("Error by importing 'sqlite3' module.")
        self.__connect__ = connect
        self.__DatabaseError__: DatabaseError = DatabaseError
        self.__Connection__: Connection = Connection
        self._log: otuple_str = log
        self.__name: str = self.__class__.__name__.lower()
        self.app_path_actual: int = 0
        self.create_apps_menu_actual: int = 0
        self.DB_PATH: str = path_to_db
        self.connection = self._create_connection()
        self.apps_paths: list[Any] = self.fetch_all_apps_paths()
        self.apps_names: list[Any] = self.fetch_all_apps_names()
        self.apps_ids: list[Any] = self.fetch_all_apps_ids()

    @property
    def name(self):
        return self.__name

    def _create_connection(self):
        try:
            if self.DB_PATH == cwddb:
                conn = self.__connect__(self.DB_PATH)
                cur = conn.cursor()
                cur.execute("DROP TABLE IF EXISTS Activities")
                cur.execute("DROP TABLE IF EXISTS Icons")
                cur.execute("DROP TABLE IF EXISTS Urls")
                cur.execute("DROP TABLE IF EXISTS Apps")
                cur.execute("DROP TABLE IF EXISTS Notifications")
                cur.execute("DROP TABLE IF EXISTS Config")
                conn.commit()
                cur.close()
                del cur
                if isinstance(conn, self.__Connection__):
                    return conn
                else:
                    raise self.__DatabaseError__("Connection Failure")
            else:
                conn = self.__connect__(self.DB_PATH)
                cur = conn.cursor()
                cur.execute("""CREATE TABLE IF NOT EXISTS Config(
                    id INTEGER PRIMARY KEY AUTOINCREMENT,
                    image_path TEXT NOT NULL,
                    title VARCHAR(30) NOT NULL
                    )""")
                cur.execute("""CREATE TABLE IF NOT EXISTS Activities(
                    id INTEGER PRIMARY KEY AUTOINCREMENT,
                    Image_URL VARCHAR(120) NOT NULL,
                    Description VARCHAR(120) NOT NULL,
                    Small_text VARCHAR(120) NOT NULL
                    )""")
                cur.execute("""CREATE TABLE IF NOT EXISTS Icons(
                    id INTEGER PRIMARY KEY AUTOINCREMENT,
                    name VARCHAR(50) NOT NULL,
                    Path VARCHAR(200) NOT NULL
                    )""")
                cur.execute("""CREATE TABLE IF NOT EXISTS Urls(
                    id INTEGER PRIMARY KEY AUTOINCREMENT,
                    name VARCHAR(50) NOT NULL,
                    Url VARCHAR(150) NOT NULL
                    )""")
                cur.execute("""CREATE TABLE IF NOT EXISTS Apps(
                    id INTEGER PRIMARY KEY AUTOINCREMENT,
                    name VARCHAR(50) NOT NULL,
                    path VARCHAR(700) NOT NULL
                    )""")
                cur.execute("""CREATE TABLE IF NOT EXISTS Notifications AS
                            SELECT Urls.id as "id",
                            Urls.name as "name",
                            Urls.url as "url",
                            Icons.path as "path"
                            FROM Urls, Icons
                            WHERE(Urls.id == Icons.id) and (Urls.name == Icons.name)""")
                cur.close()
                del cur
                if isinstance(conn, self.__Connection__):
                    return conn
                else:
                    raise self.__DatabaseError__("Connection Failure")
        except self.__DatabaseError__ as dberror:
            raise self.__DatabaseError__(dberror)

    def fetch_all_apps_paths(self):
        conn = self.connection
        cur = conn.cursor()
        sql = f"""
        SELECT path FROM Apps
        """
        cur.execute(sql)
        self.apps_paths = cur.fetchall()
        return self.apps_paths

    def fetch_all_apps_names(self):
        conn = self.connection
        cur = conn.cursor()
        sql = f"""
        SELECT name FROM Apps
        """
        cur.execute(sql)
        self.apps_names = cur.fetchall()
        return self.apps_names

    def fetch_all_apps_ids(self):
        conn = self.connection
        cur = conn.cursor()
        sql = f"""
        SELECT id FROM Apps
        """
        cur.execute(sql)
        self.apps_ids = cur.fetchall()
        return self.apps_ids

    def get_current_apps_path_apps(self):
        if len(self.apps_paths) != 0:
            return self.apps_paths[self.app_path_actual]
        else:
            raise IndexError("There are not items in database to look for")

    def right_path(self):
        self.app_path_actual += 1
        self.app_path_actual %= len(self.apps_paths)

    def left_path(self):
        self.app_path_actual -= 1
        self.app_path_actual %= len(self.apps_paths)

    def get_current_apps_name(self):
        if len(self.apps_names) != 0:
            return self.apps_names[self.create_apps_menu_actual]
        else:
            raise IndexError("There are not items in database to look for")

    def get_current_apps_id(self):
        if len(self.apps_ids) != 0:
            return self.apps_ids[self.create_apps_menu_actual]
        else:
            raise IndexError("There are not items in database to look for")

    def get_current_apps_path(self):
        if len(self.apps_paths) != 0:
            return self.apps_paths[self.create_apps_menu_actual]
        else:
            raise IndexError("There are not items in database to look for")

    def right_create_apps_menu(self):
        self.create_apps_menu_actual += 1
        self.create_apps_menu_actual %= len(self.apps_ids)

    def left_create_apps_menu(self):
        self.create_apps_menu_actual -= 1
        self.create_apps_menu_actual %= len(self.apps_ids)

    def create_log_apps(self, log: otuple_str, element: elementType):
        conn = self.connection
        cur = conn.cursor()
        sql = f"""
        SELECT name, path, COUNT(*) FROM Apps
        GROUP BY name, path HAVING COUNT(*) > 1
        """

        cur.execute(sql)
        results = cur.fetchall()
        if len(results) == 0:
            sql = f'''
            INSERT INTO Apps(name, path)
            VALUES(?, ?)
            '''
            cur.execute(sql, log)
            conn.commit()
            QMessageBox.information(
                element, 'Database', 'Information added to database')
            return cur.lastrowid
        else:
            QMessageBox.warning(
                element, 'Error', 'Data already in database')

    def delete_log_apps(self, t: tuple[str, str], element: elementType):
        if len(t) == 2:
            conn = self.connection
            cur = conn.cursor()
            sql = f"""
            SELECT name, path FROM Apps
            WHERE name = ? AND path = ?
            """
            cur.execute(sql, t)
            result = cur.fetchone()
            if result:
                sql = f"""
                DELETE FROM Apps WHERE name = ? AND path = ?
                """
                cur.execute(sql, t)
                conn.commit()
                conn.close()
                QMessageBox.information(
                    element, "Deleted", "Elements deleted in database")
            else:
                QMessageBox.warning(element, "Not Found",
                                    "Elements not found in database")
        else:
            QMessageBox.warning(
                element, "Error", "Only 2 items allowed in tuple")

    def update_log_apps(self, path: str, name: str, element: elementType):
        conn = self.connection
        cur = conn.cursor()
        sql = f"""
        UPDATE Apps SET path = ? WHERE name = ?
        """
        cur.execute(sql, (path, name))
        conn.commit()
        conn.close()
        QMessageBox.information(element, "Updated", "Path updated in database")

    def fetch_all_logins(self, username: str, password: str):
        conn = self.connection
        cur = conn.cursor()
        sql = f"""
        SELECT username, password FROM Login 
        WHERE username = ? AND password = ?
        """
        l = cur.execute(sql, (username, password))
        return l.fetchall()

    def add_user_logins(self, username: str, password: str):
        conn = self.connection
        cur = conn.cursor()

        sql = """
        INSERT INTO Login(username, password)
        VALUES(?, ?)
        """
        cur.execute(sql, (username, password))
        conn.commit()
        return cur.lastrowid

    def update_user_password_logins(self, element: elementType, username: str, password: str, new_password: str):
        conn = self.connection
        cur = conn.cursor()

        sql = f"""
        UPDATE Login SET password = ? WHERE (username = ? AND password = ?)
        """
        cur.execute(sql, (new_password, username, password))
        conn.commit()
        conn.close()
        QMessageBox.information(
            element, "Password changed", "Your password has been updated")

    def set_config(self, element: elementType, config: tuple[str, str]):
        assert len(config) == 2, "Config length must be 2"
        conn = self.connection
        cur = conn.cursor()

        sql = f"""
        INSERT INTO Config(image_path, title)
        VALUES(?, ?)
        """
        cur.execute(sql, config)
        conn.commit()
        QMessageBox.information(element, "Information",
                                "Your config has been saved")
        return cur.lastrowid

    def update_config_icon(self, element: elementType, new_icon: str, title: str):
        conn = self.connection
        cur = conn.cursor()

        sql = f"""
        UPDATE Config SET image_path = ? WHERE title = ?
        """

        cur.execute(sql, (new_icon, title))
        conn.commit()
        conn.close()
        QMessageBox.information(element, "Information", "Icon changed")

    def update_config_title(self, element: elementType, new_title: str, icon: str):
        conn = self.connection
        cur = conn.cursor()

        sql = """
        UPDATE Config SET title = ? WHERE icon = ?
        """
        cur.execute(sql, (new_title, icon))
        conn.commit()
        conn.close()
        QMessageBox.information(element, "Information", "Title changed")

    def delete_config(self, element: elementType):
        conn = self.connection
        cur = conn.cursor()

        cur.execute("""
                    DELETE FROM Config
                    """)
        conn.commit()
        QMessageBox.information(element, "Information",
                                "All config has been reseted")

    def get_config(self):
        conn = self.connection
        cur = conn.cursor()
        sql = "SELECT image_path, title FROM Config"
        l = cur.execute(sql)
        return l.fetchone()
