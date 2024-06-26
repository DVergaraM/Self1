"Database module from Logic Module"
# pylint: disable=import-self
# pylint: disable=invalid-name
# pylint: disable=no-name-in-module
# pylint: disable=import-error
# pylint: disable=no-member
# pylint: disable=not-callable
# pylint: disable=redefined-builtin
# pylint: disable=cyclic-import
# pylint: disable=too-many-public-methods
# pylint: disable=too-many-instance-attributes
from collections import deque
from typing import Callable
from sqlite3 import connect, Connection, DatabaseError
import os
from PyQt5.QtWidgets import QMessageBox

from utils import otuple_str, ElementType, cwd, others


def create_brain_tables(conn: Connection):
    """
    Creates the necessary tables for the SBrain application in the given database connection.

    :param conn: The connection to the SQLite database.
    :type conn: sqlite3.Connection

    :return: The same connection object passed as an argument.
    :rtype: sqlite3.Connection
    """
    cur = conn.cursor()
    cur.execute("""
                CREATE TABLE IF NOT EXISTS Config(
                    id INTEGER PRIMARY KEY AUTOINCREMENT,
                    image_path VARCHAR(200) NOT NULL,
                    title VARCHAR(20) NOT NULL
                )
                """)
    cur.execute("""
                CREATE TABLE IF NOT EXISTS Icons(
                id INTEGER PRIMARY KEY AUTOINCREMENT,
                name VARCHAR(50) NOT NULL,
                Path VARCHAR(200) NOT NULL
                )
                """)
    cur.execute("""
                CREATE TABLE IF NOT EXISTS Urls(
                id INTEGER PRIMARY KEY AUTOINCREMENT,
                name VARCHAR(50) NOT NULL,
                Url VARCHAR(150) NOT NULL
                )
                """)
    cur.execute("""
                CREATE TABLE IF NOT EXISTS Apps(
                    id INTEGER PRIMARY KEY AUTOINCREMENT,
                    name VARCHAR(50) NOT NULL,
                    path VARCHAR(700) NOT NULL
                )
                """)
    cur.execute("""
                CREATE TABLE IF NOT EXISTS Tasks(
                    id INTEGER PRIMARY KEY AUTOINCREMENT,
                    time VARCHAR(100) NOT NULL,
                    method_name VARCHAR(30) NOT NULL,
                    url VARCHAR(150),
                    job VARCHAR(450) NOT NULL
                )
                """)
    cur.execute("""
                CREATE TABLE IF NOT EXISTS Notifications(
                    id INTEGER PRIMARY KEY AUTOINCREMENT,
                    time VARCHAR(10) NOT NULL,
                    title VARCHAR(50) NOT NULL,
                    message VARCHAR(100) NOT NULL,
                    launch VARCHAR(250) NOT NULL
                    )""")
    conn.commit()
    cur.close()
    del cur
    return conn


def create_login_tables(conn: Connection):
    """
    Creates the necessary tables for the login system in the specified database connection.

    :param conn: A SQLite database connection object.
    :type conn: sqlite3.Connection

    :return: The same database connection object passed as an argument.
    :rtype: sqlite3.Connection
    """
    cur = conn.cursor()
    cur.execute("DROP TABLE IF EXISTS Activities")
    cur.execute("DROP TABLE IF EXISTS Icons")
    cur.execute("DROP TABLE IF EXISTS Urls")
    cur.execute("DROP TABLE IF EXISTS Apps")
    cur.execute("DROP TABLE IF EXISTS Notifications")
    cur.execute("DROP TABLE IF EXISTS Config")
    cur.execute("""
                CREATE TABLE IF NOT EXISTS Login(
                    id INTEGER PRIMARY KEY AUTOINCREMENT,
                    username VARCHAR(200) NOT NULL,
                    password VARCHAR(200) NOT NULL
                    )
                    """)
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

        :param path_to_db: The path to the database file.
        :type path_to_db: str
        :param type: The type of database (either "brain" or "login").
        :type type: str
        """
        self.name = self.__class__.__name__.lower()
        if os.path.exists(path_to_db) and type in ["brain", "login"]:
            self.DB_PATH = path_to_db
        else:
            self.DB_PATH = fr"{cwd}\brain_mine.db"
        self._connection = self.create_connection()

    @property
    def connection(self) -> Connection:
        """
        Returns the connection to the database.
        """
        return self._connection

    def create_connection(self, func: Callable[[Connection], Connection] | None = None):
        """
        Creates a connection to the database.

        :param func: A function to be applied to the connection, by default None.
        :type func: Callable[[Connection], Connection]

        :return: The connection object.
        :rtype: Connection
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
    - create_log_apps(self, log: otuple_str, element: ElementType): Creates an application log.
    - delete_log_apps(self, log: tuple[str, str], element: ElementType): Deletes an application log.
    - update_log_apps(self, path: str, name: str, element: ElementType): Updates an application log.
    """

    def __init__(self, path_to_db: str):
        super().__init__(path_to_db, "brain")
        self._connection = self.create_connection(create_brain_tables)
        self.app_path_actual = 0
        self.create_apps_menu_actual = 0
        self.delete_task_menu_actual = 0
        self.notifications_menu_actual = 0
        self.apps_paths = deque(self.fetch_all_apps_paths())
        self.apps_names = deque(self.fetch_all_apps_names())
        self.apps_ids = deque(self.fetch_all_apps_ids())
        self.tasks_menu_time = deque(self.fetch_all_tasks_time())
        self.tasks_menu_url = deque(self.fetch_all_tasks_url())
        self.notifications_times = deque(self.fetch_all_notifications_times())
        self.notifications_titles = deque(self.fetch_all_notifications_titles())
        self.notifications_messages = deque(self.fetch_all_notifications_messages())
        self.notifications_launches = deque(self.fetch_all_notifications_launches())

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

    def create_log_apps(self, log: otuple_str, element: ElementType):
        """
        Creates an Application Log

        :param log: The log to be inserted into the database
        :type log: otuple_str
        :param element: The element to display the message box
        :type element: ElementType

        :return: The ID of the inserted log if successful, None otherwise
        :rtype: int or None
        """
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
            cur.execute(sql, log)  # type: ignore
            conn.commit()
            QMessageBox.information(
                element, 'Database', 'Information added to database')
            print(f"{others.get_time_status('INFO | Database')} - Information added to database")
            return cur.lastrowid
        QMessageBox.warning(
            element, 'Error', 'Data already in database')
        print(f"{others.get_time_status('ERROR')} - Data already in database")
        return None

    def delete_log_apps(self, log: tuple[str, str], element: ElementType):
        """
        Deletes an Application Log

        :param log: A tuple containing the name and path of the log
        :type log: tuple[str, str]
        :param element: The element to display the message box
        :type element: ElementType

        :return: None
        :rtype: None
        """
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
                QMessageBox.information(
                    element, "Deleted", "Elements deleted in database")
                return None
            QMessageBox.warning(element, "Not Found",
                                "Elements not found in database")
            return None
        QMessageBox.warning(
            element, "Error", "Only 2 items allowed in tuple")
        return None

    def update_log_apps(self, new_path: str, name: str, element: ElementType):
        """
        Updates an Application Log.

        :param new_path: The new path to update.
        :type new_path: str
        :param name: The name of the application.
        :type name: str
        :param element: The element to display the information.
        :type element: ElementType

        :return: None
        :rtype: None
        """
        conn = self.connection
        cur = conn.cursor()
        sql = """
        UPDATE Apps SET path = ? WHERE name = ?
        """
        cur.execute(sql, (new_path, name))
        conn.commit()
        QMessageBox.information(element, "Updated", "Path updated in database")

    def set_config(self, element: ElementType, config: tuple[str, str]):
        """
        Sets the config with a directory and title that will be used for all Program's GUI and Stray

        :param element: The element to display the information message box
        :type element: ElementType
        :param config: The configuration tuple containing the image path and title
        :type config: tuple[str, str]

        :return: The last inserted row id
        :rtype: int
        """
        assert len(config) == 2, "Config length must be 2"
        conn = self.connection
        cur = conn.cursor()
        image_path, title = config
        if len(title) > 20 and len(image_path) > 200:
            image_path, title = title, image_path
        if len(title) > len(image_path):
            title, image_path = image_path, title
        sql = """
        INSERT INTO Config(image_path, title)
        VALUES(?, ?)
        """
        cur.execute(sql, (image_path, title))
        conn.commit()
        QMessageBox.information(element, "Information",
                                "Your config has been saved")
        print(f"{others.get_time_status('INFO')} - Your config has been saved")
        others.update_window(element)
        return cur.lastrowid

    def update_config_icon(self, element: ElementType, new_icon: str, title: str):
        """
        Updates the icon according to the title.

        :param element: The element to display the information.
        :type element: ElementType
        :param new_icon: The new icon path.
        :type new_icon: str
        :param title: The title of the configuration.
        :type title: str

        :return: None
        :rtype: None
        """
        conn = self.connection
        cur = conn.cursor()

        sql = """
        UPDATE Config SET image_path = ? WHERE title = ?
        """

        cur.execute(sql, (new_icon, title))
        conn.commit()
        QMessageBox.information(element, "Information", "Icon changed")

    def update_config_title(self, element: ElementType, new_title: str, icon: str):
        """
        Updates the title of a configuration based on the provided icon.

        :param element: The element to display the information message.
        :type element: ElementType
        :param new_title: The new title to set for the configuration.
        :type new_title: str
        :param icon: The icon associated with the configuration.
        :type icon: str

        :return: None
        :rtype: None
        """
        conn = self.connection
        cur = conn.cursor()

        sql = """
        UPDATE Config SET title = ? WHERE icon = ?
        """
        cur.execute(sql, (new_title, icon))
        conn.commit()
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
        result = cur.fetchone()
        if result:
            return deque(result)
        return deque([f"{os.getcwd()}/assets/default.png", "Second Brain"])

    def create_task(self, log: otuple_str, element: ElementType = None):  # type: ignore
        """
        Creates an Schedule Log

        :param log: The log information
        :type log: otuple_str
        :param element: The element to display the message box
        :type element: ElementType

        :return: The ID of the inserted task or None if data already exists
        :rtype: int or None
        """
        conn = self.connection
        cur = conn.cursor()
        sql = """
        SELECT time, method_name, url, job, COUNT(*) FROM Tasks
        GROUP BY time, method_name, url, job HAVING COUNT(*) > 1
        """

        cur.execute(sql)
        results = cur.fetchall()
        if len(results) == 0:
            # time, method_name, url, job = log # type: ignore
            sql = '''
            INSERT INTO Tasks(time, method_name, url, job)
            VALUES(?, ?, ?, ?)
            '''
            # if len(time) > 5
            cur.execute(sql, log)  # type: ignore
            conn.commit()
            if element:
                QMessageBox.information(
                    element, 'Database', 'Information added to database')
            else:
                print(f"{others.get_time_status('INFO')} - Information added to database")
            return cur.lastrowid
        if element:
            QMessageBox.warning(
                element, 'Error', 'Data already in database')
        else:
            print(f"{others.get_time_status('ERROR')} - Data already in database")
        return None

    def remove_task(self, time: str, element: ElementType | None = None) -> bool:  # type: ignore
        """
        Removes a task from the schedule.

        :param element: The element to display the information.
        :type element: ElementType
        :param job: The job to remove.
        :type job: Any

        :return: True if the task was removed successfully, False otherwise.
        :rtype: bool
        """
        conn = connect(self.DB_PATH)
        cur = conn.cursor()
        sql = """
                SELECT time, COUNT(*) FROM Tasks
                GROUP BY time HAVING COUNT(*) > 0
                """
        cur.execute(sql)
        results = cur.fetchall()

        for result in deque(results):  # type: ignore
            if result[0] == time:
                sql = """
                DELETE FROM Tasks WHERE time = ?
                """
                cur.execute(sql, (result[0],))
                conn.commit()
                if cur.rowcount > 0:
                    if element:
                        QMessageBox.information(
                            element, "Information", "Task removed")
                    else:
                        print(f"{others.get_time_status('INFO')} - Task removed")
                    return True
                print(f"{others.get_time_status('WARN')} - No rows were deleted")
        return False

    def fetch_all_tasks_time(self):
        """
        Fetches all tasks from the database.

        :return: A list of all tasks.
        :rtype: list
        """
        conn = self.connection
        cur = conn.cursor()
        sql = """
        SELECT time FROM Tasks
        """
        cur.execute(sql)
        return cur.fetchall()

    def fetch_all_tasks(self):
        """
        Fetches all tasks from the database.

        :return: A list of all tasks.
        :rtype: list
        """
        conn = self.connection
        cur = conn.cursor()
        sql = """
        SELECT time, method_name, url, job FROM Tasks
        """
        cur.execute(sql)
        return cur.fetchall()

    def fetch_all_tasks_url(self):
        """
        Fetches all tasks from the database.

        :return: A list of all tasks.
        :rtype: list
        """
        conn = self.connection
        cur = conn.cursor()
        sql = """
        SELECT url FROM Tasks
        """
        cur.execute(sql)
        return cur.fetchall()

    def get_current_delete_task_menu_time(self):
        "Get the current Task Time"
        if len(self.tasks_menu_time) != 0:
            return self.tasks_menu_time[self.delete_task_menu_actual]
        raise IndexError("There are no items in database to look for")

    def get_current_delete_task_menu_url(self):
        "Get the current Task URL"
        if len(self.tasks_menu_url) != 0:
            return self.tasks_menu_url[self.delete_task_menu_actual]
        raise IndexError("There are no items in database to look")

    def right_delete_task_menu(self):
        "Moves right in the Apps list"
        self.delete_task_menu_actual += 1
        self.delete_task_menu_actual %= len(self.tasks_menu_time)

    def left_delete_task_menu(self):
        "Moves left in the Apps list"
        self.delete_task_menu_actual -= 1
        self.delete_task_menu_actual %= len(self.tasks_menu_time)

    def fetch_all_notifications(self):
        """
        Fetches all notifications from the database.

        :return: A list of all notifications.
        :rtype: list
        """
        conn = self.connection
        cur = conn.cursor()
        sql = """
        SELECT time, title, message, launch FROM Notifications
        """
        cur.execute(sql)
        return cur.fetchall()

    def fetch_all_notifications_times(self):
        """
        Fetches all notifications from the database.

        :return: A list of all notifications.
        :rtype: list
        """
        conn = self.connection
        cur = conn.cursor()
        sql = """
        SELECT time FROM Notifications
        """
        cur.execute(sql)
        return cur.fetchall()

    def fetch_all_notifications_titles(self):
        """
        Fetches all notifications from the database.

        :return: A list of all notifications.
        :rtype: list
        """
        conn = self.connection
        cur = conn.cursor()
        sql = """
        SELECT title FROM Notifications
        """
        cur.execute(sql)
        return cur.fetchall()

    def fetch_all_notifications_launches(self):
        """
        Fetches all notifications from the database.

        :return: A list of all notifications.
        :rtype: list
        """
        conn = self.connection
        cur = conn.cursor()
        sql = """
        SELECT launch FROM Notifications
        """
        cur.execute(sql)
        return cur.fetchall()

    def fetch_all_notifications_messages(self):
        """
        Fetches all notifications from the database.

        :return: A list of all notifications.
        :rtype: list
        """
        conn = self.connection
        cur = conn.cursor()
        sql = """
        SELECT message FROM Notifications
        """
        cur.execute(sql)
        return cur.fetchall()

    def get_current_notifications_time(self):
        "Get the current Notification Time"
        if len(self.notifications_times) != 0:
            return self.notifications_times[self.notifications_menu_actual]
        raise IndexError("There are no items in database to look for")

    def get_current_notifications_title(self):
        "Get the current Notification Title"
        if len(self.notifications_titles) != 0:
            return self.notifications_titles[self.notifications_menu_actual]
        raise IndexError("There are no items in database to look for")

    def get_current_notifications_message(self):
        "Get the current Notification Message"
        if len(self.notifications_messages) != 0:
            return self.notifications_messages[self.notifications_menu_actual]
        raise IndexError("There are no items in database to look for")

    def get_current_notifications_launch(self):
        "Get the current Notification Launch"
        if len(self.notifications_launches) != 0:
            return self.notifications_launches[self.notifications_menu_actual]
        raise IndexError("There are no items in database to look for")

    def notifications_menu_right(self):
        "Moves right in the Notifications list"
        self.notifications_menu_actual += 1
        self.notifications_menu_actual %= len(self.notifications_titles)

    def notifications_menu_left(self):
        "Moves left in the Notifications list"
        self.notifications_menu_actual -= 1
        self.notifications_menu_actual %= len(self.notifications_titles)

    def delete_notification(self, time: str, title: str, message: str, launch: str = "", **kwargs):
        """
        Deletes a notification from the database.

        :param time: The time of the notification.
        :type time: str
        :param title: The title of the notification.
        :type title: str
        :param message: The message of the notification.
        :type message: str
        :param launch: The launch of the notification, by default "".
        :type launch: str, optional

        :return: None
        :rtype: None
        """
        conn = self.connection
        cur = conn.cursor()
        sql = """
        SELECT time, title, message, launch FROM Notifications
        WHERE time = ? AND title = ? AND message = ? AND launch = ?
        """
        cur.execute(sql, (time, title, message, launch))
        result = cur.fetchone()
        if result:
            sql = """
            DELETE FROM Notifications WHERE time = ? AND title = ? AND message = ? AND launch = ?
            """
            cur.execute(sql, (time, title, message, launch))
            conn.commit()
            if "element" in kwargs:
                QMessageBox.information(
                    kwargs["element"], "Information", "Notification deleted from database")
            else:
                print(f"{others.get_time_status('INFO')} - Notification deleted from database")
            return None
        if "element" in kwargs:
            QMessageBox.warning(kwargs["element"], "Warning",
                                "There's no Notification in Database")
        else:
            print(f"{others.get_time_status('WARN')} - There's no Notification in Database")
        return None

    def add_notification(self, time: str, title: str, message: str, launch: str, **kwargs):
        """
        Adds a notification to the database.

        :param time: The time of the notification.
        :type time: str
        :param title: The title of the notification.
        :type title: str
        :param message: The message of the notification.
        :type message: str
        :param launch: The launch of the notification.
        :type launch: str

        :return: None
        :rtype: None
        """
        conn = self.connection
        cur = conn.cursor()
        sql = """
        SELECT time, title, message, launch FROM Notifications
        WHERE launch = ? AND time = ?
        """
        cur.execute(sql, (launch, time))
        result = cur.fetchone()
        if not result:
            sql = """
            INSERT INTO Notifications(time, title, message, launch)
            VALUES(?, ?, ?, ?)
            """
            cur.execute(sql, (time, title, message, launch))
            conn.commit()
            if "element" in kwargs:
                QMessageBox.information(
                    kwargs["element"], "Information", "Notification added to database")
            else:
                print(f"{others.get_time_status('INFO')} - Notification added to database")


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
    update_user_password_logins(element:ElementType, username:str, password:str, new_password:str)
        Updates the user's password in database.
    """

    def __init__(self, path_to_db: str):
        super().__init__(path_to_db, "login")
        self._connection = self.create_connection(create_login_tables)

    def fetch_all_logins(self, username: str, password: str, **kwargs):
        """
        Get all logins and checks if an username and password exists in Database

        :param username: The username to check
        :type username: str
        :param password: The password to check
        :type password: str
        :param kwargs: Additional keyword arguments
        :type kwargs: dict

        :return: A list of logins matching the username and password
        :rtype: list
        """
        if "encrypted" in kwargs and not kwargs["encrypted"]:
            username = str(others.sha_256(username))
        conn = self.connection
        cur = conn.cursor()
        sql = """
        SELECT username, password FROM Login 
        WHERE username = ? AND password = ?
        """
        logins = cur.execute(sql, (username, password))
        return logins.fetchall()

    def add_user_logins(self, username: str, password: str):
        """
        Adds a Login to Database according to some QLineEdit values in SHA256

        :param username: The username of the login
        :type username: str
        :param password: The password of the login
        :type password: str

        :return: The ID of the inserted login
        :rtype: int
        """
        conn = self.connection
        cur = conn.cursor()

        sql = """
        INSERT INTO Login(username, password)
        VALUES(?, ?)
        """
        cur.execute(sql, (username, password))
        conn.commit()
        return cur.lastrowid

    def update_user_password_logins(self, new_password: str,
                                    username: str, password: str):
        """
        Updates the user's password in the database.

        :param new_password: The new password to be set.
        :type new_password: str
        :param username: The username of the user.
        :type username: str
        :param password: The current password of the user.
        :type password: str

        :return: None
        :rtype: None
        """
        conn = self.connection
        cur = conn.cursor()

        sql = """
        UPDATE Login SET password = ? WHERE (username = ? AND password = ?)
        """
        u_name = str(others.sha_256(username))
        cur.execute(sql, (new_password, u_name, password))
        conn.commit()
