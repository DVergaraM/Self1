from typing import Any, Callable, TypeAlias, TypeVar
import os
from PyQt5.QtWidgets import QMainWindow, QWidget, QDialog, QLabel

class SubWindow(QWidget):
    "Subclass of `PyQt5.QtWidgets.QWidget`"
    def __init__(self, parent: Any = None, size: tuple[int, int] = None):
        super(SubWindow, self).__init__(parent)
        if size is not None and len(size) == 2:
            self.setFixedSize(size[0], size[1])
        label = QLabel(self)
        label.setGeometry(0, 0, 760, 680)


elementType = TypeVar("elementType", QMainWindow, SubWindow, QWidget, QDialog)
"""
`TypeVar` of:
- `PyQt5.QtWidgets.QMainWindow`
- `PyQt5.QtWidgets.QWidget`
- `PyQt5.QtWidgets.QDialog`
- `src.logic.SubWindow`
"""

attribute = TypeVar("attribute", str)
method = TypeVar("method", Callable)

cwd = fr"{os.getcwd()}\src\\"
otuple_str = TypeVar("otuple_str", tuple[str], tuple[tuple[str]], None)
cwddb = fr"{os.getcwd()}\src\login.db"