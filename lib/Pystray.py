import time
from datetime import datetime
import os
from pystray import Menu, MenuItem, Icon
import webbrowser as wb
import PIL.Image as Img
from .Threads import ThreadRPC, ThreadNotifier, ThreadNotion
from .RPC import RPC
from core.SQL import Urls
from core import image_path

aries = Img.open(image_path)

sql = Urls()
conn = sql.create_connection()
with conn:
    Duolingo = sql.get_url(sql.get_id("Duolingo"))
    Book = sql.get_url(sql.get_id("Book"))
    Edx = sql.get_url(sql.get_id("Edx"))

del (sql, conn)

class Stray:
    def __init__(self, icon_name: str, image: Img):
        self.icon_name: str = icon_name
        self.image: Img = image

    def create_menu(self):
        '''
        Creates the system tray with custom buttons and actions
        '''        
        icon = Icon(self.icon_name, self.image, menu=Menu(
            MenuItem("RPC", Menu(
                MenuItem("Start Status", self._helper),
                MenuItem("Stop Status", self._helper)
            )),
            MenuItem("Notifier", Menu(
                MenuItem("Start Pop-Ups", self._helper),
                MenuItem("Stop Pop-Ups", self._helper)
            )),
            MenuItem("Apps", Menu(
                MenuItem("Notion", self._helper),
                MenuItem("Code", self._helper),
                MenuItem("Life At", self._helper),
            )),
            MenuItem("Duolingo", self._helper),
            MenuItem("Edx", self._helper),
            MenuItem("Book", self._helper),
            MenuItem("Exit", self._helper)
        ), title="Second Brain")
        icon.run()

    def _helper(self, icon, item):
        '''

        Args:
            icon (Any): The current thread for the stray
            item (str): Button to be clicked by the user
        '''
        item = str(item)
        notifier = ThreadNotifier()
        rpc = ThreadRPC()
        notion = ThreadNotion()
        match item:
            case 'Start Status':
                date = datetime.now()
                print(
                    f"[{date.year}-{date.month}-{date.day} {date.hour}:{date.minute}:{date.second}] - Starting DiscordRPC...")

                RPC.connect()
                rpc.start()
            case 'Stop Status':
                date = datetime.now()
                print(
                    f"[{date.year}-{date.month}-{date.day} {date.hour}:{date.minute}:{date.second}] - Stopping DiscordRPC...")
                rpc.stop()

            case 'Start Pop-Ups':
                date = datetime.now()
                print(
                    f"[{date.year}-{date.month}-{date.day} {date.hour}:{date.minute}:{date.second}] - Starting Notifier...")
                notifier.start()

            case 'Stop Pop-Ups':
                date = datetime.now()
                print(
                    f"[{date.year}-{date.month}-{date.day} {date.hour}:{date.minute}:{date.second}] - Stopping Notifier...")
                notifier.stop()

            case 'Duolingo':
                date = datetime.now()
                print(
                    f"[{date.year}-{date.month}-{date.day} {date.hour}:{date.minute}:{date.second}] - Opening Duolingo...")
                wb.open(Duolingo)
            case 'Edx':
                date = datetime.now()
                print(
                    f"[{date.year}-{date.month}-{date.day} {date.hour}:{date.minute}:{date.second}] - Opening Youtube...")
                wb.open(Edx)
                # wb.open(self.playlists["C++"])
                os.system("code")
            case 'Book':
                date = datetime.now()
                print(
                    f"[{date.year}-{date.month}-{date.day} {date.hour}:{date.minute}:{date.second}] - Opening Notion and Freda...")
                wb.open(Book)
                os.system("FREDA_W10")
            case 'Notion':
                date = datetime.now()
                print(
                    f"[{date.year}-{date.month}-{date.day} {date.hour}:{date.minute}:{date.second}] - Opening Notion...")
                notion.start()
                # wb.open(self.urls["Notion"])
                # os.system("notion")
            case 'Life At':
                date = datetime.now()
                print(
                    f"[{date.year}-{date.month}-{date.day} {date.hour}:{date.minute}:{date.second}] - Opening LifeAt...")
                os.system("lifeat")
            case 'Code':
                date = datetime.now()
                print(
                    f"[{date.year}-{date.month}-{date.day} {date.hour}:{date.minute}:{date.second}] - Opening VSCode...")
                os.system("code")
            case 'Exit':
                date = datetime.now()
                print(
                    f"[{date.year}-{date.month}-{date.day} {date.hour}:{date.minute}:{date.second}] - Closing Stray...")
                time.sleep(5)
                icon.stop()
