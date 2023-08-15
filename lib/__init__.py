from winotify import Notification as _Notifier
from winotify import audio as sounds
from datetime import datetime as _datetime
from typing import (Optional as _Optional,
                    Callable as _Callable, List as _List)
import schedule as _schedule
from core.SQL import Icons


_sql = Icons()
_conn = _sql.create_connection()
with _conn:
    Second_Brain = _sql.get_path(_sql.get_id("Second_Brain"))
del _sql, _conn


class Notification(_Notifier):
    def __init__(self, app_id: str = "Second Brain", title: str = "Notifier", msg: str = "", icon: str = "", launch: str | _Callable | None = "",  duration='long', sound=sounds.Reminder) -> None:
        super().__init__(app_id, title, msg, icon, duration)
        self.set_audio(sound, loop=False)
        if launch is not None:
            self.add_actions("Click Here!", launch)

    def run(self) -> None:
        self.show()
        date = _datetime.now()
        print(f"[{date.year}-{date.month}-{date.day} {date.hour}:{date.minute}:{date.second}] - Task: '{self.msg}'")


class Schedule:
    def __init__(self, time: str, task: _Callable, tz: _Optional[str] = "America/Bogota") -> None:
        _schedule.every().day.at(time, tz).do(task)


def run_pending() -> None:
    while True:
        _schedule.run_pending()


def get_next_run() -> (_datetime | None):
    return _schedule.next_run()


def get_jobs() -> _List[_schedule.Job]:
    return _schedule.get_jobs()


def stop() -> None:
    _stop = Notification("Second Brain", "Notifier", "Closing Notifier",
                         Second_Brain, None, "short")
    _stop.run()
    return _schedule.clear()
