import MySQLdb
import os
import time
import configparser
import traceback
from config import py_config


class MySQL:

    def __init__(self, db_config_path):
        self.config = configparser.ConfigParser()
        self.config.read(db_config_path)
        self.my_db_user = self.config.get('mysql', 'username')
        self.my_db_pass = os.environ.get('mysql_password')
        self.my_db_host = self.config.get('mysql', 'host')
        self.my_db_name = self.config.get('mysql', 'default_db')
        # print(self.my_db_name, self.my_db_host, self.my_db_user)
        try:
            self.my_db_port = self.config.get('mysql', 'db_port')
        except configparser.NoOptionError:
            self.my_db_port = 3306
        self.my_db_retry = self.config.get('mysql', 'db_connect_retry_attempts')
        self.conn = self.connect()

    def connect(self):
        conn = None
        for i in range(int(self.my_db_retry)):
            try:
                conn = MySQLdb.connect(user=self.my_db_user, password=self.my_db_pass,
                                       host=self.my_db_host, database=self.my_db_name)
            except Exception as e:
                time.sleep(1)
                print(e)
            return conn

    def get_curs(self, opt=''):
        curs = None
        for i in range(2):
            try:
                curs = ''
                if opt == 1:
                    curs = self.conn.cursor()
                else:
                    curs = self.conn.cursor(MySQLdb.cursors.SSDictCursor)
                return curs
            except Exception as e:
                print(e)
        return curs

    def processQuery(self, q, locals=None, opt='', copt=''):
        for i in range(2):
            try:
                cursor = self.get_curs(copt)
                cursor.execute(q, locals)
                if opt == 1:
                    records = cursor.fetchone()
                else:
                    records = cursor.fetchall()
                cursor.close()

                return records
            except Exception as e:
                print("Exception Query:", q)
                print("Exception:", e)
                print(traceback.format_exc())
                self.conn = self.connect()
        print(traceback.format_exc())
        raise RuntimeError("Execute failed despite our best attempts...Giving up :(")

    def replaceFromDict(self, dic, table, colList=None):
        if not colList:
            colList = dic.keys()
        query = "Replace into %s (%s) values (%s)" % (
            table, ",".join(colList), ",".join(map(lambda x: "%(" + x + ")s", colList)))
        ret = self.processQuery(query, dic)
        return ret

    def insertFromDict(self, dic, table, colList=None):
        if not colList:
            colList = dic.keys()
        query = "insert into %s (%s) values (%s)" % (
            table, ",".join(colList), ",".join(map(lambda x: "%(" + x + ")s", colList)))
        ret = self.processQuery(query, dic)
        return ret

    def updateFromDict(self, dic, table, colList=None, **pkeys):
        if not colList:
            colList = dic.keys()

        if pkeys:
            query = "update %s set %s where %s" % (
                table, ",".join(map(lambda x: x + " = %(" + x + ")s", colList)),
                ' and '.join(map(lambda x: x + " = %(" + x + ")s", pkeys)))

        else:
            raise RuntimeError('Not a single key present where clause')

        ret = self.processQuery(query, dict(dic, **pkeys))
        return ret

    def commit(self):
        self.conn.commit()

    def rollback(self):
        self.conn.rollback()


if __name__ == "__main__":
    db = MySQL(py_config.db_config)
    query_out = db.processQuery("SELECT * FROM local_db.actor_local;")

    for row in query_out:
        print(row)

    db.commit()
