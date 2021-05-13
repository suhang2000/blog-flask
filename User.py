from pymysql import connect
from pymysql.cursors import DictCursor

from config import MYSQL_HOST, MYSQL_PORT, MYSQL_USER, MYSQL_PASSWORD, MYSQL_DATABASE


class User:
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

    def select_user(self, userid, password):
        # print('select user')
        # mysql语句
        select_user_sql = 'select * from user where username="%s" and user_password="%s";' % (userid, password)
        # 执行mysql语句
        result = self.cursor.execute(select_user_sql)
        # 如果返回了一条数据，则登录成功，否则登录失败
        if 1 == result:
            result = True
        else:
            result = False
            print('there is no user where username="%s" and password="%s"!!' % (userid, password))
        return result

    def insert_user(self, data: dict) -> bool:
        keys = ''
        values = ''
        for k, v in data.items():
            keys += k
            keys += ','
            values += "'"
            values += v
            values += "'"
            values += ','
        keys = keys[:-1]
        values = values[:-1]
        insert_user_sql = "INSERT INTO user({}) values({});".format(keys, values)
        print(insert_user_sql)
        # 执行mysql语句，如果插入成功，则注册成功，否则注册失败
        try:
            self.cursor.execute(insert_user_sql)
            self.conn.commit()
            print('success')
            result = True
        except:
            print('failed')
            self.conn.rollback()
            result = False
        finally:
            return result

    def update_user(self, data: dict) -> bool:
        insert_user_sql = ''
        for key, value in data.items():
            insert_user_sql = "UPDATE user SET {}='{}' WHERE username='{}';".format(key, value, data['username'])
            print(insert_user_sql)
            self.cursor.execute(insert_user_sql)

        # 执行mysql语句，如果插入成功，则注册成功，否则注册失败
        try:
            self.conn.commit()
            print('success')
            result = True
        except:
            print('failed')
            self.conn.rollback()
            result = False
        finally:
            return result