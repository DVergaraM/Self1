#!C:/Users/DANIEL/AppData/Local/Programs/Python/Python311/python.exe
import sys
from typing import NoReturn
from core import STRAY_ICON
from lib.Pystray import Stray
# nuitka main.py --windows-icon-from-ico=images/Notion.png --follow-imports --onefile --low-memory --output-filename=MyNotion_No_Console.exe --disable-console
# C:\Users\DANIEL\AppData\Roaming\Microsoft\Windows\Start Menu\Programs\Startup


def main() -> NoReturn:

    stray = Stray("Second Brain", STRAY_ICON)
    stray.create_menu()
    sys.exit()


if __name__ == '__main__':
    main()
