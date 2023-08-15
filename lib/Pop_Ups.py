from typing import Callable as _Callable
from . import Notification, Schedule, run_pending
from core.SQL import Icons, Urls

sql = Icons()
conn = sql.create_connection()
with conn:
    all_Icons = sql.get_all()
del (sql, conn)

sql = Urls()
conn = sql.create_connection()
with conn:
    all_Urls = sql.get_all()

del (sql, conn)


Duolingo_Task: Notification = Notification("Second Brain", "Habit Tracker",
                                           "Time to practice Japanese!", all_Icons[1][2], all_Urls[1][2])

Programming_Task: Notification = Notification("Second Brain", "Habit Tracker",
                                              "Time to practice C++ Skills!", all_Icons[0][2], all_Urls[0][2])

Book_Task: Notification = Notification("Second Brain", "Habit Tracker",
                                       "Time to read 'How to Talk to Anyone - Leil Lowndes'", all_Icons[2][2], all_Urls[2][2])

Notifier_Enabled: Notification = Notification("Second Brain", "Notifier",
                                              "Notifier pop-ups enabled", all_Icons[7][2], None)

UR_Zoom: Notification = Notification("Second Brain", "Zoom Meeting",
                                     "Unete a la reunión del PFA", all_Icons[4][2], all_Urls[4][2])

Edx_Course: Notification = Notification("Second Brain", "EDx Course",
                                        "Follow up with the AI course", all_Icons[5], all_Urls[5][2])


Tasks: dict[str, _Callable[[], None]] = {
    "Duolingo": Duolingo_Task.run,
    "Edx Course": Edx_Course.run,
    "Book": Book_Task.run,
    # "Zoom": UR_Zoom.run
}
Error: Notification = Notification("Second Brain", "Notifier",
                                   "Runtime Error | Warning", all_Icons[7][2], None)


def main() -> None:
    try:
        Schedule("20:00", Tasks["Duolingo"])
        # Schedule("09:00", Tasks["Zoom"])
        Schedule("10:00", Tasks["Edx Course"])
        Schedule("15:00", Tasks["Book"])

        Notifier_Enabled.run()

        run_pending()
    except (RuntimeError or RuntimeWarning):
        Error.run()
