from utils import elementType, attribute, method


def setText(element: elementType, objs: dict[attribute, int | str] | tuple[attribute, int | str]) -> None:
    if isinstance(objs, tuple) and len(objs) == 2:
        attr, data = objs
        if (isinstance(attr, str) and (isinstance(data, int) or isinstance(data, str))) and hasattr(element, attr):
            obj = getattr(element, attr)
            obj.setText(f"{data}")
    elif isinstance(objs, dict) and all(isinstance(key, attribute) and (isinstance(value, int) or isinstance(value, str))for key, value in objs.items()):
        for key, value in objs.items():
            if hasattr(element, key):
                obj = getattr(element, key)
                obj.setText(f"{value}")
            else:
                continue
    else:
        raise TypeError(
            fr"'objs' and/or 'data' params must have the correct type")


def connect(element: elementType, objs: tuple[attribute, method] | dict[attribute, method]) -> None:
    if isinstance(objs, tuple) and len(objs) == 2:
        attr, meth = objs
        if (isinstance(attr, attribute) and isinstance(meth, method)) and hasattr(element, attr):
            obj = getattr(element, attr)
            obj.clicked.connect(meth)
    elif isinstance(objs, dict) and all(isinstance(key, attribute) and isinstance(value, method) for key, value in objs.items()):
        for attr, meth in objs.items():
            if hasattr(element, attr):
                obj = getattr(element, attr)
                obj.clicked.connect(meth)
            else:
                continue
    else:
        raise TypeError(
            fr"'obj' and/or 'method' params must have the correct type")


def textChangedConnect(element: elementType, objs: tuple[attribute, method] | dict[method, list[attribute]]) -> None:
    if isinstance(objs, tuple) and len(objs) == 2:
        attr, meth = objs
        if (isinstance(attr, attribute) and isinstance(meth, method)) and hasattr(element, attr):
            obj = getattr(element, attr)
            obj.textChanged.connect(meth)
    elif isinstance(objs, dict) and all(isinstance(meth, method) and isinstance(lst, list) for meth, lst in objs.items()):
        for meth, lst in objs.items():
            for attr in lst:
                if hasattr(element, attr):
                    obj = getattr(element, attr)
                    obj.textChanged.connect(meth)
                else:
                    continue
    else:
        raise TypeError(
            fr"'obj' and/or 'method' params must have the correct type")

def enableButton(element: elementType, data: dict[attribute, bool] | tuple[attribute, bool]) -> None:
    '''

    Args:
        element (elementType): object to check if it has the attributes
        data (dict[attribute, bool] | tuple[attribute, bool]): dictionary or tuple to assign values

    Raises:
        TypeError: 'data' param must have the correct type.
    '''    
    if isinstance(data, tuple) and len(data) == 2:
        attr, value = data # Unzip the data inside in two variables
        if hasattr(element, attr):
            attr = getattr(element, attr)
            attr.setEnabled(value)
    elif isinstance(data, dict) and (isinstance(k, str) and isinstance(v, bool) for k, v in data.items()):
        for attr, value in data.items(): # Loops in the items of the dict and assign values.
            if hasattr(element, attr):
                attr = getattr(element, attr)
                attr.setEnabled(value)
            else:
                continue
    else:
        raise TypeError(
            fr"'data' param must have the correct type")
