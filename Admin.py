from pymysql import connect
from pymysql.cursors import DictCursor

from config import MYSQL_HOST, MYSQL_PORT, MYSQL_USER, MYSQL_PASSWORD, MYSQL_DATABASE


class Admin:
    def __init__(self):
        self.conn = connect(
            host=MYSQL_HOST,
            port=MYSQL_PORT,
            user=MYSQL_USER,
            password=MYSQL_PASSWORD,
            database=MYSQL_DATABASE,
        )

        self.cursor = self.conn.cursor(DictCursor)

    def __del__(self):
        self.cursor.close()
        self.conn.close()

    def select_admin(self, adminid, password):
        # print('select admin')
        # mysql语句
        select_admin_sql = 'select * from admin where admin_id="%s" and admin_password="%s";' % (adminid, password)
        # 执行mysql语句
        result = self.cursor.execute(select_admin_sql)
        # 如果返回了一条数据，则登录成功，否则登录失败
        if 1 == result:
            result = True
        else:
            result = False
            print('there is no administrator where adminid="%s" and password="%s"!!' % (adminid, password))
        return result
