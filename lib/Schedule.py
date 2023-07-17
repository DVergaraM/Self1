import schedule
from typing import Callable
from lib.Notification import Notification
from core.SQL import Icons

sql = Icons()
conn = sql.create_connection()
with conn:
    Second_Brain = sql.get_path(sql.get_id("Second_Brain"))
del sql, conn


class Schedule:
    def __init__(self, time: str, task: Callable):
        schedule.every().day.at(time, "America/Bogota").do(task)


def run_pending():
    schedule.run_pending()


def get_next_run():
    return schedule.next_run()


def get_jobs():
    return schedule.get_jobs()


def stop():
    Stop = Notification("Second Brain", "Notifier", "Closing Notifier",
                        Second_Brain, None, "short")
    Stop.run()
    return schedule.clear()
