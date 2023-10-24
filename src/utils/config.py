"Config module from Utils module"
from PyQt5.QtGui import QIcon
from PyQt5.QtCore import QSize

from utils import elementType, others


def setConfig(element: elementType, title: str | None = None, icon: QIcon | None = None,
              size: QSize | tuple[int, int] | None = None) -> None:
    "Sets the config of an element with ease"
    if title is None:
        title = element.windowTitle()
    if icon is None:
        icon = element.windowIcon()
    if size is None:
        size = element.size()
    element.setWindowTitle(title)
    element.setWindowIcon(icon)
    if isinstance(size, tuple):
        if len(size) == 2:
            element.setFixedSize(size[0], size[1])
        else:
            element.setFixedSize(760, 680)
    elif isinstance(size, QSize):
        element.setFixedSize(size)
    elif size is None:
        pass
    else:
        raise TypeError(
            "'size' must be an instance of tuple or PyQt5.QtCore.QSize")


def setMultipleConfig(elements: tuple[elementType], titles: tuple[str], icon: QIcon,
                      sizes: tuple[QSize]) -> None:
    "Sets the config of multiple elements with ease"
    if len(elements) == len(titles) == len(sizes):
        for _, (element, title, size) in enumerate(zip(elements, titles, sizes)):
            element.setWindowTitle(title)
            element.setWindowIcon(icon)
            element.setFixedSize(size)
            others.updateWindow(element)
    else:
        raise ValueError(
            "'elements', 'titles' and 'sizes' parameters must have the same amount of items")
