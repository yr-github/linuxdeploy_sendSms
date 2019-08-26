import sqlite3

class OperateSQL():
    def __init__(self,path,logger):
        self.path = path
        self.logger = logger
    def getConn(self):
        try:
            self.conn = sqlite3.connect(self.path)
        except sqlite3.Error as err:
            self.logger.info(err)
        return

    def updateSms(self):
        writeSql = "UPDATE sms SET seen = 1 ,read = 1 WHERE seen =0"#按需更改
        try:
            self.getConn()
            cursor = self.conn.cursor()
            num = cursor.execute(writeSql)
            self.conn.commit()
            cursor.close()
            self.conn.close()
            return num

        except sqlite3.Error as err:
            self.logger.info(err)
            return 0
        finally:
            if self.conn:
                self.conn.close()

    def readSms(self):
        readSql = "SELECT address,body FROM sms WHERE seen=0"#按需更改
        try:
            self.getConn()
            cursor = self.conn.cursor()
            cursor.execute(readSql)
            results = cursor.fetchall()
            self.conn.commit()
            cursor.close()
            self.conn.close()
            return results
        except sqlite3.Error as err:
            self.logger.info(err)
            return 0
        finally:
            if self.conn:
                self.conn.close()


