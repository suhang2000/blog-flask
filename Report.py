from pymysql import connect
from pymysql.cursors import DictCursor

from config import MYSQL_HOST, MYSQL_PORT, MYSQL_USER, MYSQL_PASSWORD, MYSQL_DATABASE


class Report:
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

    def select_report_with_conditions(self, data: dict):
        strs = []
        condition = ""
        # print(data)
        for k, v in data.items():
            if v != '':
                str = k + "=" + "'" + v + "'"
                strs.append(str)
        # print(strs)
        for i in range(len(strs)):
            if i != len(strs) - 1:
                condition = condition + strs[i] + " and "
            else:
                condition = condition + strs[i]
        # print("condition:", condition)
        if condition != '':
            select_report_conditionally_sql = "select * from report where " + condition + ";"
            self.cursor.execute(select_report_conditionally_sql)
        else:
            select_sql = "select * from report;"
            self.cursor.execute(select_sql)

        result = self.cursor.fetchall()
        print(result)
        return result

    def delete_report_with_id(self, blog_id):
        delete_sql = 'delete from report where blog_id=' + "'" + blog_id + "'" + ';'
        print(delete_sql)
        result = self.cursor.execute(delete_sql)
        try:
            self.conn.commit()
        except:
            print('delete failed!')
            result = 0
        finally:
            return result