"Installs the required packages"
import os

def install_req():
    """
    Installs the required packages specified in the requirements.txt file.

    Raises:
        os.error: If an error occurs during the installation process.
    """
    try:
        if os.name == "nt":
            os.system("pip install -r requirements.txt")
            return None
        os.system("pip3 install -r requirements.txt")
        return None
    except os.error as excp:
        raise os.error(excp) from excp

install_req()
