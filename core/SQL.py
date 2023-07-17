from .config import db_path, oint, otuple_str
# from mysql import sqlite3
import sqlite3


class Table:
    def __init__(self, log: otuple_str = None):
        self._log = log
        self._conn: sqlite3.Connection

    def create_connection(self):
        try:
            self._conn = sqlite3.connect(db_path)
            return self._conn
        except sqlite3.Error as e:
            print(e)


class Activities(Table):
    def __init__(self, log: otuple_str = None):
        super().__init__(log)
    """ 
    def create_connection(self):

        try:

            self._conn = sqlite3.connect(db_path)

            return self._conn
        except sqlite3.Error as e:
            print(e) 
    """

    def create_log(self, log: otuple_str = None):
        db = self._conn

        if log is None:
            log = self._log

        sql = f'''INSERT INTO activities(Image_URL, Description, Small_text)
                VALUES(?, ?, ?)'''

        cur = db.cursor()
        cur.execute(sql, log)
        db.commit()
        return cur.lastrowid

    def get_imageurl(self, log_id: oint = None, log: otuple_str = None):
        if log is None:
            log = self._log

        if log_id is None:
            log_id = self.create_log(log=log)

        db = self._conn

        sql = '''
        SELECT Image_URL FROM activities WHERE id={0};
        '''

        cur = db.cursor()
        cur.execute(sql.format(log_id))
        return cur.fetchone()[0]

    def get_description(self, log_id: oint = None, log: otuple_str = None):
        if log is None:
            log = self._log

        if log_id is None:
            log_id = self.create_log(log=log)

        db = self._conn

        sql = '''
        SELECT Description FROM activities WHERE id={0};
        '''
        cur = db.cursor()
        cur.execute(sql.format(log_id))

        return cur.fetchone()[0]

    def get_smalltext(self, log_id: oint = None, log: otuple_str = None):
        if log is None:
            log = self._log

        if log_id is None:
            log_id = self.create_log(log=log)

        db = self._conn

        sql = '''
        SELECT Small_text FROM activities WHERE id={0}
        '''

        cur = db.cursor()
        cur.execute(sql.format(log_id))

        return cur.fetchone()[0]


class Icons(Table):
    def __init__(self, log: otuple_str = None):
        super().__init__(log)
    """ 
    def create_connection(self):

        try:

            self._conn = sqlite3.connect(db_path)
            # host=config["host"], user=config["user"], password=config["password"], database=config["database"])
            return self._conn
        except sqlite3.Error as e:
            print(e) 
    """

    def create_log(self, log: otuple_str = None):
        db = self._conn

        if log is None:
            log = self._log

        sql = f'''INSERT INTO Icons(App, Path)
                VALUES(?, ?)'''

        cur = db.cursor()
        cur.execute(sql, log)
        db.commit()
        return cur.lastrowid

    def get_app(self, log_id: oint = None, log: otuple_str = None):

        if log is None:
            log = self._log

        if log_id is None:
            log_id = self.create_log(log=log)

        db = self._conn

        sql = '''
        SELECT App FROM Icons WHERE id={0};
        '''

        cur = db.cursor()
        cur.execute(sql.format(log_id))
        return cur.fetchone()[0]

    def get_path(self, log_id: oint = None, log: otuple_str = None):

        if log is None:
            log = self._log

        if log_id is None:
            log_id = self.create_log(log=log)

        db = self._conn

        sql = '''
        SELECT Path FROM Icons WHERE id={0};
        '''

        cur = db.cursor()
        cur.execute(sql.format(log_id))
        return cur.fetchone()[0]

    def get_id(self, app_query: str):

        db = self._conn

        sql = '''
        SELECT id FROM Icons WHERE '{0}' IN(App)
        '''

        cur = db.cursor()
        cur.execute(sql.format(app_query))
        return cur.fetchone()[0]


class Urls(Table):
    def __init__(self, log: otuple_str = None):
        super().__init__(log)
    """ 
    def create_connection(self):

        try:

            self._conn = sqlite3.connect(db_path)
            # host=config["host"], user=config["user"], password=config["password"], database=config["database"])
            return self._conn
        except sqlite3.Error as e:
            print(e)
        # return self._conn 
    """

    def create_log(self, log: otuple_str = None):
        db = self._conn

        if log is None:
            log = self._log

        sql = f'''INSERT INTO Urls(App, Path)
                VALUES(?, ?)'''

        cur = db.cursor()
        cur.execute(sql, log)
        db.commit()
        return cur.lastrowid

    def get_app(self, log_id: oint = None, log: otuple_str = None):

        if log is None:
            log = self._log

        if log_id is None:
            log_id = self.create_log(log=log)

        db = self._conn

        sql = '''
        SELECT App FROM Urls WHERE id={0};
        '''

        cur = db.cursor()
        cur.execute(sql.format(log_id))
        return cur.fetchone()[0]

    def get_url(self, log_id: oint = None, log: otuple_str = None):

        if log is None:
            log = self._log

        if log_id is None:
            log_id = self.create_log(log=log)

        db = self._conn

        sql = '''
        SELECT Url FROM Urls WHERE id={0};
        '''

        cur = db.cursor()
        cur.execute(sql.format(log_id))
        return cur.fetchone()[0]

    def get_id(self, app_query: str):

        db = self._conn

        sql = '''
        SELECT id FROM Urls WHERE '{0}' IN(App)
        '''

        cur = db.cursor()
        cur.execute(sql.format(app_query))
        return cur.fetchone()[0]
