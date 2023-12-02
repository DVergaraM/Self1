"Setters module from Utils module"
# pylint: disable=no-name-in-module
from typing import TypeAlias
from collections import deque
from utils import ElementType, attribute, method


DictListType: TypeAlias = dict[method, list[attribute] | deque[attribute]]

def set_text(element: ElementType,
            objs: dict[attribute, int | str] | tuple[attribute, int | str]) -> None:
    """
    Sets the text of a QLineEdit with some value.

    :param element: The QLineEdit element to set the text on.
    :type element: ElementType
    :param objs: A dictionary or tuple containing the attribute and value to set.
    :type objs: Union[dict[attribute, int | str], tuple[attribute, int | str]]

    :return: None
    :rtype: None

    :raises TypeError: If 'objs' and/or 'data' params have the incorrect type.
    """
    if isinstance(objs, tuple) and len(objs) == 2:
        attr, data = objs
        if (isinstance(attr, str) and isinstance(data, (int, str)))\
                and hasattr(element, attr):
            obj = getattr(element, attr)
            obj.setText(f"{data}")
    elif isinstance(objs, dict) and all(isinstance(key, attribute) and
                                        isinstance(value, (int, str))\
                                            for key, value in objs.items()):
        for key, value in objs.items():
            if hasattr(element, key):
                obj = getattr(element, key)
                obj.setText(f"{value}")
            else:
                continue
    else:
        raise TypeError(
            "'objs' and/or 'data' params must have the correct type")


def connect(element: ElementType, objs: tuple[attribute, method] | dict[attribute, method]) -> None:
    """
    Connects a button or a group of buttons with a method or a group of methods.

    :param element: Element where the attributes are going to be.
    :type element: ElementType
    :param objs: The button or group of buttons to connect with the method or group of methods to.
    :type objs: tuple[attribute, method] | dict[attribute, method]

    :return: None
    :rtype: None

    :raises TypeError: If the 'objs' parameter is not a tuple or a dictionary, \
        or if it is a tuple but does not have exactly two elements, \
            or if it is a dictionary but not all its keys are of type 'attribute' \
                and all its values are of type 'method'.
    """
    if isinstance(objs, tuple) and len(objs) == 2:
        attr, meth = objs
        if (isinstance(attr, attribute) and isinstance(meth, method)) and hasattr(element, attr):
            obj = getattr(element, attr)
            obj.clicked.connect(meth)
    elif isinstance(objs, dict) and all(isinstance(key, attribute) and
                                        isinstance(value, method) for key, value in objs.items()):
        for attr, meth in objs.items():
            if hasattr(element, attr):
                obj = getattr(element, attr)
                obj.clicked.connect(meth)
            else:
                continue
    else:
        raise TypeError("'obj' and/or 'method' params must have the correct type")


def text_changed_connect(element: ElementType,
                       objs: tuple[attribute, method] | DictListType) -> None:
    """
    Connects a button with a method depending on a QLineEdit.

    :param element: The element to connect the method to.
    :type element: ElementType
    :param objs: A tuple or dictionary containing the attributes and methods to connect.
    :type objs: tuple[attribute, method] | dict[method, list[attribute]]

    :return: None
    :rtype: None
    
    :raises TypeError: If 'objs' and/or 'method' params must have the correct type.
    """
    if isinstance(objs, tuple) and len(objs) == 2:
        attr, meth = objs
        if (isinstance(attr, attribute) and isinstance(meth, method)) and hasattr(element, attr):
            obj = getattr(element, attr)
            obj.textChanged.connect(meth)
    elif isinstance(objs, dict) and all(isinstance(meth, method) and
            isinstance(lst, (list, deque)) for meth, lst in objs.items()):
        for meth, lst in objs.items():
            for attr in lst:
                if hasattr(element, attr):
                    obj = getattr(element, attr)
                    obj.textChanged.connect(meth)
                else:
                    continue
    else:
        raise TypeError("'obj' and/or 'method' params must have the correct type")


def enable_button(element: ElementType,
                 data: dict[attribute, bool] | tuple[attribute, bool]) -> None:
    '''
    Enables or disables a button

    :param element: Object to check if it has the attributes
    :type element: ElementType
    :param data: Dictionary or tuple to assign values
    :type data: dict[attribute, bool] | tuple[attribute, bool]

    :raises TypeError: 'data' param must have the correct type.

    :return: None
    :rtype: None
    '''
    if isinstance(data, tuple) and len(data) == 2:
        attr, value = data  # Unzip the data inside in two variables
        if hasattr(element, attr):
            attr = getattr(element, attr)
            attr.setEnabled(value)
    elif isinstance(data, dict) and\
            (isinstance(k, str) and isinstance(v, bool) for k, v in data.items()):
        for attr, value in data.items():  # Loops in the items of the dict and assign values.
            if hasattr(element, attr):
                attr = getattr(element, attr)
                attr.setEnabled(value)
            else:
                continue
    else:
        raise TypeError(
            "'data' param must have the correct type")
