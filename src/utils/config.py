"Config module from Utils module"
# pylint: disable=no-name-in-module
# pylint: disable=cyclic-import
from typing import Any
from PyQt5.QtGui import QIcon
from PyQt5.QtCore import QSize

from . import ElementType, others, props


def set_config(element: ElementType, title: str | None = None, icon: QIcon | None = None,
              size: QSize | tuple[int, int] | None = None) -> None:
    """
    Sets the configuration of an element with ease.

    Args:
        element (ElementType): The element to set the configuration for.
        title (str | None, optional): The title to set for the element.
        icon (QIcon | None, optional): The icon to set for the element.
        size (QSize | tuple[int, int] | None, optional): The size to set for the element.

    Raises:
        TypeError: If size is not an instance of tuple or PyQt5.QtCore.QSize.
    """
    title = title or element.windowTitle()
    icon = icon or element.windowIcon()
    size = size or element.size() # type: ignore
    element.setWindowTitle(title)
    element.setWindowIcon(icon)
    if isinstance(size, tuple):
        element.setFixedSize(*size)
    elif isinstance(size, QSize):
        element.setFixedSize(size)
    else:
        raise TypeError(
            "'size' must be an instance of tuple or PyQt5.QtCore.QSize")


def set_multiple_config(element: ElementType, icon: QIcon, properties: list[Any] | None, **kwargs):
    """
    Set the configuration for multiple elements.

    Args::
        - element (ElementType): The main element to configure.
        - icon (QIcon): The icon to set for all elements.
        - properties (list[Any] | None): The list of elements to configure. 
            If None, all menu elements will be configured.
        - **kwargs: Additional arguments.
        
    Returns:
        None
    """
    if not properties:
        properties = [getattr(element, obj) for obj in props(
            element) if "menu" in obj and not "button" in obj]

    titles = ()
    sizes = ()
    default_title = kwargs["default_title"] if "default_title" in kwargs else None

    for prop in properties:
        titles += (prop.title, )
        sizes += (prop.size(), )

    if default_title:
        element.setWindowTitle(default_title)

    element.setWindowIcon(icon)

    for prop, title, size in zip(properties, titles, sizes):
        prop.setWindowTitle(title)
        prop.setWindowIcon(icon)
        prop.setFixedSize(size)
        others.update_window(prop)
