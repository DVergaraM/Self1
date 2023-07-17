import pypresence
import struct
from lib.Notification import Notification
import time
from pypresence import Presence
from random import choice
from core.SQL import Activities, Icons


sql = Icons()
conn = sql.create_connection()
with conn:
    Discord = sql.get_path(sql.get_id("Discord"))

del sql, conn

__all__ = ["mainRPC", "stopRPC"]

RPC = Presence('1126179074130321508')

Pop = Notification("Second Brain", "Notifier",
                   "Discord RPC Enabled", Discord, None, 'short')

cwt = time.time()

Error = Notification("Second Brain", "Notifier",
                     "Discord Not Found | Server Error | Runtime Error | Warning", Discord, None, 'short')

Stop = Notification("Second Brain", "Notifier", "Closing Discord RPC",
                    Discord, None, "short")

status = False

""" {
        "Image_URL": "https://i.imgur.com/J6LeoUb.png",
        "Description": "@DVergaraM",
        "Small_text": "DVergaraM"
    },
    {
        "Image_URL": "https://i.imgur.com/PstvzgE.png", 
        "Description": "Programming a Notifier",
        "Small_text": "Learning CPython"
    },
    {
        "Image_URL": "https://i.imgur.com/M6yBwxS.png",
        "Description": "@dan.v.m_137",
        "Small_text": "@dan.v.m_137"
    }"""


activities_dict: dict[int, dict] = {
    0: {},
    1: {},
    2: {},
}
sql = Activities()
conn = sql.create_connection()
with conn:
    for key, value in activities_dict.items():
        activities_dict[key]["Image_URL"] = sql.get_imageurl(key+1)
        activities_dict[key]["Description"] = sql.get_description(key+1)
        activities_dict[key]["Small_text"] = sql.get_smalltext(key+1)


def mainRPC():
    try:
        global status
        Pop.run()
        while True:
            current_activity = choice(activities_dict)
            detail = "True progress comes not through action, but through awakening."

            # https://i.imgur.com/N1fuUn8.jpg
            try:
                RPC.update(state=current_activity["Description"], details=detail,
                           start=cwt, large_image="https://i.imgur.com/N1fuUn8.jpg",
                           large_text="Second Brain", small_image=current_activity["Image_URL"],
                           small_text=current_activity["Small_text"],
                           buttons=[{'label': "Linktree", 'url': "https://linktr.ee/dvergaram"}])
                time.sleep(5)
                if status:
                    break
            except KeyboardInterrupt:
                pass

    except (pypresence.exceptions.DiscordNotFound, struct.error, pypresence.exceptions.ServerError, RuntimeError or RuntimeWarning) as e:
        Error.run()
        time.sleep(2)
        print(e)
        return

    except (KeyboardInterrupt, ValueError):
        pass


def stopRPC():
    try:
        global status
        status = True
        time.sleep(2)
        RPC.close()
        Stop.run()
    except:
        Error.run()
        return
