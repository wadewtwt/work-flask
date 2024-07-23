from decimal import Decimal

from flask import Flask, jsonify, request
from common.mysql_operate import db
import re, time
import requests
import json
import random
import threading
from urllib3.exceptions import InsecureRequestWarning



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
    with open("../proxy.txt", "r") as f:
        lines = f.readlines()

        # 使用random.choice随机选择一行
    random_line = random.choice(lines)

    # 去掉选中行的前后空白符（包括换行符）
    return random_line.strip()


def run(proxy, start):
    ret = ""
    try:
        print("proxy:{}".format(proxy))
        # 不显示警告
        requests.packages.urllib3.disable_warnings(InsecureRequestWarning)

        s = requests.Session()
        proxies = {
            "https": "http://{}".format(proxy.strip()),
            "http": "http://{}".format(proxy.strip())
        }

        header = {
            'User-Agent': 'Mozilla/5.0 (Windows NT 10.0; Win64; x64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/58.0.3029.110 Safari/537.3'
        }

        ret = s.get(url='https://movie.douban.com/j/new_search_subjects?sort=T&tags=&start=' + str(start),
                    headers=header, proxies=proxies, timeout=10, verify=False)
        rc = ret.content.decode("utf-8")
        print("now2 start is：{}".format(start))
        print("rc:{}".format(rc))
        analysisRemoteResult(ret, start)

    except Exception as e:
        addText("\n" + str(start), 'film-insert-start-todo.txt')
        pass



def analysisRemoteResult(response, start):
    if response.status_code == 200:
        print("success start is：{}".format(start))

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
        print("run 发生异常：", e)
        addText("\n" + str(start), 'film-insert-start-todo.txt')
        print(f'Error: Failed to fetch data. Status code: {response.status_code}')
        exit()

def addText(content, fileName):
    with open(fileName, 'a', encoding='utf-8') as file:
        # 在文件末尾追加文本
        file.write(content)


if __name__ == '__main__':
    # 如果以这个文件为启动文件就释放下面这行
    # app.run(host="0.0.0.0", port=8989, debug=True)

    # while True:
    # allPages = [4201, 2861]
    # for i in allPages:
    for i in range(1, 3, 20):
        proxyLine = getProxysFromFile()

        random_number = random.randint(1, 5)
        time.sleep(random_number)
        print("now start is:" + str(i))
        try:
            t=threading.Thread(target=run,args=(proxyLine, i))
            t.start()
        except Exception as e:
            print("线程出错！{}", e)
            pass
