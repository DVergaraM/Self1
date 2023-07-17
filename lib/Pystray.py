import time
from datetime import datetime
import os
from typing import Any
from pystray import Menu, MenuItem, Icon
import webbrowser as wb
import PIL.Image as Img
from lib.Threads import ThreadRPC, ThreadNotifier, ThreadNotion
from lib.RPC import RPC
from core.SQL import Urls

aries = Img.open(
    r"C:\Users\DANIEL\Desktop\rqaw\Documentos\Dev\Python\Self\images\aries.png")

sql = Urls()
conn = sql.create_connection()
with conn:
    Duolingo = sql.get_url(sql.get_id("Duolingo"))
    Book = sql.get_url(sql.get_id("Book"))
    Edx = sql.get_url(sql.get_id("Edx"))


class Stray:
    def __init__(self, icon_name: str, image: Img):     
        self.icon_name: str = icon_name
        self.image: Img = image

    def create_menu(self):        
        icon = Icon(self.icon_name, self.image, menu=Menu(
            MenuItem("RPC", Menu(
                MenuItem("Start Status", self.helper),
                MenuItem("Stop Status", self.helper)
            )),
            MenuItem("Notifier", Menu(
                MenuItem("Start Pop-Ups", self.helper),
                MenuItem("Stop Pop-Ups", self.helper)
            )),
            MenuItem("Apps", Menu(
                MenuItem("Notion", self.helper),
                MenuItem("Code", self.helper),
                MenuItem("Life At", self.helper),
            )),
            MenuItem("Duolingo", self.helper),
            MenuItem("Edx", self.helper),
            MenuItem("Book", self.helper),
            MenuItem("Exit", self.helper)
        ), title="Second Brain")
        icon.run()

    def helper(self, icon, item):
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
