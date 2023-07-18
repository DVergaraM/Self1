from threading import Thread as _Thread
from typing import Optional as _Optional
from sqlite3 import (Connection as _Connection, connect as _connect, Error as _SQLITE3Error)
from os import getcwd as _getcwd

cwd = _getcwd()
db_path = fr"{cwd}\brain.db"
image_path = fr"{cwd}\images\aries.png"


otuple_str = _Optional[tuple[str]]
oint = _Optional[int]


class mainThread(object):
    def __init__(self) -> None:
        self.thread = _Thread(target=self.run, args=())

    def start(self):
        self.thread.daemon = True
        self.thread.start()

    def run(self): ...

    def stop(self): ...


class Table:
    def __init__(self, log: otuple_str = None):
        self._log = log
        self._conn: _Connection

    def create_connection(self):
        try:
            self._conn = _connect(db_path)
            cur = self._conn.cursor()
            cur.execute("""CREATE TABLE IF NOT EXISTS Activities(
                id INTEGER PRIMARY KEY AUTOINCREMENT,
                Image_URL VARCHAR(50) NOT NULL,
                Description VARCHAR(30) NOT NULL,
                Small_text VARCHAR(30) NOT NULL
                )""")
            cur.execute("""CREATE TABLE IF NOT EXISTS Icons(
                id INTEGER PRIMARY KEY AUTOINCREMENT,
                App VARCHAR(50) NOT NULL,
                Path VARCHAR(200) NOT NULL
                )""")
            cur.execute("""CREATE TABLE IF NOT EXISTS Urls(
                id INTEGER PRIMARY KEY AUTOINCREMENT,
                App VARCHAR(50) NOT NULL,
                Url VARCHAR(100) NOT NULL
                )""")
            cur.close()
            return self._conn
        except _SQLITE3Error as e:
            print(e)
