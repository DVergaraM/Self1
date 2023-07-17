from winotify import Notification as Notifier
from winotify import audio
from datetime import datetime
from typing import Callable


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
