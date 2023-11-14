"Utils Module"
from typing import Any, Callable, Literal, Type, TypeAlias, TypeVar
import os
from PyQt5.QtWidgets import QMainWindow, QWidget, QDialog, QLabel


class SubWindow(QWidget):
    """
    Subclass of `PyQt5.QtWidgets.QWidget`.
    A custom widget for creating sub-windows with a fixed size and a label.
    """
    def __init__(self, parent: Any = None, size: tuple[int, int] = None): # type: ignore
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


# pylint: disable=invalid-name
ElementType = TypeVar("ElementType", QMainWindow, SubWindow, QWidget, QDialog)
"""
`TypeVar` of:
- `PyQt5.QtWidgets.QMainWindow`
- `PyQt5.QtWidgets.QWidget`
- `PyQt5.QtWidgets.QDialog`
- `src.logic.SubWindow`
"""
# pylint: disable=invalid-name
attribute: TypeAlias = str
# pylint: disable=invalid-name
method: TypeAlias = Callable
# pylint: disable=invalid-name
cwd: Literal[r"\src\\"] = fr"{os.getcwd()}\src\\"  # type: ignore
# pylint: disable=invalid-name
otuple_str = TypeVar("otuple_str", tuple[str], tuple[tuple[str]], None)
# pylint: disable=invalid-name
cwddb: Literal[r"\src\login.db"] = fr"{os.getcwd()}\src\login.db" # type: ignore


def props(cls: Type[Any]) -> list[str]:  # type: ignore
    """
    Returns a list of the public properties of a class.

    Args:
        cls (Type[Any]): The class to inspect.

    Returns:
        list[str]: A list of the public properties of the class.
    """
    properties = [i for i in cls.__dict__.keys() if i[:1] != '_']
    return properties
