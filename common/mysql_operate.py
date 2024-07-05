import pymysql
from config.setting import MYSQL_HOST, MYSQL_PORT, MYSQL_USER, MYSQL_PASSWD, MYSQL_DB, MYSQL_DB_POETIZE
from datetime import datetime

class MysqlDb():

    def __init__(self, host, port, user, passwd, db):
        self.host = host
        self.port = port
        self.user = user
        self.passwd = passwd
        self.current_db = db  # 保存当前数据库名
        self.connect_db()  # 连接数据库

    def connect_db(self):
        """连接数据库"""
        self.conn = pymysql.connect(
            host=self.host,
            port=self.port,
            user=self.user,
            passwd=self.passwd,
            db=self.current_db,  # 使用当前数据库名
            autocommit=True
        )
        self.cur = self.conn.cursor(cursor=pymysql.cursors.DictCursor)

    def change_db(self, dbInt):
        mapDb = {
            1: MYSQL_DB,
            2: MYSQL_DB_POETIZE
        }
        """更改当前数据库"""
        self.current_db = mapDb.get(dbInt, MYSQL_DB)
        self.connect_db()  # 重新连接数据库

    def __del__(self): # 对象资源被释放时触发，在对象即将被删除时的最后操作
        # 关闭游标
        self.cur.close()
        # 关闭数据库连接
        self.conn.close()

    def select_db(self, sql):
        """查询"""
        # 检查连接是否断开，如果断开就进行重连
        self.conn.ping(reconnect=True)
        # 使用 execute() 执行sql
        self.cur.execute(sql)
        # 使用 fetchall() 获取查询结果
        data = self.cur.fetchall()
        return data

    def execute_db(self, sql):
        """更新/新增/删除"""
        try:
            # 检查连接是否断开，如果断开就进行重连
            self.conn.ping(reconnect=True)
            # 使用 execute() 执行sql
            self.cur.execute(sql)
            # 提交事务
            self.conn.commit()
        except Exception as e:
            print("execute_db 操作出现错误：{}".format(e))
            # 回滚所有更改
            self.conn.rollback()

    def execute_db_params(self, sql, params=None):
        """更新/新增/删除"""
        try:
            # 检查连接是否断开，如果断开就进行重连
            self.conn.ping(reconnect=True)

            # 使用 mogrify 来组合SQL语句和参数
            compiled_sql = self.cur.mogrify(sql, params)
            # 打印出完整的SQL语句

            self.addText(self.getNowTime() + compiled_sql, 'film-insert.txt')

            # 使用 execute() 执行sql
            self.cur.execute(sql, params)
            # 提交事务
            self.conn.commit()
        except Exception as e:

            print("execute_db_params 操作出现错误：{}".format(e))
            self.addText(self.getNowTime() + "错误：{}".format(e), 'film-insert-error.txt')

            # 使用 mogrify 来组合SQL语句和参数
            compiled_sql = self.cur.mogrify(sql, params)
            # 打印出完整的SQL语句
            # print("Executing  SQL: " + compiled_sql)
            self.addText(self.getNowTime() + compiled_sql + ";", 'film-insert-todo.txt')

            # 回滚所有更改
            self.conn.rollback()
            pass

    def getNowTime(self):
        # 获取当前时间
        now = datetime.now()
        # 按照指定格式格式化时间字符串，'%Y-%m-%d %H:%M:%S' 是年-月-日 时:分:秒 的格式
        formatted_time = now.strftime('%Y-%m-%d %H:%M:%S')
        return "【" + formatted_time + "】\n"

    def addText(self, content, fileName):
        with open(fileName, 'a', encoding='utf-8') as file:
            # 在文件末尾追加文本
            file.write("\n"+content)


db = MysqlDb(MYSQL_HOST, MYSQL_PORT, MYSQL_USER, MYSQL_PASSWD, '')