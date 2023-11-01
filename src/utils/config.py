"Config module from Utils module"
from PyQt5.QtGui import QIcon
from PyQt5.QtCore import QSize

from utils import elementType, others


def setConfig(element: elementType, title: str | None = None, icon: QIcon | None = None,
              size: QSize | tuple[int, int] | None = None) -> None:
    """
    Sets the configuration of an element with ease.

    Args:
        element (elementType): The element to set the configuration for.
        title (str | None, optional): The title to set for the element. Defaults to None.
        icon (QIcon | None, optional): The icon to set for the element. Defaults to None.
        size (QSize | tuple[int, int] | None, optional): The size to set for the element. Defaults to None.

    Raises:
        TypeError: If size is not an instance of tuple or PyQt5.QtCore.QSize.
    """
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
    """
    Sets the configuration of multiple elements with ease.

    Args:
        elements (tuple[elementType]): A tuple of elements to be configured.
        titles (tuple[str]): A tuple of titles to be set for each element.
        icon (QIcon): The icon to be set for each element.
        sizes (tuple[QSize]): A tuple of sizes to be set for each element.

    Raises:
        ValueError: If the length of 'elements', 'titles' and 'sizes' parameters are not equal.

    Returns:
        None
    """
    if len(elements) != len(titles) != len(sizes):
        raise ValueError(
            "'elements', 'titles' and 'sizes' parameters must have the same amount of items")
    for element, title, size in zip(elements, titles, sizes):
        element.setWindowTitle(title)
        element.setWindowIcon(icon)
        element.setFixedSize(size)
        others.updateWindow(element)
    return None
