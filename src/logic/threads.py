import threading
from datetime import datetime
from abc import ABC, abstractmethod
from typing import Literal
import time
import os
from . import run_pending
from PyQt5.QtCore import QProcess


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
