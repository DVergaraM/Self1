"Schedule Logic Module"
# pylint: disable=import-self
# pylint: disable=invalid-name
# pylint: disable=no-name-in-module
# pylint: disable=import-error
# pylint: disable=no-member
# pylint: disable=not-callable
from typing import Callable, Tuple, Any, Union, Iterator
import time as tm
import re
import webbrowser as wb
import pytz
import schedule as _schedule
import validators
from logic import MQThread


class Schedule:
    """
    Schedule class is responsible for managing tasks that will be executed at specific times.
    """
    def __init__(self, timezone: Union[str, pytz.BaseTzInfo] = "America/Bogota", **kwargs) -> None:
        """
        Initializes a new instance of the Schedule class.

        :param timezone: The timezone to use for scheduling tasks.
        :type timezone: Union[str, pytz.BaseTzInfo]
        :param kwargs: Additional arguments to configure the Schedule instance.
        :type kwargs: dict
        """
        self._tasks: list[tuple] = []
        self._amount_tasks = 0
        self.notifier = kwargs["notifier"] if "notifier" in kwargs else None
        self.start_thread = kwargs["start_thread"] if "start_thread" in kwargs else None
        self.database = kwargs["database"] if "database" in kwargs else None
        if isinstance(timezone, str):
            self.timezone = pytz.timezone(timezone)
        elif isinstance(timezone, pytz.BaseTzInfo):
            self.timezone = timezone
        else:
            raise ValueError(
                "'timezone' is not an instance of str or pytz.BaseTzInfo")

    @property
    def tasks(self):
        """
        Gets the list of tasks currently scheduled.

        :return: The list of tasks currently scheduled.
        :rtype: list[tuple]
        """
        return self._tasks

    def add_task(self, time: str, method: Union[Callable, str],
                 args: Tuple[Any] | list[Any] = None) -> bool:  # type: ignore
        """
        Adds a new task to the schedule.

        :param time: The time at which the task should be executed.
        :type time: str
        :param method: The method to execute when the task is executed.
        :type method: Union[Callable, str]
        :param args: The arguments to pass to the method when it is executed.
        :type args: Tuple[Any] | list[Any]
        :return: True if the task was added successfully, False otherwise.
        :rtype: bool
        """
        if isinstance(method, Callable) and self.is_time(time):
            job = _schedule.every().day.at(time).do(
                self.run_task, method, args if args else [])
            self._tasks.append((time, method, job))
            print(self._tasks)
            self._amount_tasks += 1
            print("Added method")
            return True
        if isinstance(method, str) and self.is_time(time):
            job = _schedule.every().day.at(time).do(
                self.run_task, self.open_web, [method])
            self._tasks.append((time, self.open_web, job))
            print(self._tasks)
            self._amount_tasks += 1
            print("Added URL")
            return True
        return False

    def remove_task(self, method_name: Union[str, Callable]) -> bool:
        """
        Removes a task from the schedule.

        :param method_name: The name of the method to remove, or the method itself.
        :type method_name: Union[str, Callable]
        :return: True if the task was removed successfully, False otherwise.
        :rtype: bool
        """
        for t in self._tasks:
            if isinstance(method_name, Callable):
                if t[1].__name__ == method_name.__name__:
                    _schedule.cancel_job(t[2])
                    self._tasks.remove(t)
                    self._amount_tasks -= 1
                    return True
            if isinstance(method_name, str):
                if t[1] == method_name:
                    _schedule.cancel_job(t[2])
                    self._tasks.remove(t)
                    self._amount_tasks -= 1
                    return True
        print("Still", self._tasks, self._amount_tasks)
        return False

    def run_task(self, method: Callable, args: list | tuple) -> None:
        """
        Executes a task.

        :param method: The method to execute.
        :type method: Callable
        :param args: The arguments to pass to the method.
        :type args: list | tuple
        """
        method(*args)
        tm.sleep(1.25)
        self.remove_task(method)

    def total_tasks(self) -> int:
        """
        Gets the total number of tasks currently scheduled.

        :return: The total number of tasks currently scheduled.
        :rtype: int
        """
        return len(self._tasks)

    def has_tasks(self) -> bool:
        """
        Determines whether there are any tasks currently scheduled.

        :return: True if there are tasks currently scheduled, False otherwise.
        :rtype: bool
        """
        return len(self._tasks) != 0

    def start(self) -> None:
        """
        Starts the schedule and begins executing tasks.
        """
        if self.notifier and isinstance(self.notifier, Callable):
            self.notifier()
        if self.notifier and isinstance(self.notifier, MQThread):
            self.notifier.start()
        while self._amount_tasks != 0:
            _schedule.run_pending()
            tm.sleep(1)

    def stop(self) -> None:
        """
        Stops the schedule and cancels all scheduled tasks.
        """
        _schedule.clear()

    @staticmethod
    def open_web(url: str) -> bool:
        """
        Opens a URL in the default web browser.

        :param url: The URL to open.
        :type url: str
        :return: True if the URL was opened successfully, False otherwise.
        :rtype: bool
        """
        try:
            if validators.url(url):  # type: ignore
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
        """
        Determines whether a string represents a valid time in the format HH:MM.

        :param time: The string to check.
        :type time: str
        :return: True if the string represents a valid time, False otherwise.
        :rtype: bool
        """
        pattern = r"^[0-9]{2}:[0-9]{2}$"
        return bool(re.match(pattern, time))

    def __int__(self) -> int:
        """
        Gets the total number of tasks currently scheduled.

        :return: The total number of tasks currently scheduled.
        :rtype: int
        """
        return self.total_tasks()

    def __bool__(self) -> bool:
        """
        Determines whether there are any tasks currently scheduled.

        :return: True if there are tasks currently scheduled, False otherwise.
        :rtype: bool
        """
        return self.has_tasks()

    def __str__(self) -> str:
        """
        Gets a string representation of the Schedule instance.

        :return: A string representation of the Schedule instance.
        :rtype: str
        """
        return " ".join([str(task) for task in self._tasks])

    def __iter__(self) -> Iterator:
        """
        Gets an iterator for the list of tasks currently scheduled.

        :return: An iterator for the list of tasks currently scheduled.
        :rtype: Iterator
        """
        return iter(self._tasks)

    def __next__(self) -> Any:
        """
        Gets the next item in the list of tasks currently scheduled.

        :return: The next item in the list of tasks currently scheduled.
        :rtype: Any
        """
        return next(iter(self._tasks))
