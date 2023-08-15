from threading import Thread as _Thread
from typing import (Any as _Any,
                    TypeVar as _TypeVar)
from sqlite3 import (Connection as _Connection,
                     connect as _connect, DatabaseError as _DatabaseError)
import PIL.Image as Img
from os import getcwd as _getcwd
from abc import (ABC as _ABC, abstractmethod as _abstractmethod)
from datetime import datetime

CWD = _getcwd()
DB_PATH = fr"{CWD}\brain_mine.db"
IMAGE_PATH = fr"{CWD}\images\aries.png"
PRESENCE_ID = "1126179074130321508"
STRAY_ICON = Img.open(IMAGE_PATH)
ICON = "https://i.imgur.com/N1fuUn8.jpg"

dict_tuple = _TypeVar("dict_tuple", dict[int, dict[str, str]], tuple[tuple[str]])
otuple_str = _TypeVar("otuple_str", tuple[str], None)
oint = _TypeVar("oint", int, None)


class Thread(_ABC):
    def __init__(self) -> None:
        self._thread = _Thread(target=self.run)

    def _start(self) -> None:
        self._thread.daemon = True
        self._thread.start()
        thread_name = self._thread.name
        date = datetime.now()
        print(
            f"[{date.year}-{date.month}-{date.day} {date.hour}:{date.minute}:{date.second}] - {thread_name}")

    @_abstractmethod
    def run(self) -> _Any:
        ...

    @_abstractmethod
    def stop(self) -> _Any:
        ...


class Table:
    def __init__(self, log: otuple_str) -> None:
        self._log = log
        self._conn: _Connection
        self._name = self.__class__.__name__.lower()

    @property
    def name(self):
        return self._name

    @name.setter
    def name(self, value):
        self._name = str(value)

    def create_connection(self) -> (_Connection | None):
        try:
            self._conn = _connect(DB_PATH)
            cur = self._conn.cursor()
            cur.execute("""CREATE TABLE IF NOT EXISTS Activities(
                id INTEGER PRIMARY KEY AUTOINCREMENT,
                Image_URL VARCHAR(120) NOT NULL,
                Description VARCHAR(120) NOT NULL,
                Small_text VARCHAR(120) NOT NULL
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
            del cur
            if isinstance(self._conn, _Connection):
                return self._conn
            else:
                raise _DatabaseError("Connection Failure")
        except _DatabaseError as e:
            # print(e)
            raise _DatabaseError

    def _is_empty(self, fetchall: list[_Any]) -> bool:
        return len(fetchall) == 0

    def get_all(self) -> (tuple[()] | tuple[_Any, ...]):
        db = self._conn

        sql = '''
        SELECT * FROM {0}
        '''.format(self._name)

        cur = db.cursor()
        cur.execute(sql)
        fetchall = cur.fetchall()
        tp = ()
        if self._is_empty(fetchall):
            raise _DatabaseError(
                f"There are not items to get in \"{self._name}\" table, please add some and try again.")
        else:
            for element in fetchall:
                tp = tp + (element, )
            return tp
