from .RPC import mainRPC, stopRPC
from .Pop_Ups import main as mainNotifier
from . import stop as stopNotifier
import os
from datetime import datetime
from core import mainThread

class ThreadRPC(mainThread):
    def __init__(self) -> None:
        super().__init__()

    def run(self):
        mainRPC()

    def stop(self):
        stopRPC()


class ThreadNotifier(mainThread):
    def __init__(self) -> None:
        super().__init__()

    def run(self):
        mainNotifier()

    def stop(self):
        stopNotifier()


class ThreadNotion(mainThread):
    def __init__(self) -> None:
        super().__init__()

    def run(self):
        cwt = datetime.now().strftime("%Y-%m-%d_%H-%M-%S")
        os.system(
            fr"notion > C:\Users\DANIEL\Desktop\rqaw\Documentos\Dev\Python\SelfCopy\notion-{cwt}.log")
    
    def stop(self):
        raise KeyboardInterrupt
