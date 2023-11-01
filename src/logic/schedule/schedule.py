from typing import Callable, Any, Iterator, Union, Tuple
import os
from datetime import datetime
import time as tm
import webbrowser as wb
import pytz
import validators
import schedule as _schedule


class Schedule:
    """
    Class that allows the user to schedule tasks according to a time and timezone
    """
    _running = False

    def __init__(self, timezone: str | pytz.BaseTzInfo = "America/Bogota") -> None:
        '''

        Args:
            timezone (str, pytz.BaseTzInfo, opt): Current timezone. Defaults to`America/Bogota`.
        '''
        self._tasks: list[tuple] = []
        self._amount_tasks = 0
        if isinstance(timezone, str):
            self.timezone = pytz.timezone(timezone)  # type: ignore
        elif isinstance(timezone, pytz.BaseTzInfo):
            self.timezone = timezone
        else:
            raise ValueError(
                "'timezone' is not an instance of str or pytz.BaseTzInfo")
        return None

    @property
    def tasks(self):
        """
        Structure: (time, method name | url, Job Object)
        Example: 
        ```python
            def say_hello():
                print("Hello World!")
            schedule = Schedule()
            schedule.add_task("12:00", say_hello)
            print(schedule.tasks) # ("12:00", "say_hello", Job Object)
        ```
        """
        return self._tasks

    def add_task(self, time: str, method: Union[Callable, str], args: Tuple[Any] = None) -> bool:
        "Adds a task to the list and runs it at the time setted"
        if isinstance(method, Callable):
            job = _schedule.every().day.at(time).do(self.run_task, method,
                                                    args if args else [], self.remove_task)
            self._tasks.append((time, method.__name__, job))
            self._amount_tasks += 1
            return True
        elif isinstance(method, str):
            job = _schedule.every().day.at(time).do(
                self.run_task, self.open_web, [method], self.remove_task)
            self._tasks.append((time, method, job))
            self._amount_tasks += 1
            return True
        return False

    def remove_task(self, method_name: str) -> bool:
        "Removes a task from the list according to the url or name"
        for t in self._tasks:
            if t[1].__name__ == method_name:
                _schedule.cancel_job(t[2])
                self._tasks.remove(t)
                self._amount_tasks -= 1
                return True
            elif validators.url(t[1]) and t[1] == method_name:
                _schedule.cancel_job(t[2])
                self._tasks.remove(t)
                self._amount_tasks -= 1
                return True
        return False

    def total_tasks(self) -> int:
        "Gives the amount of items in  the list"
        return len(self._tasks)

    def has_tasks(self) -> bool:
        "Checks if the list has items or not"
        return len(self._tasks) != 0

    def start(self) -> None:
        "Runs the tasks that are pending."
        try:
            self._running = True
            while self._amount_tasks != 0:
                _schedule.run_pending()
                tm.sleep(1)
            return None
        except _schedule.ScheduleError as excp:
            raise _schedule.ScheduleError(excp) from excp

    def run_task(self, method: Callable, args: list | tuple, callback: Callable):
        "Runs a task with its arguments and run a callback"
        method(*args)
        self._tasks = list(
            filter(lambda task: task[1] != method.__name__, self._tasks))
        self._amount_tasks -= 1
        callback(method.__name__)

    def stop(self) -> None:
        "Clears the tasks in Queue"
        self._running = False
        try:
            _schedule.clear()
            return None
        except _schedule.ScheduleError as excp:
            raise _schedule.ScheduleError(excp) from excp

    @staticmethod
    def open_web(url: str) -> bool:
        try:
            if validators.url(url):
                print(f"Trying to open {url}...")
                success = wb.open(url)
                print(f"Successfully opened {url}") if success else print(
                    f"Failed to open {url}")
                return success
            else:
                print(f"{url} is not a valid URL")
                return False
        except wb.Error as excp:
            print(f"An error occurred while trying to open {url}: {excp}")
            raise wb.Error(excp) from excp

    def __int__(self) -> int:
        return self.total_tasks()

    def __bool__(self) -> bool:
        return self.has_tasks()

    def __str__(self) -> str:
        return " ".join(self._tasks)

    def __iter__(self) -> Iterator:
        return iter(self._tasks)

    def __next__(self) -> Any:
        return next(self._tasks)
