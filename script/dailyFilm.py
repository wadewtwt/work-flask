import requests
from bs4 import BeautifulSoup
import re
import sys
import os

common_dir = os.path.abspath(os.path.join(os.path.dirname(__file__),  '..'))
sys.path.append(common_dir)

from common.mysql_operate import db
from flask import Flask
import datetime
import time
from apscheduler.schedulers.background import BackgroundScheduler
from utils.file_util import FileUtil


app = Flask(__name__)

def newestMovieWork():
    fileUtil = FileUtil()
    fileUtil.append_text("log/dailyFilmLog.txt", "newestMovieWork is doing!")
    print("newestMovieWork doing!")

    url = 'https://movie.douban.com/chart'
    headers = {
        'User-Agent': 'Mozilla/5.0 (Windows NT 10.0; Win64; x64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/58.0.3029.110 Safari/537.3'
    }
    response = requests.get(url, headers=headers)
    soup = BeautifulSoup(response.text, 'html.parser')

    items = soup.find_all('tr', class_='item')
    for item in items:
        a_img = item.find('img')
        imgText = a_img.attrs['src']

        movies = soup.find_all('div', class_='pl2')
        for movie in movies:
            a_tag = movie.find('a')
            hrefText = a_tag.get('href')
            titleText = ''
            for elem in a_tag.contents:
                if elem.name != 'span':
                    titleText += str(elem).strip().replace(" ", "").replace("/", "").replace("\n", "")
            ratingText = movie.find('span', class_='rating_nums').text.strip()

            # 判断是否存在，有就返回
            listByTitle = selectBytitle(titleText)
            if len(listByTitle) > 0:
                print("已经存在：{}".format(titleText))
                continue

            print(f'Title: {titleText}, Rating: {ratingText}, hrefText:{hrefText}, imgText:{imgText}')
            addFilmSql(titleText, imgText, hrefText, ratingText, "",0, "", 0, 0, 0);

def addFilmSql(title, cover, url, rating, casts, star, directors, cover_x, cover_y, other_id):
    sql3 = "INSERT INTO a_film(title, cover, url, rating, casts, star, directors, cover_x, cover_y, other_id) " \
           "VALUES(%s, %s, %s, %s, %s, %s, %s, %s, %s, %s)"

    print("title is:" + title)
    db.execute_db_params(sql3, (title, cover, url, rating, casts, star, directors, cover_x, cover_y, other_id))

def selectBytitle(title):
    sql1 = "SELECT id,title FROM a_film WHERE title = '{}'".format(title)
    res1 = db.select_db(sql1)
    return res1

if __name__ == '__main__':
    db.change_db(1)

    # 创建后台执行的 schedulers
    scheduler = BackgroundScheduler()
    # 添加调度任务
    # 调度方法为 timedTask，触发器选择 interval(间隔性)，间隔时长为 2 秒（seconds，hours）
    scheduler.add_job(newestMovieWork, 'interval', hours=1)
    # 启动调度任务
    scheduler.start()

    while True:
        print(time.time())
        time.sleep(60)

