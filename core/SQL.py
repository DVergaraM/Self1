from . import oint, otuple_str, Table


class Activities(Table):
    def __init__(self, log: otuple_str = None):
        super().__init__(log)
        self._name = self.__class__.__name__.lower()

    def create_log(self, log: otuple_str = None):
        db = self._conn

        if log is None:
            log = self._log

        sql = f'''INSERT INTO {0}(Image_URL, Description, Small_text)
                VALUES(?, ?, ?)'''

        cur = db.cursor()
        cur.execute(sql.format(self._name), log)
        db.commit()
        return cur.lastrowid

    def get_imageurl(self, log_id: oint = None, log: otuple_str = None):
        if log is None:
            log = self._log

        if log_id is None:
            log_id = self.create_log(log=log)

        db = self._conn

        sql = '''
        SELECT Image_URL FROM {0} WHERE id={1};
        '''

        cur = db.cursor()
        cur.execute(sql.format(self._name, log_id))
        return cur.fetchone()[0]

    def get_description(self, log_id: oint = None, log: otuple_str = None):
        if log is None:
            log = self._log

        if log_id is None:
            log_id = self.create_log(log=log)

        db = self._conn

        sql = '''
        SELECT Description FROM {0} WHERE id={1};
        '''
        cur = db.cursor()
        cur.execute(sql.format(self._name, log_id))

        return cur.fetchone()[0]

    def get_smalltext(self, log_id: oint = None, log: otuple_str = None):
        if log is None:
            log = self._log

        if log_id is None:
            log_id = self.create_log(log=log)

        db = self._conn

        sql = '''
        SELECT Small_text FROM {0} WHERE id={1}
        '''

        cur = db.cursor()
        cur.execute(sql.format(self._name, log_id))

        return cur.fetchone()[0]


class Icons(Table):
    def __init__(self, log: otuple_str = None):
        super().__init__(log)
        self._name = self.__class__.__name__.lower()
        
    def create_log(self, log: otuple_str = None):
        db = self._conn

        if log is None:
            log = self._log

        sql = '''INSERT INTO {0}(App, Path)
                VALUES(?, ?)'''

        cur = db.cursor()
        cur.execute(sql.format(self._name), log)
        db.commit()
        return cur.lastrowid

    def get_app(self, log_id: oint = None, log: otuple_str = None):

        if log is None:
            log = self._log

        if log_id is None:
            log_id = self.create_log(log=log)

        db = self._conn

        sql = '''
        SELECT App FROM {0} WHERE id={1};
        '''

        cur = db.cursor()
        cur.execute(sql.format(self._name, log_id))
        return cur.fetchone()[0]

    def get_path(self, log_id: oint = None, log: otuple_str = None):

        if log is None:
            log = self._log

        if log_id is None:
            log_id = self.create_log(log=log)

        db = self._conn

        sql = '''
        SELECT Path FROM {0} WHERE id={1};
        '''

        cur = db.cursor()
        cur.execute(sql.format(self._name, log_id))
        return cur.fetchone()[0]

    def get_id(self, app_query: str):

        db = self._conn

        sql = '''
        SELECT id FROM {0} WHERE '{1}' IN(App)
        '''

        cur = db.cursor()
        cur.execute(sql.format(self._name, app_query))
        return cur.fetchone()[0]


class Urls(Table):
    def __init__(self, log: otuple_str = None):
        super().__init__(log)
        self._name = self.__class__.__name__.lower()

    def create_log(self, log: otuple_str = None):
        db = self._conn

        if log is None:
            log = self._log

        sql = f'''INSERT INTO {0}(App, Url)
                VALUES(?, ?)'''

        cur = db.cursor()
        cur.execute(sql.format(self._name), log)
        db.commit()
        return cur.lastrowid

    def get_app(self, log_id: oint = None, log: otuple_str = None):

        if log is None:
            log = self._log

        if log_id is None:
            log_id = self.create_log(log=log)

        db = self._conn

        sql = '''
        SELECT App FROM {0} WHERE id={1};
        '''

        cur = db.cursor()
        cur.execute(sql.format(self._name, log_id))
        return cur.fetchone()[0]

    def get_url(self, log_id: oint = None, log: otuple_str = None):

        if log is None:
            log = self._log

        if log_id is None:
            log_id = self.create_log(log=log)

        db = self._conn

        sql = '''
        SELECT Url FROM {0} WHERE id={1};
        '''

        cur = db.cursor()
        cur.execute(sql.format(self._name, log_id))
        return cur.fetchone()[0]

    def get_id(self, app_query: str):

        db = self._conn

        sql = '''
        SELECT id FROM {0} WHERE '{1}' IN(App)
        '''

        cur = db.cursor()
        cur.execute(sql.format(self._name, app_query))
        return cur.fetchone()[0]
