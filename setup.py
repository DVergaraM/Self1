import os
import platform

try:
    if platform.system() == "Windows":
        os.system("pip install -r requirements.txt")
        return None
    else:
        os.system("pip3 install -r requirements.txt")
        return None
    return None
except os.OSError as excp:
    raise os.OSError(excp) from excp