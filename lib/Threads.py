from .RPC import mainRPC, stopRPC
from .Pop_Ups import main as mainNotifier
from . import stop as stopNotifier
import os
from datetime import datetime
from typing import NoReturn as _NoReturn
from core import Thread

class ThreadRPC(Thread):
    def __init__(self) -> None:
        super().__init__()

    def run(self) -> None:
        mainRPC()

    def stop(self) -> None:
        stopRPC()


class ThreadNotifier(Thread):
    def __init__(self) -> None:
        super().__init__()

    def run(self) -> None:
        mainNotifier()

    def stop(self) -> None:
        stopNotifier()


class ThreadNotion(Thread):
    def __init__(self) -> None:
        super().__init__()

    def run(self) -> None:
        cwt = datetime.now().strftime("%Y-%m-%d_%H-%M-%S")
        os.system(
            fr"notion > C:\Users\DANIEL\Desktop\rqaw\Documentos\Dev\Python\SelfCopy\notion-{cwt}.log")
    
    def stop(self) -> _NoReturn:
        raise KeyboardInterrupt
