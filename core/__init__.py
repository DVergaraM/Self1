from threading import Thread as _Thread
from typing import (Optional as _Optional, Any as _Any)
from sqlite3 import (Connection as _Connection,
                     connect as _connect, Error as _SQLITE3Error)
from os import getcwd as _getcwd
from abc import (ABC as _ABC, abstractmethod as _abstractmethod)

cwd = _getcwd()
db_path = fr"{cwd}\brain_mine.db"
image_path = fr"{cwd}\images\aries.png"


otuple_str = _Optional[tuple[str]]
oint = _Optional[int]


class Thread(_ABC):
    def __init__(self) -> None:
        self.thread = _Thread(target=self.run, args=())

    def start(self) -> None:
        self.thread.daemon = True
        self.thread.start()

    @_abstractmethod
    def run(self) -> _Any:
        ...

    @_abstractmethod
    def stop(self) -> _Any:
        ...


class Table:
    def __init__(self, log: otuple_str = None) -> None:
        self._log = log
        self._conn: _Connection
        self._name = self.__class__.__name__.lower()

    def create_connection(self) -> _Optional[_Connection]:
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

    def _is_empty(self, lst: list[_Any]) -> bool:
        return len(lst) == 0

    def get_all(self) -> (tuple[()] | tuple[_Any, ...]):
        db = self._conn

        sql = '''
        SELECT * FROM {0}
        '''.format(self._name)

        cur = db.cursor()
        cur.execute(sql)
        lst = cur.fetchall()
        tp = ()
        if self._is_empty(lst):
            raise Exception(
                "There are not Items to get, please add some and try again.")
        else:
            for element in lst:
                tp = tp + (element, )
            return tp
