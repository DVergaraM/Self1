from typing import Any
from PyQt5.QtWidgets import QMessageBox

from utils import otuple_str, cwddb, elementType
from utils import others

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
        others.updateWindow(element)
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

    def delete_config(self):
        conn = self.connection
        cur = conn.cursor()

        cur.execute("""
                    DELETE FROM Config
                    """)
        conn.commit()

    def get_config(self):
        conn = self.connection
        cur = conn.cursor()
        sql = """
        SELECT image_path, title FROM Config
        """
        cur.execute(sql)
        return cur.fetchone()
