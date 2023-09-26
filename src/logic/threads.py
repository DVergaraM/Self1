import threading
from datetime import datetime
from abc import ABC, abstractmethod
from typing import Literal
import time
import os
from . import run_pending


class ThreadBase(ABC, threading.Thread):
    def __init__(self, **kwargs) -> None:
        super().__init__(**kwargs)
        self.stop_event = threading.Event()
        self.state = "stopped" 
        self.new_thread: threading.Thread = threading.Thread()

    @abstractmethod
    def run(self):
        date = datetime.now()
        print(f"[{date.year}-{date.month}-{date.day} {date.hour}:{date.minute}:{date.second}] - {self.name} (run)")
        while not self.stop_event.is_set():
            print("Running")
            time.sleep(1.5)

    def start(self) -> None:
        if (self.state == "stopped" or self.state == "finished"):
            self.state = "running"
            self.new_thread = threading.Thread(target=self.run)
            self.new_thread.daemon = self.daemon
            self.new_thread.start()

    def stop(self):
        if self.state == "running":
            self.state = "stopped"
            date = datetime.now()
            print(
                f"[{date.year}-{date.month}-{date.day} {date.hour}:{date.minute}:{date.second}] - {self.name} (stop)")
            self.stop_event.set()
            self.new_thread.join()


class ThreadNotifier(ThreadBase):
    def __init__(self, **kwargs) -> None:
        super().__init__(**kwargs)

    def run(self) -> None:
        try:
            date = datetime.now()
            print(
                f"[{date.year}-{date.month}-{date.day} {date.hour}:{date.minute}:{date.second}] - {self.name} (run)")

            while not self.stop_event.is_set():
                run_pending()

            self.state = "finished" 
        except Exception as e:
            print(f"Error in ThreadNotifier: {e}")


class OSThread(ThreadBase):
    def __init__(self, path: str = None, name: str = None, **kwargs) -> None:
        super().__init__(**kwargs)
        self._path = path
        self._name = name
        self.cwd = os.getcwd()

    @property
    def path(self):
        return self._path

    @path.setter
    def path(self, value):
        if isinstance(value, str):
            self._path = value
        else:
            raise TypeError("value must be a string")

    @property
    def name(self):
        return self._name

    @name.setter
    def name(self, value):
        if isinstance(value, str):
            self._name = value
        else:
            raise TypeError("value must be a string")

    def run(self) -> None:
        try:
            date = datetime.now()
            self.name = "Thread"
            print(
                f"[{date.year}-{date.month}-{date.day} {date.hour}:{date.minute}:{date.second}] - {self.name} (run)")

            # while not self.stop_event.is_set():
            self.path = fr'"{self.path}"'
            try:
                os.system(fr"mkdir {self.cwd}\logs\\")
            except:
                pass
            
            command = fr"{self.path} > {self.cwd}\logs\log-{date.year}-{date.month}-{date.day}_{date.hour}-{date.minute}.log"
            os.system(command)

            self.state = "finished"
            self.stop()
        except Exception as e:
            print(f"Error in OSThread: {e}")
