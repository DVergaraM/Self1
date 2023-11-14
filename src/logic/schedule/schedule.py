import pytz
import schedule as _schedule
import time as tm
import re
import webbrowser as wb
import validators
from typing import Callable, Tuple, Any, Union, Iterator
from logic import MQThread


class Schedule:
    def __init__(self, timezone: Union[str, pytz.BaseTzInfo] = "America/Bogota", **kwargs) -> None:
        self._tasks: list[tuple] = []
        self._amount_tasks = 0
        self.notifier = kwargs["notifier"] if "notifier" in kwargs else None
        self.start_thread = kwargs["start_thread"] if "start_thread" in kwargs else None
        if isinstance(timezone, str):
            self.timezone = pytz.timezone(timezone)
        elif isinstance(timezone, pytz.BaseTzInfo):
            self.timezone = timezone
        else:
            raise ValueError(
                "'timezone' is not an instance of str or pytz.BaseTzInfo")

    @property
    def tasks(self):
        return self._tasks

    def add_task(self, time: str, method: Union[Callable, str], args: Tuple[Any] | list[Any] = None) -> bool: # type: ignore
        if isinstance(method, Callable) and self.is_time(time):
            job = _schedule.every().day.at(time).do(
                self.run_task, method, args if args else [])
            self._tasks.append((time, method, job))
            self._amount_tasks += 1
            print("Added method")
            return True
        if isinstance(method, str) and self.is_time(time):
            job = _schedule.every().day.at(time).do(
                self.run_task, self.open_web, [method])
            self._tasks.append((time, self.open_web, job))
            self._amount_tasks += 1
            print("Added URL")
            return True
        return False

    def remove_task(self, method_name: Union[str, Callable]) -> bool:
        for t in self._tasks:
            if isinstance(method_name, Callable):
                if t[1].__name__ == method_name.__name__:
                    _schedule.cancel_job(t[2])
                    self._tasks.remove(t)
                    self._amount_tasks -= 1
                    return True
            elif isinstance(method_name, str):
                if t[1] == method_name:
                    _schedule.cancel_job(t[2])
                    self._tasks.remove(t)
                    self._amount_tasks -= 1
                    return True
            else:
                continue
        else:
            print("Still", self._tasks, self._amount_tasks)
            return False

    def run_task(self, method: Callable, args: list | tuple) -> None:
        method(*args)
        tm.sleep(1.25)
        self.remove_task(method)

    def total_tasks(self) -> int:
        return len(self._tasks)

    def has_tasks(self) -> bool:
        return len(self._tasks) != 0

    def start(self) -> None:
        if self.notifier and isinstance(self.notifier, Callable):
            self.notifier()
        if self.notifier and isinstance(self.notifier, MQThread):
            self.notifier.start()
        while self._amount_tasks != 0:
            _schedule.run_pending()
            tm.sleep(1)

    def stop(self) -> None:
        _schedule.clear()

    @staticmethod
    def open_web(url: str) -> bool:
        try:
            if validators.url(url): # type: ignore
                success = wb.open(url)
                print("Opening URL...")
                if success:
                    print("Successfully opened.")
                    return success
                return success
            return False
        except wb.Error as excp:
            raise wb.Error(excp) from excp
    
    @staticmethod
    def is_time(time: str) -> bool:
        pattern = r"^[0-9]{2}:[0-9]{2}$"
        return bool(re.match(pattern, time))

    def __int__(self) -> int:
        return self.total_tasks()

    def __bool__(self) -> bool:
        return self.has_tasks()

    def __str__(self) -> str:
        return " ".join([str(task) for task in self._tasks])

    def __iter__(self) -> Iterator:
        return iter(self._tasks)

    def __next__(self) -> Any:
        return next(iter(self._tasks))
