from typing import Callable, Any
from sqlite3 import connect, Connection, DatabaseError
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

def create_brain_tables(conn: Connection):
    """
    Creates the necessary tables for the SBrain application in the given database connection.

    Args:
        conn (sqlite3.Connection): The connection to the SQLite database.

    Returns:
        sqlite3.Connection: The same connection object passed as an argument.
    """
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
    conn.commit()
    cur.close()
    del cur
    return conn


def create_login_tables(conn: Connection):
    """
    Creates the necessary tables for the login system in the specified database connection.

    Args:
        conn: A SQLite database connection object.

    Returns:
        The same database connection object passed as an argument.
    """
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
    return conn


class ParentDatabase:
    """
    A class representing a parent database.

    Attributes:
    -----------
    DB_PATH : str
        The path to the database file.
    connection : Connection
        The connection to the database.

    Methods:
    --------
    __init__(self, path_to_db: str, type: str)
        Initializes the ParentDatabase object.
    _create_connection(self, func: Callable[[], Any] = None)
        Creates a connection to the database.
    """

    def __init__(self, path_to_db: str, type: str):
        """
        Initializes the ParentDatabase object.

        Parameters:
        -----------
        path_to_db : str
            The path to the database file.
        type : str
            The type of database (either "brain" or "login").
        """
        self.name = self.__class__.__name__.lower()
        if os.path.exists(path_to_db) and type == "brain":
            self.DB_PATH = path_to_db
        elif os.path.exists(path_to_db) and type == "login":
            self.DB_PATH = path_to_db
        else:
            self.DB_PATH = fr"{cwd}\brain_mine.db"
        self._connection = self._create_connection()
        return None

    @property
    def connection(self) -> Connection:
        """
        Returns the connection to the database.

        Returns:
        --------
        Connection
            The connection to the database.
        """
        return self._connection

    def _create_connection(self, func: Callable[[Connection], Connection] = None) -> Connection: # type: ignore
        """
        Creates a connection to the database.

        Parameters:
        -----------
        func : Callable[[], Any], optional
            A function to be applied to the connection, by default None.

        Returns:
        --------
        Any
            The result of applying the function to the connection, if provided.
        """
        try:
            conn = connect(self.DB_PATH)
            return func(conn) if func else conn
        except DatabaseError as excp:
            raise DatabaseError(excp) from excp


class BrainDatabase(ParentDatabase):
    """
    A class representing a database for storing information about applications.

    Attributes:
    - path_to_db (str): The path to the database file.
    - _connection: The connection object to the database.
    - app_path_actual (int): The index of the current application directory.
    - create_apps_menu_actual (int): The index of the current application in the create apps menu.
    - apps_paths (list): A list of all application directories.
    - apps_names (list): A list of all application names.
    - apps_ids (list): A list of all application IDs.

    Methods:
    - __init__(self, path_to_db: str): Initializes the BrainDatabase object.
    - fetch_all_apps_paths(self): Returns a list of all application directories.
    - fetch_all_apps_names(self): Returns a list of all application names.
    - fetch_all_apps_ids(self): Returns a list of all application IDs.
    - get_current_apps_path_apps(self): Returns the current application directory.
    - right_path(self): Moves right in the application directory list.
    - left_path(self): Moves left in the application directory list.
    - get_current_apps_name(self): Returns the current application name.
    - get_current_apps_id(self): Returns the current application ID.
    - get_current_apps_path(self): Returns the current application directory.
    - right_create_apps_menu(self): Moves right in the application list.
    - left_create_apps_menu(self): Moves left in the application list.
    - create_log_apps(self, log: otuple_str, element: elementType): Creates an application log.
    - delete_log_apps(self, log: tuple[str, str], element: elementType): Deletes an application log.
    - update_log_apps(self, path: str, name: str, element: elementType): Updates an application log.
    """

    def __init__(self, path_to_db: str):
        super().__init__(path_to_db, "brain")
        self._connection = self._create_connection(create_brain_tables)
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
        return None

    def left_path(self):
        "Moves left in the Apps Directory list"
        self.app_path_actual -= 1
        self.app_path_actual %= len(self.apps_paths)
        return None

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
        return None

    def left_create_apps_menu(self):
        "Moves left in the Apps list"
        self.create_apps_menu_actual -= 1
        self.create_apps_menu_actual %= len(self.apps_ids)
        return None

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
            cur.execute(sql, log) # type: ignore
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
                return None
            else:
                QMessageBox.warning(element, "Not Found",
                                    "Elements not found in database")
                return None
        QMessageBox.warning(
            element, "Error", "Only 2 items allowed in tuple")
        return None

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
    """
    A class used to represent a Login Database.

    Attributes
    ----------
    path_to_db : str
        The path to the database file.

    Methods
    -------
    fetch_all_logins(username: str, password: str)
        Get all logins and checks if an username and password exists in Database.
    add_user_logins(username: str, password: str)
        Adds a Login to Database according to some QLineEdit values in SHA256.
    update_user_password_logins(element: elementType, username: str, password: str, new_password: str)
        Updates the user's password in database.
    """

    def __init__(self, path_to_db: str):
        super().__init__(path_to_db, "login")
        self._connection = self._create_connection(create_login_tables)

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
