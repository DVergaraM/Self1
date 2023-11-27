"Others module from Utils module"
# pylint: disable=import-outside-toplevel
from hashlib import sha256
from typing import Any, Tuple
from datetime import datetime

from . import ElementType, attribute


def get_text(element: ElementType,
             attrs: tuple[attribute, ...] | attribute):
    """
    Gets a single or multiple QLineEdit value(s) and returns it/them

    :param element: The element from which to get the text
    :type element: ElementType
    :param attrs: The attribute(s) of the element to retrieve the text from
    :type attrs: tuple[attribute, ...] | attribute

    :return: The text value(s) of the element
    :rtype: str | tuple[str, ...]

    :raises AttributeError: If the attribute(s) do not exist on the element
    """
    if isinstance(attrs, tuple):
        return tuple(getattr(element, attr).text() if isinstance(attr, attribute)
                     and hasattr(element, attr) else "" for attr in attrs)
    return getattr(element, attrs).text() if isinstance(attrs, attribute)\
        and hasattr(element, attrs) else ""


def update_database(element: ElementType, db_attr: str, path_attr: str):
    """
    Update the database attribute of an element based on the given db_attr and path_attr.

    :param element: The element to update the database attribute.
    :type element: ElementType
    :param db_attr: The name of the database attribute to update.
    :type db_attr: str
    :param path_attr: The name of the path attribute containing the database path.
    :type path_attr: str

    :return: None
    :rtype: None

    :raises AttributeError: If the element does not have the specified db_attr or path_attr.
    """
    from logic.database import BrainDatabase, LoginDatabase
    if hasattr(element, db_attr) and hasattr(element, path_attr):
        if db_attr == "db_login":
            element.db_login = LoginDatabase(getattr(element, path_attr))
        else:
            setattr(element, db_attr, BrainDatabase(
                getattr(element, path_attr)))


def update_element(element: ElementType):
    """
    Updates the specified element with the current configuration settings.

    :param element: The element to be updated.
    :type element: ElementType

    :return: None
    :rtype: None

    :raises: None
    """
    from utils import config
    config.set_config(element, element.windowTitle(),
                      element.windowIcon(), element.size())
    element.update()


def update_window(element: ElementType) -> None:
    """
    Updates the window with the given element.

    :param element: The element to update the window with.
    :type element: ElementType

    :return: None
    :rtype: None

    :raises AttributeError: If an attribute error occurs during the update process.
    """
    try:
        update_database(element, "db", "DB_PATH")
        update_database(element, "database", "DB_PATH")
        update_database(element, "db_login", "DB_PATH_LOGIN")
        update_database(element, "db_config", "DB_PATH_CONFIG")
        update_element(element)
    except AttributeError as excp:
        raise AttributeError(excp) from excp


def sha(element: ElementType, objs: Tuple[str, ...] | str):
    """
    Converts QLineEdit values to SHA256 and returns it as a tuple.

    :param element: The element containing the attributes to be hashed.
    :type element: Any
    :param objs: A tuple containing the names of the attributes to be hashed.
                 If a single string is provided, it will be treated as a single attribute name.
    :type objs: Tuple[str, ...] | str

    :return: A tuple containing the hashed values of the attributes.
    :rtype: Tuple[str, ...]

    :raises IndexError: If the tuple contains more than 2 items.
    :raises TypeError: If the objs parameter is not a tuple of strings.
    """
    if isinstance(objs, tuple):
        if len(objs) >= 2:
            objs_in_sha = ()
            for _, obj in enumerate(objs):
                if hasattr(element, obj):
                    obj: Any = getattr(element, obj)
                    objsha: str = sha256(
                        str(obj.text()).encode('utf-8')).hexdigest()
                    objs_in_sha += (objsha, )
                else:
                    continue
            return objs_in_sha  # type: ignore
        raise IndexError("At least 2 items are allowed in the tuple")
    return sha256(str(getattr(element, objs).text()).encode('utf-8')).hexdigest()\
        if hasattr(element, objs) else ""


def sha_256(objs: str | Tuple[str]) -> str | Tuple[str]:
    """
    Converts a tuple of strings to SHA256 and returns it as a tuple.

    :param objs: A tuple containing the strings to be hashed.
    :type objs: Tuple[str]

    :return: A tuple containing the hashed values of the strings.
    :rtype: Tuple[str]

    :raises TypeError: If objs is not a string or a tuple.

    """
    if isinstance(objs, str):
        return sha256(str(objs).encode('utf-8')).hexdigest()
    objs_in_sha = ()
    for _, obj in enumerate(objs):
        objsha = sha256(str(obj).encode('utf-8')).hexdigest()
        objs_in_sha += (objsha, )
    return objs_in_sha  # type: ignore


def compare(result: tuple[str, ...], comparation: tuple[str, ...]):
    """
    Compares the items inside 2 tuples and checks if they are the same.

    :param result: The first tuple to compare.
    :type result: tuple[str, ...]
    :param comparation: The second tuple to compare.
    :type comparation: tuple[str, ...]

    :return: If the tuples are the same, returns True. Otherwise, returns False
        indicating which elements are different.
    :rtype: bool | tuple[bool]

    :raises: None
    """
    if len(result) != len(comparation):
        return False
    return tuple(element != comp for element, comp
                 in zip(result, comparation))


def remove(elements: tuple) -> tuple:
    """
    Removes duplicate elements in a tuple.

    :param elements: The tuple to remove duplicates from.
    :type elements: tuple

    :return: A new tuple with the duplicate elements removed.
    :rtype: tuple

    :raises: None
    """
    return tuple(set(elements))


def get_time_log() -> str:
    """
    Returns the current time in the format of day-month-year_hour-minute-second.

    :return: A string representing the current time in the format of \
        day-month-year_hour-minute-second.
    :rtype: str
    """
    date = datetime.now()
    format_date = f"{date.day}-{date.month}-{date.year}_"
    format_hour = f"{date.hour}-{date.minute}-{date.second}"
    return format_date+format_hour


def get_time():
    """
    Returns the current time in the format of [day-month-year hour:minute:second].

    :return: The current time in the format of [day-month-year hour:minute:second].
    :rtype: str
    """
    date = datetime.now()
    format_date = f"[{date.day}-{date.month}-{date.year} "
    format_time = f"{date.hour}:{date.minute}:{date.second}]"
    return format_date + format_time
