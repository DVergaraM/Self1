from winotify import Notification as Notifier
from winotify import audio
from datetime import datetime
from typing import Callable
import schedule as _schedule
from core.SQL import Icons


_sql = Icons()
_conn = _sql.create_connection()
with _conn:
    Second_Brain = _sql.get_path(_sql.get_id("Second_Brain"))
del _sql, _conn


class Notification(Notifier):
    def __init__(self, app_id: str, title: str, msg: str, icon: str, launch: str | Callable | None = "",  duration='long', sound=audio.Reminder):
        super().__init__(app_id, title, msg, icon, duration)
        self.set_audio(sound, loop=False)
        if launch is not None:
            self.add_actions("Click Here!", launch)

    def run(self):
        self.show()
        date = datetime.now()
        print(f"[{date.year}-{date.month}-{date.day} {date.hour}:{date.minute}:{date.second}] - Task: '{self.msg}'")


class Schedule:
    def __init__(self, time: str, task: Callable):
        _schedule.every().day.at(time, "America/Bogota").do(task)


def run_pending():
    _schedule.run_pending()


def get_next_run():
    return _schedule.next_run()


def get_jobs():
    return _schedule.get_jobs()


def stop():
    _Stop = Notification("Second Brain", "Notifier", "Closing Notifier",
                         Second_Brain, None, "short")
    _Stop.run()
    return _schedule.clear()
