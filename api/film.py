from decimal import Decimal

from flask import Flask, jsonify, request
from common.mysql_operate import db
from common.redis_operate import redis_db
from common.md5_operate import get_md5
import re, time
import requests
import json
import random
import threading



app = Flask(__name__)
app.config["JSON_AS_ASCII"] = False  # jsonify返回的中文正常显示


@app.route('/')
def hello_world():
    return 'Hello World!'

@app.route("/filmAdd", methods=['POST'])
def filmAdd():
    # title = "大鱼海棠"
    # cover = "https://img9.doubanio.com/view/photo/s_ratio_poster/public/p2361744534.webp"
    # url = "https://movie.douban.com/subject/5045678/"
    # rating = 6.7
    # casts = "\"季冠霖\",\"苏尚卿\""
    # star = "35"
    # directors = "\"张浩\""
    # cover_x = 1080
    # cover_y = 1620
    # other_id = "5045678"
    #
    # sql3 = "INSERT INTO a_film(title, cover, url, rating, casts, star, directors, cover_x, cover_y, other_id) " \
    #        "VALUES('{}', '{}', '{}', '{}', '{}', '{}', '{}', '{}', '{}', '{}')".format(title, cover, url, rating, casts, star, directors, cover_x, cover_y, other_id)
    # print("sql3:" + sql3 )
    # db.execute_db(sql3)
    # print("新增用户信息SQL ==>> {}".format(sql3))
    return jsonify({"code": 200, "msg": "ok!"})

@app.route("/collect", methods=['GET'])
def collect():
    for i in range(2701, 10000, 20):
        print("now start is:" + str(i))
        remoteCollect(i)

    return jsonify({"code": 200, "msg": "collect ok!"})

def remoteCollect(start):
    random_number = random.randint(1, 5)
    time.sleep(random_number)

    url = 'https://movie.douban.com/j/new_search_subjects?sort=T&tags=&start=' + str(start)
    headers = {
        'User-Agent': 'Mozilla/5.0 (Windows NT 10.0; Win64; x64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/58.0.3029.110 Safari/537.3'
    }
    response = requests.get(url, headers=headers)

    if response.status_code == 200:
        try:
            data = response.json()

            for item in data['data']:
                title = item['title']
                cover = item['cover']
                url = item['url']
                rating = Decimal(item['rate'])
                casts = str(item['casts'])
                star = int(item['star'])
                directors = str(item['directors'])
                cover_x = int(item['cover_x'])
                cover_y = int(item['cover_y'])
                other_id = str(item['id'])
                addFilmSql(title, cover, url, rating, casts, star, directors, cover_x, cover_y, other_id)


        except json.decoder.JSONDecodeError:
            print('Error: Failed to decode JSON data')
    else:
        print(f'Error: Failed to fetch data. Status code: {response.status_code}')
        exit()

def addFilmSql(title, cover, url, rating, casts, star, directors, cover_x, cover_y, other_id):
    sql3 = "INSERT INTO a_film(title, cover, url, rating, casts, star, directors, cover_x, cover_y, other_id) " \
           "VALUES(%s, %s, %s, %s, %s, %s, %s, %s, %s, %s)"

    print("title is:" + title)
    db.execute_db_params(sql3, (title, cover, url, rating, casts, star, directors, cover_x, cover_y, other_id))


def getProxysFromFile():
    with open("proxy.txt", "r") as f:
        l = f.readlines()
    return l


def run(proxy, start):
    try:
        print("proxy:{}".format(proxy))
        s = requests.Session()
        proxies = {
            "http": "http://{}".format(proxy.strip())
        }

        header = {
            'User-Agent': 'Mozilla/5.0 (Windows NT 10.0; Win64; x64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/58.0.3029.110 Safari/537.3'
        }

        ret = s.get(url='https://movie.douban.com/j/new_search_subjects?sort=T&tags=&start=' + str(start),
                    headers=header, proxies=proxies, timeout=4, verify=False)
        rc = ret.content.decode("utf-8")
        print("远程结果：")
        print(rc)
        exit()
        if "成功" in rc:
            global count
            count += 1
            print(count)
    except Exception as e:
        print("发生异常：", e)
        pass


if __name__ == '__main__':
    l=getProxysFromFile()
    # while True:
    for i in range(2701, 2750, 20):
        print("now start is:" + str(i))
        try:
            t=threading.Thread(target=run,args=(l.pop(), i))
            t.start()
        except:
            print("线程出错！")
            pass
