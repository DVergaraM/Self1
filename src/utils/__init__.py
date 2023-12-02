"Utils Module"
# pylint: disable=invalid-name
# pylint: disable=no-name-in-module
# pylint: disable=import-error
from collections import deque
from typing import Any, Callable, Type, TypeAlias, TypeVar
import os
from PyQt5.QtWidgets import QMainWindow, QWidget, QDialog, QLabel


class SubWindow(QWidget):
    """
    Subclass of `PyQt5.QtWidgets.QWidget`.
    A custom widget for creating sub-windows with a fixed size and a label.
    """

    def __init__(self, parent: Any = None, size: tuple[int, int] | None = None):
        super().__init__(parent)
        if size is not None and len(size) == 2:
            self.setFixedSize(size[0], size[1])
        label = QLabel(self)
        label.setGeometry(0, 0, 760, 680)

    @property
    def title(self):
        """
        Returns the title of the window.
        """
        return self.windowTitle()

    @property
    def m_size(self):
        """
        Returns the size of the window.
        """
        return self.size()


ElementType = TypeVar("ElementType", QMainWindow, SubWindow, QWidget, QDialog)
"""
`TypeVar` of:
- `PyQt5.QtWidgets.QMainWindow`
- `PyQt5.QtWidgets.QWidget`
- `PyQt5.QtWidgets.QDialog`
- `src.logic.SubWindow`
"""
attribute: TypeAlias = str
method: TypeAlias = Callable
cwd = fr"{os.getcwd()}\src\\"
otuple_str = TypeVar("otuple_str", tuple[str, ...], None)


def props(cls: Type[Any], **kwargs) -> list[str] | deque[str]:
    """
    Returns a list of the public properties of a class.

    Args:
        cls (Type[Any]): The class to inspect.

    Returns:
        list[str]: A list of the public properties of the class.
    """
    if "deque" in kwargs and kwargs["deque"]:
        properties = deque([i for i in cls.__dict__.keys() if i[:1] != '_'])
    else:
        properties = [i for i in cls.__dict__.keys() if i[:1] != '_']
    return properties


__template__ = """
__description__

:param parameter_1: __description__
:type parameter_1: __type__

__end__
:return: __description__
:rtype: __type__
:raises __ErrorType__: __description__
"""
