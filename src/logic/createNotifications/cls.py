"Create Notifications Module"
# pylint: disable=invalid-name
# pylint: disable=no-name-in-module
# pylint: disable=import-error
# pylint: disable=too-many-instance-attributes
# pylint: disable=duplicate-code
from PyQt5.QtGui import QIcon
from PyQt5 import uic

from utils import cwd, SubWindow, ElementType
from utils.config import set_config
from utils.setters import set_text, connect
from utils.others import get_text, update_window

from logic import database as l_database


class CreateNotificationsMenu(SubWindow):
    """
    Subclass of `SubWindow` that represents a window for creating and managing Notifications

    Attributes:
    - icon (QIcon): The icon for the window.
    - parent (ElementType): The parent object of the window.
    - database(BrainDatabase): The database object used for storing application information.
    """

    def __init__(self, parent: ElementType, icon: QIcon,
                 database: l_database.BrainDatabase):
        """
        Initializes the class object.

        :param parent: The parent element.
        :type parent: ElementType
        :param icon: The icon for the class object.
        :type icon: QIcon
        :param database: The database object.
        :type database: l_database.BrainDatabase
        :rtype: None
        """
        super().__init__(size=(760, 680))
        self.icon = icon
        self.parent = parent
        self.database = database
        uic.loadUi(
            fr"{cwd}logic\createNotifications\create_notifications_menu.ui", self)
        set_config(self, "Notifications Create", self.icon, (760, 680))
        self.struct = {
            "title": "",
            "message": "",
            "icon": self.icon,
            "duration": "short",
            "launch": ""
        }
        self.actual_time = str(
            self.database.get_current_notifications_time()[0])
        self.actual_title = str(
            self.database.get_current_notifications_title()[0])
        self.actual_message = str(
            self.database.get_current_notifications_message()[0])
        self.actual_launch = str(
            self.database.get_current_notifications_title()[0])

    def loadShow(self):
        """
        Loads, connects, sets and shows the GUI.
        """
        set_text(self, {
            "time_line": self.actual_time,
            "title_line": self.actual_title,
            "message_line": self.actual_message,
            "url_line": self.actual_launch
        })
        connect(self, {
            "exit_button": self.close,
            "right_button": self.avanzar,
            "left_button": self.retroceder,
            "delete_button": self.delete_from_db,
            "add_button": self.add_to_db
        })
        self.show()

    def avanzar(self):
        """
        Loops front through the paths in database and sets it up in QLineEdit.
        """
        with self.database.connection:
            self.database.notifications_menu_right()
            self.actual_time = str(
                self.database.get_current_notifications_time()[0])
            self.actual_title = str(
                self.database.get_current_notifications_title()[0])
            self.actual_message = str(
                self.database.get_current_notifications_message()[0])
            self.actual_launch = str(
                self.database.get_current_notifications_title()[0])
            set_text(self, {
                "time_line": self.actual_time,
                "title_line": self.actual_title,
                "message_line": self.actual_message,
                "url_line": self.actual_launch
            })
        return self.actual_time, self.actual_title, self.actual_message, self.actual_launch

    def retroceder(self):
        """
        Loops back through the paths in database and sets it up in QLineEdit.
        """
        with self.database.connection:
            self.database.notifications_menu_left()
            self.actual_time = str(
                self.database.get_current_notifications_time()[0])
            self.actual_title = str(
                self.database.get_current_notifications_title()[0])
            self.actual_message = str(
                self.database.get_current_notifications_message()[0])
            self.actual_launch = str(
                self.database.get_current_notifications_title()[0])
            set_text(self, {
                "time_line": self.actual_time,
                "title_line": self.actual_title,
                "message_line": self.actual_message,
                "url_line": self.actual_launch
            })
        return self.actual_time, self.actual_title, self.actual_message, self.actual_launch

    def delete_from_db(self):
        """
        Deletes the task displayed in QLineEdit.
        """
        time, title, message, launch = get_text(
            self, ("time_line", "title_line", "message_line", "url_line"))
        current_working_directory = cwd
        self.database.delete_notification(time, title, message, launch)
        update_window(self)
        self.database = l_database.BrainDatabase(
            fr"{current_working_directory}\src\brain_mine.db")
        next_time, next_title, next_message, next_launch = self.avanzar()
        set_text(self, {
            "time_line": next_time,
            "title_line": next_title,
            "message_line": next_message,
            "url_line": next_launch
        })
        update_window(self)
        self.database = l_database.BrainDatabase(
            fr"{current_working_directory}\src\brain_mine.db")

    def add_to_db(self):
        """
        Adds the task displayed in QLineEdit to the database.
        """
        time, title, message, launch = get_text(
            self, ("time_line", "title_line", "message_line", "url_line"))
        self.database.add_notification(time, title, message, launch)
        update_window(self)
        self.database = l_database.BrainDatabase(fr"{cwd}\src\brain_mine.db")
        next_time, next_title, next_message, next_launch = self.avanzar()
        set_text(self, {
            "time_line": next_time,
            "title_line": next_title,
            "message_line": next_message,
            "url_line": next_launch
        })
        update_window(self)
        self.database = l_database.BrainDatabase(fr"{cwd}\src\brain_mine.db")
