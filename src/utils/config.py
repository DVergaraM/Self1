"Config module from Utils module"
# pylint: disable=no-name-in-module
# pylint: disable=cyclic-import
# pylint: disable=import-error
from typing import Any
from PyQt5.QtGui import QIcon
from PyQt5.QtCore import QSize

from . import ElementType, others, props


def set_config(element: ElementType, title: str | None = None, icon: QIcon | None = None,
              size: QSize | tuple[int, int] | None = None) -> None:
    """
    Sets the configuration of an element with ease.

    :param element: The element to set the configuration for.
    :type element: ElementType
    :param title: The title to set for the element, defaults to None.
    :type title: str, optional
    :param icon: The icon to set for the element, defaults to None.
    :type icon: QIcon, optional
    :param size: The size to set for the element, defaults to None.
    :type size: QSize or tuple[int, int], optional

    :return: None
    :rtype: None

    :raises TypeError: If size is not an instance of tuple or PyQt5.QtCore.QSize.
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


def set_multiple_config(element: ElementType, icon: QIcon,\
        properties: list[Any] | None = None, **kwargs):
    """
    Set the configuration for multiple elements.

    :param element: The main element to configure.
    :type element: ElementType
    :param icon: The icon to set for all elements.
    :type icon: QIcon
    :param properties: The list of elements to configure. If None, \
        all menu elements will be configured.
    :type properties: list[Any] | None
    :param **kwargs: Additional arguments.

    :return: None
    :rtype: None
    :raises KeyError: If 'default_title' is not present in kwargs.

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
        set_config(element, default_title, icon)
    else:
        set_config(element, icon=icon)

    for prop, title, size in zip(properties, titles, sizes):
        set_config(prop, title, icon, size)
        others.update_window(prop)
