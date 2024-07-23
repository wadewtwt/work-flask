import sys
import os
common_dir = os.path.abspath(os.path.join(os.path.dirname(__file__),  '..'))
sys.path.append(common_dir)
# sys.path.append('D:\work\py\work-flask\common')
from common.mysql_operate import db



if __name__ == '__main__':
    print(common_dir)

    db.change_db(1)
    sql1 = "SELECT id,title FROM a_film WHERE title = '{}'".format("窗边的小豆豆")
    res1 = db.select_db(sql1)
    print(sys.path)
    print(res1)