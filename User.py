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

    def select_user_with_conditions(self, data:dict):
        strs = []
        condition = ""
        #print(data)
        for k, v in data.items():
            if v != '':
                str = k + "=" + "'" + v + "'"
                strs.append(str)
        #print(strs)
        for i in range(len(strs)):
            if i != len(strs) - 1:
                condition = condition + strs[i] + " and "
            else:
                condition = condition + strs[i]
        #print("condition:", condition)
        if condition != '':
            select_user_conditionally_sql = "select * from user where " + condition + ";"
            self.cursor.execute(select_user_conditionally_sql)
        else:
            select_sql = "select * from user;"
            self.cursor.execute(select_sql)

        result = self.cursor.fetchall()
        print(result)
        return result

    def fix_user_information(self, data:dict):
        u_id = data['user_id']
        strs = []
        set = ""
        for k,v in data.items():
            if v!='':
                if k != 'user_id':
                    str = k + "=" + "'" + v + "'"
                    strs.append(str)
        for i in range(len(strs)):
            if i != len(strs)-1:
                set = set + strs[i] + ", "
            else:
                set = set + strs[i]
        try:
            if set != "":
                fix_user_sql = "update user set " + set + " where user_id=" + "'" + u_id + "';"
                print(fix_user_sql)
                result = self.cursor.execute(fix_user_sql)
                self.conn.commit()
                print("number changed: ", result)
            else:
                return 0
            print('success')
        except:
            print('failed')
            result = 0
        finally:
            return result






