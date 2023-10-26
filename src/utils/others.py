"Others module from Utils module"
from hashlib import sha256
from typing import Any, overload
from datetime import datetime

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
    "Updates a window and reloads variables"
    try:
        if hasattr(element, "db") and hasattr(element, "DB_PATH"):
            db: database.Database = getattr(element, "db")
            DB_PATH: str = getattr(element, "DB_PATH")
            if hasattr(db, "connection"):
                connection: Any = getattr(db, "connection")
                element.db = database.Database(DB_PATH)
                element.connection = connection
                config.setConfig(element, element.windowTitle(),
                                 element.windowIcon(), element.size())
                element.update()
            else:
                config.setConfig(element, element.windowTitle(),
                                 element.windowIcon(), element.size())
                element.update()
        elif hasattr(element, "db") and hasattr(element, "DB_PATH_CONFIG") and\
                hasattr(element, "db_login") and hasattr(element, "DB_PATH_LOGIN"):
            db: database.Database = getattr(element, "db")
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
    except AttributeError as excep:
        raise AttributeError(excep) from excep


def sha(element: elementType, objs: tuple[attribute, attribute]) -> tuple[str, str]:
    "Converts QLineEdit values to SHA256 and return it as a tuple"
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
    if len(result) == len(comparation):
        j: tuple[bool] = tuple()
        for _, (element, comp) in enumerate(zip(result, comparation)):
            if element != comp:
                j += (True, )
            else:
                j += (False, )
        return j
    return False


def remove(elements: tuple) -> tuple:
    "Removes duped elements in tuple"
    return tuple(set(elements))


@overload
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

