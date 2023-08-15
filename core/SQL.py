from typing import Any as _Any
from . import oint, otuple_str, Table


class Activities(Table):
    def __init__(self, log: otuple_str = None) -> None:
        super().__init__(log)

    def create_log(self, log: otuple_str = None) -> int | None:
        db = self._conn

        if log is None:
            log = self._log

        sql = '''INSERT INTO {0}(Image_URL, Description, Small_text)
                VALUES(?, ?, ?)'''.format(self._name)

        cur = db.cursor()
        cur.execute(sql, log)
        db.commit()
        return cur.lastrowid

    def get_imageurl(self, log_id: oint = None, log: otuple_str = None) -> _Any:
        if log is None:
            log = self._log

        if log_id is None:
            log_id = self.create_log(log=log)

        db = self._conn

        sql = '''
        SELECT Image_URL FROM {0} WHERE id={1};
        '''.format(self._name, log_id)

        cur = db.cursor()
        cur.execute(sql)
        value = cur.fetchone()
        if value is None:
            raise Exception(
                f"There is not an item with the name '{log_id}', add or create one.")
        else:
            return value[0]

    def get_description(self, log_id: oint = None, log: otuple_str = None) -> _Any:
        if log is None:
            log = self._log

        if log_id is None:
            log_id = self.create_log(log=log)

        db = self._conn

        sql = '''
        SELECT Description FROM {0} WHERE id={1};
        '''.format(self._name, log_id)
        cur = db.cursor()
        cur.execute(sql)

        value = cur.fetchone()
        if value is None:
            raise Exception(
                f"There is not an item with the name '{log_id}', add or create one.")
        else:
            return value[0]

    def get_smalltext(self, log_id: oint = None, log: otuple_str = None) -> _Any:
        if log is None:
            log = self._log

        if log_id is None:
            log_id = self.create_log(log=log)

        db = self._conn

        sql = '''
        SELECT Small_text FROM {0} WHERE id={1}
        '''.format(self._name, log_id)

        cur = db.cursor()
        cur.execute(sql)

        value = cur.fetchone()
        if value is None:
            raise Exception(
                f"There is not an item with the name '{log_id}', add or create one.")
        else:
            return value[0]


class Icons(Table):
    def __init__(self, log: otuple_str = None) -> None:
        super().__init__(log)

    def create_log(self, log: otuple_str = None) -> int | None:
        db = self._conn

        if log is None:
            log = self._log

        sql = '''INSERT INTO {0}(App, Path)
                VALUES(?, ?)'''.format(self._name)

        cur = db.cursor()
        cur.execute(sql, log)
        db.commit()
        return cur.lastrowid

    def get_app(self, log_id: oint = None, log: otuple_str = None) -> _Any:

        if log is None:
            log = self._log

        if log_id is None:
            log_id = self.create_log(log=log)

        db = self._conn

        sql = '''
        SELECT App FROM {0} WHERE id={1};
        '''.format(self._name, log_id)

        cur = db.cursor()
        cur.execute(sql)
        value = cur.fetchone()
        if value is None:
            raise Exception(
                f"There is not an item with the name '{log_id}', add or create one.")
        else:
            return value[0]

    def get_path(self, log_id: oint = None, log: otuple_str = None) -> _Any:

        if log is None:
            log = self._log

        if log_id is None:
            log_id = self.create_log(log=log)

        db = self._conn

        sql = '''
        SELECT Path FROM {0} WHERE id={1};
        '''.format(self._name, log_id)

        cur = db.cursor()
        cur.execute(sql)
        value = cur.fetchone()
        if value is None:
            raise Exception(
                f"There is not an item with the name '{log_id}', add or create one.")
        else:
            return value[0]

    def get_id(self, app_query: str) -> _Any:

        db = self._conn

        sql = '''
        SELECT id FROM {0} WHERE '{1}' IN(App)
        '''.format(self._name, app_query)

        cur = db.cursor()
        cur.execute(sql)
        query_id = cur.fetchone()
        if query_id is None:
            raise Exception(
                f"There is not an item with the name '{app_query}', add or create one.")
        else:
            return query_id[0]


class Urls(Table):
    def __init__(self, log: otuple_str = None) -> None:
        super().__init__(log)

    def create_log(self, log: otuple_str = None) -> int | None:
        db = self._conn

        if log is None:
            log = self._log

        sql = f'''INSERT INTO {0}(App, Url)
                VALUES(?, ?)'''.format(self._name)

        cur = db.cursor()
        cur.execute(sql, log)
        db.commit()
        return cur.lastrowid

    def get_app(self, log_id: oint = None, log: otuple_str = None) -> _Any:

        if log is None:
            log = self._log

        if log_id is None:
            log_id = self.create_log(log=log)

        db = self._conn

        sql = '''
        SELECT App FROM {0} WHERE id={1};
        '''.format(self._name, log_id)

        cur = db.cursor()
        cur.execute(sql)
        query_id = cur.fetchone()
        if query_id is None:
            raise Exception(
                f"There is not an item with the name '{log_id}', add or create one.")
        else:
            return query_id[0]

    def get_url(self, log_id: oint = None, log: otuple_str = None) -> _Any:

        if log is None:
            log = self._log

        if log_id is None:
            log_id = self.create_log(log=log)

        db = self._conn

        sql = '''
        SELECT Url FROM {0} WHERE id={1};
        '''.format(self._name, log_id)

        cur = db.cursor()
        cur.execute(sql)
        value = cur.fetchone()
        if value is None:
            raise Exception(
                f"There is not an item with the name '{log_id}', add or create one.")
        else:
            return value[0]

    def get_id(self, app_query: str) -> _Any:

        db = self._conn

        sql = '''
        SELECT id FROM {0} WHERE '{1}' IN(App)
        '''.format(self._name, app_query)

        cur = db.cursor()
        cur.execute(sql)
        value = cur.fetchone()
        if value is None:
            raise Exception(
                f"There is not an item with the name '{app_query}', add or create one.")
        else:
            return value[0]
