"Database module from Logic Module"
import os
from typing import Any, Callable
from PyQt5.QtWidgets import QMessageBox
try:
    from sqlite3 import (Connection,
                         connect, DatabaseError)
except ImportError as exc:
    raise ImportError("Error by importing 'sqlite3' module.") from exc

from utils import otuple_str, cwddb, elementType, cwd
from utils import others


def create_brain_tables(conn):
    cur = conn.cursor()
    cur.execute("""CREATE TABLE IF NOT EXISTS Config(
            id INTEGER PRIMARY KEY AUTOINCREMENT,
            image_path TEXT NOT NULL,
            title VARCHAR(30) NOT NULL
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
    return None


def create_login_tables(conn):
    cur = conn.cursor()
    cur.execute("DROP TABLE IF EXISTS Activities")
    cur.execute("DROP TABLE IF EXISTS Icons")
    cur.execute("DROP TABLE IF EXISTS Urls")
    cur.execute("DROP TABLE IF EXISTS Apps")
    cur.execute("DROP TABLE IF EXISTS Notifications")
    cur.execute("DROP TABLE IF EXISTS Config")
    cur.execute("""CREATE TABLE IF NOT EXISTS Login(
        id INTEGER PRIMARY KEY AUTOINCREMENT,
        username VARCHAR(200) NOT NULL,
        password VARCHAR(200) NOT NULL
        )""")
    conn.commit()
    cur.close()
    del cur
    return None


class ParentDatabase:
    def __init__(self, path_to_db: str, type: str):
        self.name = self.__class__.__name__.lower()
        if os.path.exists(path_to_db) and type == "brain":
            self.DB_PATH = path_to_db
        elif os.path.exists(path_to_db) and type == "login":
            self.DB_PATH = path_to_db
        else:
            self.DB_PATH = fr"{cwd}\brain_mine.db"

        self.connection = self._create_connection()

    def _create_connection(self, func: Callable[[], Any] = None):
        try:
            conn = connect(self.DB_PATH)
            if func is not None:
                func(conn)
            return conn
        except DatabaseError as excp:
            raise DatabaseError(excp) from excp


class BrainDatabase(ParentDatabase):
    def __init__(self, path_to_db: str):
        super().__init__(path_to_db, "brain")
        self.connection = self._create_connection(create_brain_tables)
        self.app_path_actual = 0
        self.create_apps_menu_actual = 0
        self.apps_paths = self.fetch_all_apps_paths()
        self.apps_names = self.fetch_all_apps_names()
        self.apps_ids = self.fetch_all_apps_ids()

    def fetch_all_apps_paths(self):
        "Get all Applications directories"
        conn = self.connection
        cur = conn.cursor()
        sql = """
        SELECT path FROM Apps
        """
        cur.execute(sql)
        return cur.fetchall()

    def fetch_all_apps_names(self):
        "Get all Applications names"
        conn = self.connection
        cur = conn.cursor()
        sql = """
        SELECT name FROM Apps
        """
        cur.execute(sql)
        return cur.fetchall()

    def fetch_all_apps_ids(self):
        "Get all Applications ids"
        conn = self.connection
        cur = conn.cursor()
        sql = """
        SELECT id FROM Apps
        """
        cur.execute(sql)
        return cur.fetchall()

    def get_current_apps_path_apps(self):
        "Get the current Application directory"
        if len(self.apps_paths) != 0:
            return self.apps_paths[self.app_path_actual]
        raise IndexError("There are not items in database to look for")

    def right_path(self):
        "Moves right in the Apps Directory list"
        self.app_path_actual += 1
        self.app_path_actual %= len(self.apps_paths)

    def left_path(self):
        "Moves left in the Apps Directory list"
        self.app_path_actual -= 1
        self.app_path_actual %= len(self.apps_paths)

    def get_current_apps_name(self):
        "Get the current Application name"
        if len(self.apps_names) != 0:
            return self.apps_names[self.create_apps_menu_actual]
        raise IndexError("There are not items in database to look for")

    def get_current_apps_id(self):
        "Get the current Application id"
        if len(self.apps_ids) != 0:
            return self.apps_ids[self.create_apps_menu_actual]
        raise IndexError("There are not items in database to look for")

    def get_current_apps_path(self):
        "Get the current Application directory"
        if len(self.apps_paths) != 0:
            return self.apps_paths[self.create_apps_menu_actual]
        raise IndexError("There are not items in database to look for")

    def right_create_apps_menu(self):
        "Moves right in the Apps list"
        self.create_apps_menu_actual += 1
        self.create_apps_menu_actual %= len(self.apps_ids)

    def left_create_apps_menu(self):
        "Moves left in the Apps list"
        self.create_apps_menu_actual -= 1
        self.create_apps_menu_actual %= len(self.apps_ids)

    def create_log_apps(self, log: otuple_str, element: elementType):
        "Creates an Application Log"
        conn = self.connection
        cur = conn.cursor()
        sql = """
        SELECT name, path, COUNT(*) FROM Apps
        GROUP BY name, path HAVING COUNT(*) > 1
        """

        cur.execute(sql)
        results = cur.fetchall()
        if len(results) == 0:
            sql = '''
            INSERT INTO Apps(name, path)
            VALUES(?, ?)
            '''
            cur.execute(sql, log)
            conn.commit()
            QMessageBox.information(
                element, 'Database', 'Information added to database')
            return cur.lastrowid
        QMessageBox.warning(
            element, 'Error', 'Data already in database')
        return None

    def delete_log_apps(self, log: tuple[str, str], element: elementType):
        "Deletes an Application Log"
        if len(log) == 2:
            conn = self.connection
            cur = conn.cursor()
            sql = """
            SELECT name, path FROM Apps
            WHERE name = ? AND path = ?
            """
            cur.execute(sql, log)
            result = cur.fetchone()
            if result:
                sql = """
                DELETE FROM Apps WHERE name = ? AND path = ?
                """
                cur.execute(sql, log)
                conn.commit()
                conn.close()
                QMessageBox.information(
                    element, "Deleted", "Elements deleted in database")
            else:
                QMessageBox.warning(element, "Not Found",
                                    "Elements not found in database")
        QMessageBox.warning(
            element, "Error", "Only 2 items allowed in tuple")

    def update_log_apps(self, path: str, name: str, element: elementType):
        # TODO: Create a GUI that allows the user to update an App Directory according to the name
        "Updates an Application Log"
        conn = self.connection
        cur = conn.cursor()
        sql = """
        UPDATE Apps SET path = ? WHERE name = ?
        """
        cur.execute(sql, (path, name))
        conn.commit()
        conn.close()
        QMessageBox.information(element, "Updated", "Path updated in database")

    def set_config(self, element: elementType, config: tuple[str, str]):
        """Sets the config with a directory and title that will be used for all 
        Program's GUI and Stray"""
        assert len(config) == 2, "Config length must be 2"
        conn = self.connection
        cur = conn.cursor()

        sql = """
        INSERT INTO Config(image_path, title)
        VALUES(?, ?)
        """
        cur.execute(sql, config)
        conn.commit()
        QMessageBox.information(element, "Information",
                                "Your config has been saved")
        others.updateWindow(element)
        return cur.lastrowid

    def update_config_icon(self, element: elementType, new_icon: str, title: str):
        # TODO: Create a GUI that allows the user to set a new icon with ease
        "Updates the icon according to the title"
        conn = self.connection
        cur = conn.cursor()

        sql = """
        UPDATE Config SET image_path = ? WHERE title = ?
        """

        cur.execute(sql, (new_icon, title))
        conn.commit()
        conn.close()
        QMessageBox.information(element, "Information", "Icon changed")

    def update_config_title(self, element: elementType, new_title: str, icon: str):
        # TODO: Create a GUI that allows the user to set a new title with ease
        "Updates title according to the icon"
        conn = self.connection
        cur = conn.cursor()

        sql = """
        UPDATE Config SET title = ? WHERE icon = ?
        """
        cur.execute(sql, (new_title, icon))
        conn.commit()
        conn.close()
        QMessageBox.information(element, "Information", "Title changed")

    def delete_config(self):
        "Deletes the unique id found in database"
        conn = self.connection
        cur = conn.cursor()

        cur.execute("""
                    DELETE FROM Config
                    """)
        conn.commit()

    def get_config(self):
        "Returns the config found in database"
        conn = self.connection
        cur = conn.cursor()
        sql = """
        SELECT image_path, title FROM Config
        """
        cur.execute(sql)
        return cur.fetchone()


class LoginDatabase(ParentDatabase):
    def __init__(self, path_to_db: str):
        super().__init__(path_to_db, "login")
        self.connection = self._create_connection(create_login_tables)

    def fetch_all_logins(self, username: str, password: str):
        "Get all logins and checks if an username and password exists in Database"
        conn = self.connection
        cur = conn.cursor()
        sql = """
        SELECT username, password FROM Login 
        WHERE username = ? AND password = ?
        """
        logins = cur.execute(sql, (username, password))
        return logins.fetchall()

    def add_user_logins(self, username: str, password: str):
        "Adds a Login to Database according to some QLineEdit values in SHA256"
        conn = self.connection
        cur = conn.cursor()

        sql = """
        INSERT INTO Login(username, password)
        VALUES(?, ?)
        """
        cur.execute(sql, (username, password))
        conn.commit()
        return cur.lastrowid

    def update_user_password_logins(self, element: elementType, username: str,
                                    password: str, new_password: str):
        # TODO: Create a GUI that allows the user to update his password with ease
        "Updates the user's password in database"
        conn = self.connection
        cur = conn.cursor()

        sql = """
        UPDATE Login SET password = ? WHERE (username = ? AND password = ?)
        """
        cur.execute(sql, (new_password, username, password))
        conn.commit()
        conn.close()
        QMessageBox.information(
            element, "Password changed", "Your password has been updated")
        return None
