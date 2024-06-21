from flask import Flask, jsonify, request
from common.mysql_operate import db
from common.redis_operate import redis_db
from common.md5_operate import get_md5
import re, time

app = Flask(__name__)
app.config["JSON_AS_ASCII"] = False  # jsonify返回的中文正常显示


@app.route('/')
def hello_world():
    return 'Hello World!'


@app.route("/users", methods=["POST"])
def get_all_users():
    """获取所有用户信息"""
    sql = "SELECT * FROM user"
    data = db.select_db(sql)
    print("获取所有用户信息 == >> {}".format(data))
    return jsonify({"code": 0, "data": data, "msg": "查询成功"})



@app.route("/filmAdd", methods=['POST'])
def filmAdd():

    title = "大鱼海棠"
    cover = "https://img9.doubanio.com/view/photo/s_ratio_poster/public/p2361744534.webp"
    url = "https://movie.douban.com/subject/5045678/"
    rating = "蒲公英"
    casts = "\"季冠霖\",\"苏尚卿\""
    star = "35"
    directors = "\"张浩\""
    cover_x = 1080
    cover_y = 1620
    other_id = "5045678"
    sql3 = "INSERT INTO a_film(title, cover, url, rating, casts, star, directors, cover_x, cover_y, other_id) " \
           "VALUES('{}', '{}', '{}', '{}', '{}', '{}', '{}', '{}', '{}', '{}')".format(title, cover, url, rating, casts, star, directors, cover_x, cover_y, other_id)
    print("sql3:" + sql3 )
    db.execute_db(sql3)
    print("新增用户信息SQL ==>> {}".format(sql3))
    return jsonify({"code": 200, "msg": "ok!"})
