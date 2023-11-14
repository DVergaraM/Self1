"Utils Module"
from typing import Any, Callable, Literal, Type, Any, TypeAlias, TypeVar
import os
from PyQt5.QtWidgets import QMainWindow, QWidget, QDialog, QLabel


class SubWindow(QWidget):
    """
    Subclass of `PyQt5.QtWidgets.QWidget`.
    A custom widget for creating sub-windows with a fixed size and a label.
    """

    def __init__(self, parent: Any = None, size: tuple[int, int] = None): # type: ignore
        super(SubWindow, self).__init__(parent)
        if size is not None and len(size) == 2:
            self.setFixedSize(size[0], size[1])
        label = QLabel(self)
        label.setGeometry(0, 0, 760, 680)
        self.size

    @property
    def title(self):
        return self.windowTitle()


elementType = TypeVar("elementType", QMainWindow, SubWindow, QWidget, QDialog)
"""
`TypeVar` of:
- `PyQt5.QtWidgets.QMainWindow`
- `PyQt5.QtWidgets.QWidget`
- `PyQt5.QtWidgets.QDialog`
- `src.logic.SubWindow`
"""

attribute: TypeAlias = str
method: TypeAlias = Callable

cwd: Literal[r"\src\\"] = fr"{os.getcwd()}\src\\"  # type: ignore
otuple_str = TypeVar("otuple_str", tuple[str], tuple[tuple[str]], None)
cwddb: Literal[r"\src\login.db"] = fr"{os.getcwd()}\src\login.db" # type: ignore


def props(cls: Type[Any]) -> list[str]:  # type: ignore
    l = [i for i in cls.__dict__.keys() if i[:1] != '_']
    return l
