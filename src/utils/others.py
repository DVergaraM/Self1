"Others module from Utils module"

from hashlib import sha256
from typing import Any
from datetime import datetime
from hashlib import sha256

from utils import elementType, attribute, config
from logic import database


def getText(element: elementType,

            attrs: tuple[attribute] | attribute) -> tuple[()] | tuple[Any] | Any | None:
    "Gets a single or multiple QLineEdit value(s) and return it/them"
    if isinstance(attrs, tuple):
        getter = ()
        for attr in attrs:
            if isinstance(attr, attribute) and hasattr(element, attr):
                obj = getattr(element, attr)
                getter += (obj.text(), )
            else:
                continue
        return getter
    if isinstance(attrs, attribute):
        if hasattr(element, attrs):
            obj = getattr(element, attrs)
            return obj.text()
    return None


def updateWindow(element: elementType) -> None:
    """
    Updates a window and reloads variables.

    Args:
        element (elementType): The window element to be updated.

    Raises:
        AttributeError: If an attribute error occurs during the update process.
    """
    try:
        if (hasattr(element, "db") or hasattr(element, "database")):
            db: database.BrainDatabase = getattr(element, "db")
            DB_PATH: str = getattr(element, "DB_PATH")
            if hasattr(db, "connection"):
                connection: Any = getattr(db, "connection")
                element.db = database.BrainDatabase(DB_PATH)
                element.database = database.BrainDatabase(DB_PATH)
                element.connection = connection
                config.setConfig(element, element.windowTitle(),
                                 element.windowIcon(), element.size())
                element.update()
            else:
                config.setConfig(element, element.windowTitle(),
                                 element.windowIcon(), element.size())
                element.update()
        elif (hasattr(element, "db") and hasattr(element, "DB_PATH_CONFIG")) or\
                (hasattr(element, "db_login") and hasattr(element, "DB_PATH_LOGIN")) or (hasattr(element, "db_config") and hasattr(element, "DB_PATH_CONFIG")):
            db: database.BrainDatabase = getattr(
                element, "db") if hasattr(element, "db") else None
            db_login: database.LoginDatabase = getattr(element, "db_login")
            DB_PATH_CONFIG: str = getattr(element, "DB_PATH_CONFIG")
            DB_PATH_LOGIN: str = getattr(element, "DB_PATH_LOGIN")
            if hasattr(db, "connection"):
                connection: Any = getattr(db, "connection")
                element.db = database.Database(DB_PATH_CONFIG)
                element.db_login = database.Database(DB_PATH_LOGIN)
                element.connection = connection
                config.setConfig(element, element.windowTitle(),
                                 element.windowIcon(), element.size())
                element.update()
            else:
                config.setConfig(element, element.windowTitle(),
                                 element.windowIcon(), element.size())
                element.update()
        else:
            config.setConfig(element, element.windowTitle(),
                             element.windowIcon(), element.size())
            element.update()
    except AttributeError as excp:
        raise AttributeError(excp) from excp


def sha(element: Any, objs: Tuple[str, str]) -> Tuple[str, str]:
    """
    Converts QLineEdit values to SHA256 and returns it as a tuple.

    Args:
        element (Any): The element containing the attributes to be hashed.
        objs (Tuple[str, str]): A tuple containing the names of the attributes to be hashed.

    Returns:
        Tuple[str, str]: A tuple containing the hashed values of the attributes.
    Raises:
        IndexError: If the tuple contains more than 2 items.
        TypeError: If the objs parameter is not a tuple of strings.
    """
    if isinstance(objs, tuple):
        if len(objs) == 2:
            objs_in_sha = ()
            for _, obj in enumerate(objs):
                if hasattr(element, obj):
                    obj: Any = getattr(element, obj)
                    objsha: str = sha256(
                        str(obj.text()).encode('utf-8')).hexdigest()
                    objs_in_sha += (objsha, )
                else:
                    continue
            return objs_in_sha
        raise IndexError("Only 2 items are allowed in the tuple")
    raise TypeError("'objs' param must be str or tuple of str")


def compare(result: tuple[str, ...], comparation: tuple[str, ...]):
    "Compares the items inside 2 tuples and checks if they are the same"
    if len(result) != len(comparation):
        return False
    return tuple(element != comp for element, comp in zip(result, comparation))


def remove(elements: tuple) -> tuple:
    "Removes duped elements in tuple"
    return tuple(set(elements))


def get_time_log() -> str:
    "Returns the current time"
    date = datetime.now()
    format_date = f"{date.day}-{date.month}-{date.year}_"
    format_hour = f"{date.hour}-{date.minute}-{date.second}"
    return format_date+format_hour


def get_time():
    "Returns the current time"
    date = datetime.now()
    format_date = f"[{date.day}-{date.month}-{date.year} "
    format_time = f"{date.hour}:{date.minute}:{date.second}]"
    return format_date + format_time
