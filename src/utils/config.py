"Config module from Utils module"
from PyQt5.QtGui import QIcon
from PyQt5.QtCore import QSize

from utils import elementType, others


def setConfig(element: elementType, title: str | None = None, icon: QIcon | None = None,
              size: QSize | tuple[int, int] | None = None) -> None:
    "Sets the config of an element with ease"
    title = title or element.windowTitle()
    icon = icon or element.windowIcon()
    size = size or element.size()
    element.setWindowTitle(title)
    element.setWindowIcon(icon)
    if isinstance(size, tuple):
        element.setFixedSize(*size)
    elif isinstance(size, QSize):
        element.setFixedSize(size)
    else:
        raise TypeError(
            "'size' must be an instance of tuple or PyQt5.QtCore.QSize")


def setMultipleConfig(elements: tuple[elementType], titles: tuple[str], icon: QIcon,
                      sizes: tuple[QSize]) -> None:
    "Sets the config of multiple elements with ease"
    if len(elements) != len(titles) != len(sizes):
        raise ValueError(
            "'elements', 'titles' and 'sizes' parameters must have the same amount of items")
    for element, title, size in zip(elements, titles, sizes):
        element.setWindowTitle(title)
        element.setWindowIcon(icon)
        element.setFixedSize(size)
        others.updateWindow(element)
    return None
