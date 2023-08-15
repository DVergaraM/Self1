import pypresence
import struct
from typing import Any as _Any
from . import Notification
import time
from pypresence import Presence, DiscordNotFound, DiscordError
from random import choice
from core import PRESENCE_ID, dict_tuple, ICON
from core.SQL import Icons


_sql = Icons()
_conn = _sql.create_connection()
with _conn:
    Discord = _sql.get_path(_sql.get_id("Discord"))

del _sql, _conn

try:
    rpc = Presence(PRESENCE_ID)
    rpc.connect()
except DiscordNotFound or DiscordError:
    pass

Pop = Notification("Second Brain", "Notifier",
                   "Discord RPC Enabled", Discord, None, 'short')

cwt = time.time()

Error = Notification("Second Brain", "Notifier",
                     "Discord Not Found | Server Error | Runtime Error | Warning", Discord, None, 'short')

Stop = Notification("Second Brain", "Notifier", "Closing Discord RPC",
                    Discord, None, "short")

_status = False
"Something"


""" _activities_dict: dict[int, dict] = {
    0: {},
    1: {},
    2: {},
} """

_activities_dict_1: dict[int, dict[str, str]] = {
    0: {
        "Image_URL": "https://i.imgur.com/J6LeoUb.png",
        "Description": "@DVergaraM",
        "Small_text": "DVergaraM"
    },
    1: {
        "Image_URL": "https://i.imgur.com/PstvzgE.png",
        "Description": "Programming a Notifier",
        "Small_text": "Learning CPython"
    },
    2: {
        "Image_URL": "https://i.imgur.com/VFpxiwx.png",
        "Description": "@dvergaram_",
        "Small_text": "@dvergaram_"
    }
}

_activities_tuple: tuple[tuple[str]] = (("https://i.imgur.com/J6LeoUb.png", "@DVergaraM", "DVergaraM"),
                                        ("https://i.imgur.com/PstvzgE.png",
                                         "Programming a Notifier", "Learning CPython"),
                                        ("https://i.imgur.com/VFpxiwx.png", "@dvergaram_", "@dvergaram_"))
"Database like tuple"


def update_rpc(activities: dict_tuple) -> None:
    global _status
    while True:
        current_activity = choice(activities)
        detail = "True progress comes not through action, but through awakening."

        try:
            if isinstance(activities, dict):
                rpc.update(state=current_activity["Description"], details=detail,
                           start=cwt, large_image=ICON,
                           large_text="Second Brain", small_image=current_activity["Image_URL"],
                           small_text=current_activity["Small_text"],
                           buttons=[{'label': "Linktree", 'url': "https://linktr.ee/dvergaram"}])

            elif isinstance(activities, tuple):
                rpc.update(state=current_activity[1], details=detail,
                           start=cwt, large_image=ICON,
                           large_text="Second Brain", small_image=current_activity[0],
                           small_text=current_activity[2],
                           buttons=[{'label': "Linktree", 'url': "https://linktr.ee/dvergaram"}])
            else:
                raise ValueError("'activities' must be a dict or a tuple.")

            time.sleep(5)
            if _status:
                break
        except KeyboardInterrupt:
            pass


def mainRPC() -> None:
    try:
        Pop.run()
        update_rpc(_activities_tuple)

    except (pypresence.exceptions.DiscordNotFound, struct.error, pypresence.exceptions.ServerError, RuntimeError or RuntimeWarning, RuntimeError, RuntimeWarning) as ExceptionV1:
        Error.run()
        time.sleep(2)
        raise ExceptionV1()
        # print(e)
        return

    except (KeyboardInterrupt, ValueError):
        pass


def stopRPC() -> None:
    try:
        global _status
        _status = True
        time.sleep(2)
        rpc.close()
        Stop.run()
    except:
        Error.run()
        return
