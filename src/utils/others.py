"Others module from Utils module"
# pylint: disable=import-outside-toplevel
from hashlib import sha256
from typing import Any, Tuple, overload
from datetime import datetime

from . import ElementType, attribute, config


def get_text(element: ElementType,
             attrs: tuple[attribute] | attribute) -> tuple[()] | tuple[Any] | Any | None | str:
    "Gets a single or multiple QLineEdit value(s) and return it/them"
    if isinstance(attrs, tuple):
        return tuple(getattr(element, attr).text() if isinstance(attr, attribute)
                     and hasattr(element, attr) else "" for attr in attrs)
    return getattr(element, attrs).text() if isinstance(attrs, attribute)\
        and hasattr(element, attrs) else ""


def update_database(element: ElementType, db_attr: str, path_attr: str):
    """
    Update the database attribute of an element based on the given db_attr and path_attr.

    Args:
        element (ElementType): The element to update the database attribute.
        db_attr (str): The name of the database attribute to update.
        path_attr (str): The name of the path attribute containing the database path.

    Returns:
        None
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

    Args:
        element (ElementType): The element to be updated.
    """
    config.set_config(element, element.windowTitle(),
                      element.windowIcon(), element.size())
    element.update()


def update_window(element: ElementType) -> None:
    """
    Updates the window with the given element.

    Args:
        element (ElementType): The element to update the window with.

    Raises:
        AttributeError: If an attribute error occurs during the update process.
    """
    try:
        update_database(element, "db", "DB_PATH")
        update_database(element, "database", "DB_PATH")
        update_database(element, "db_login", "DB_PATH_LOGIN")
        update_database(element, "db_config", "DB_PATH_CONFIG")
        update_element(element)
    except AttributeError as excp:
        raise AttributeError(excp) from excp


def sha(element: ElementType, objs: Tuple[str, str] | str) -> Tuple[str, str] | str:
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
            return objs_in_sha  # type: ignore
        raise IndexError("Only 2 items are allowed in the tuple")
    return sha256(str(getattr(element, objs).text()).encode('utf-8')).hexdigest()\
        if hasattr(element, objs) else ""


def sha_256(objs: Tuple[str]) -> Tuple[str]:
    """
    Converts a tuple of strings to SHA256 and returns it as a tuple.

    Args:
        objs (Tuple[str]): A tuple containing the strings to be hashed.

    Returns:
        Tuple[str]: A tuple containing the hashed values of the strings.
    """
    objs_in_sha = ()
    for _, obj in enumerate(objs):
        objsha: str = sha256(str(obj).encode('utf-8')).hexdigest()
        objs_in_sha += (objsha, )
    return objs_in_sha # type: ignore


def compare(result: tuple[str, ...], comparation: tuple[str, ...]) -> bool | tuple[bool]:
    """
    Compares the items inside 2 tuples and checks if they are the same.

    Args:
        result (tuple[str, ...]): The first tuple to compare.
        comparation (tuple[str, ...]): The second tuple to compare.

    Returns:
        bool | tuple[bool]: If the tuples are the same, returns True. Otherwise, returns False
        indicating which elements are different.
    """
    if len(result) != len(comparation):
        return False
    return tuple(element != comp for element, comp
                 in zip(result, comparation))  # type: ignore


def remove(elements: tuple) -> tuple:
    """
    Removes duplicate elements in a tuple.

    Args:
        elements (tuple): The tuple to remove duplicates from.

    Returns:
        tuple: A new tuple with the duplicate elements removed.
    """
    return tuple(set(elements))


def get_time_log() -> str:
    """
    Returns the current time in the format of day-month-year_hour-minute-second.

    Returns:
    str: A string representing the current time in the format of day-month-year_hour-minute-second.
    """
    date = datetime.now()
    format_date = f"{date.day}-{date.month}-{date.year}_"
    format_hour = f"{date.hour}-{date.minute}-{date.second}"
    return format_date+format_hour


def get_time():
    """
    Returns the current time in the format of [day-month-year hour:minute:second].
    """
    date = datetime.now()
    format_date = f"[{date.day}-{date.month}-{date.year} "
    format_time = f"{date.hour}:{date.minute}:{date.second}]"
    return format_date + format_time
