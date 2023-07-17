from lib.Schedule import Schedule, run_pending
from lib.Notification import Notification
from core.SQL import Icons, Urls

sql = Icons()
conn = sql.create_connection()
with conn:
    ids = [sql.get_id("Duolingo"), sql.get_id("CPP"), sql.get_id(
        "Book"), sql.get_id("Second_Brain"), sql.get_id("Zoom"), sql.get_id("Edx")]
    Duolingo = sql.get_path(ids[0])
    CPP = sql.get_path(ids[1])
    Book = sql.get_path(ids[2])
    Second_Brain = sql.get_path(ids[3])
    Zoom = sql.get_path(ids[4])
    Edx = sql.get_path(ids[5])
del sql, conn

sql = Urls()
conn = sql.create_connection()
with conn:
    Duo_URL = sql.get_url(sql.get_id("Duolingo"))
    CPP_URL = sql.get_url(sql.get_id("CPP"))
    Book_URL = sql.get_url(sql.get_id("Book"))
    Zoom_URL = sql.get_url(sql.get_id("Zoom"))
    Edx_URL = sql.get_url(sql.get_id("Edx"))


Duolingo_Task = Notification("Second Brain", "Habit Tracker",
                             "Time to practice Japanese!", Duolingo, Duo_URL)

Programming_Task = Notification("Second Brain", "Habit Tracker",
                                "Time to practice C++ Skills!", CPP, CPP_URL)

Book_Task = Notification("Second Brain", "Habit Tracker",
                         "Time to read 'How to Talk to Anyone - Leil Lowndes'", Book, Book_URL)

Notifier_Enabled = Notification("Second Brain", "Notifier",
                                "Notifier pop-ups enabled", Second_Brain, None)

UR_Zoom = Notification("Second Brain", "Zoom Meeting",
                       "Unete a la reunión del PFA", Zoom, Zoom_URL)

Edx_Course = Notification("Second Brain", "EDx Course",
                          "Follow up with the AI course", Edx, Edx_URL)


Tasks = {
    "Duolingo": Duolingo_Task.run,
    "Edx Course": Edx_Course.run,
    "Book": Book_Task.run,
    # "Zoom": UR_Zoom.run
}
Error = Notification("Second Brain", "Notifier",
                     "Runtime Error | Warning", Second_Brain, None)


def main():
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
