import pymysql

class MysqlHelper:
    def __init__(self, host, user, password, database, port=3306, charset='utf8'):
        self.host = host
        self.port = port
        self.database = database
        self.user = user
        self.password = password
        self.charset = charset

    def connect(self):
        self.conn = pymysql.connect(host=self.host,
        user=self.user,
        password=self.password,
        database=self.database,
        port=self.port,
        charset=self.charset)
        self.cur = self.conn.cursor()

    def fetchone(self, sql, params=None):
        dataOne = None
        try:
                count = self.cur.execute(sql, params)
                if count != 0:
                        dataOne = self.cur.fetchone()
        except Exception as ex:
                print(ex)
        finally:
                self.close()
        return dataOne

    def fetchall(self, sql, params=None):
        dataall = None
        try:
            count = self.cur.execute(sql, params)
            if count != 0:
                dataall = self.cur.fetchall()
        except Exception as e:
                print(e)
        finally:
                self.close()
        return dataall

    def __item(self, sql, params=None):
        count = 0
        try:
            # print(1)
            count = self.cur.execute(sql, params)
            # print(count)
            self.conn.commit()
        except Exception as ex:
            print(ex)
        return count

    def update(self, sql, params=None):
        return self.__item(sql, params)

    def insert(self, sql, params=None):
        return self.__item(sql, params)

    def delete(self, sql, params=None):

        return self.__item(sql, params)

    def close(self):
        if self.cur != None:
                self.cur.close()
        if self.conn != None:
                self.conn.close()

helper = MysqlHelper('xxx', 'root', 'xxx', 'craw_house_price')
helper.connect()