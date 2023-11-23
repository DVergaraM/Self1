import os

def install_req():
    try:
        if os.name == "nt":
            os.system("pip install -r requirements.txt")
            return None
        os.system("pip3 install -r requirements.txt")
        return None
    except os.error as excp:
        raise os.error(excp) from excp

install_req()
