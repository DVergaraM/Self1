from typing import Callable as _Callable
from sqlite3 import Connection as _Connection
from . import Notification, Schedule, run_pending
from core.SQL import Icons, Urls

sql = Icons()
conn = sql.create_connection()
with conn:
    Duolingo = sql.get_path(sql.get_id("Duolingo"))
    CPP = sql.get_path(sql.get_id("CPP"))
    Book = sql.get_path(sql.get_id("Book"))
    Second_Brain = sql.get_path(sql.get_id("Second_Brain"))
    Zoom = sql.get_path(sql.get_id("Zoom"))
    Edx = sql.get_path(sql.get_id("Edx"))
del (sql, conn)

sql = Urls()
conn = sql.create_connection()
with conn:
    Duo_URL = sql.get_url(sql.get_id("Duolingo"))
    CPP_URL = sql.get_url(sql.get_id("CPP"))
    Book_URL = sql.get_url(sql.get_id("Book"))
    Zoom_URL = sql.get_url(sql.get_id("Zoom"))
    Edx_URL = sql.get_url(sql.get_id("Edx"))

del (sql, conn)


Duolingo_Task: Notification = Notification("Second Brain", "Habit Tracker",
                                           "Time to practice Japanese!", Duolingo, Duo_URL)

Programming_Task: Notification = Notification("Second Brain", "Habit Tracker",
                                              "Time to practice C++ Skills!", CPP, CPP_URL)

Book_Task: Notification = Notification("Second Brain", "Habit Tracker",
                                       "Time to read 'How to Talk to Anyone - Leil Lowndes'", Book, Book_URL)

Notifier_Enabled: Notification = Notification("Second Brain", "Notifier",
                                              "Notifier pop-ups enabled", Second_Brain, None)

UR_Zoom: Notification = Notification("Second Brain", "Zoom Meeting",
                                     "Unete a la reunión del PFA", Zoom, Zoom_URL)

Edx_Course: Notification = Notification("Second Brain", "EDx Course",
                                        "Follow up with the AI course", Edx, Edx_URL)


Tasks: dict[str, _Callable] = {
    "Duolingo": Duolingo_Task.run,
    "Edx Course": Edx_Course.run,
    "Book": Book_Task.run,
    # "Zoom": UR_Zoom.run
}
Error: Notification = Notification("Second Brain", "Notifier",
                                   "Runtime Error | Warning", Second_Brain, None)


def main() -> None:
    try:
        Schedule("20:00", Tasks["Duolingo"])
        # Schedule("09:00", Tasks["Zoom"])
        Schedule("10:00", Tasks["Edx Course"])
        Schedule("15:00", Tasks["Book"])

        Notifier_Enabled.run()

        while True:
            run_pending()
    except (RuntimeError or RuntimeWarning):
        Error.run()
