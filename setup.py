import os
import platform

try:
    if platform.system() == "Windows":
        os.system("pip install -r requirements.txt")
    else:
        os.system("pip3 install -r requirements.txt")
except os.error as excp:
    raise os.error(excp) from excp
