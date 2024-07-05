import threading
from utils.file_util import FileUtil
from common.mysql_operate import db
import html2text
import re


def run(params):
    try:
        sql = "SELECT * FROM article where id in(25,30,31,33,35,37,38,40,48,49,50,51,66,71,74,75,80,83,85,86,87,88,89,92,95,96,101,102,103,104,111,116,118,122,130,131,134,135,136,138,140,142,145,146,148,151,153,159,160,162,163,178,180,200,211,214)"
        # sql = "SELECT * FROM article where id in(51)"
        list = db.select_db(sql)
        for item in list:
            articleContent = item['article_content']
            id = item['id']
            print("\n now id is:" + str(id))
            matchImg(articleContent)
            # newArticleContent = html2text.html2text(articleContent)
            # newArticleContent = newArticleContent.replace("'", "\"")
            # sql3 = "UPDATE article SET article_content = '{}' " \
            #        "WHERE id = {}".format(newArticleContent, id)
            # db.execute_db(sql3)

    except Exception as e:
        print("run error:{}", e)
        exit()

def matchImg(content):
    pattern = r'(https?://\S+\.(?:png|jpg|jpeg|gif))'
    pattern = r'这里插入图片描述\]\((.*?)\?'
    pattern = r"!\[.*?\]\((.*?)\)"
    pattern = r"https?://.*?\.(?:png|jpg|jpeg)"

    image_urls = re.findall(pattern, content)
    fileUtil = FileUtil()

    for image_url in image_urls:
        fileUtil.download_image(image_url, "")
        print(image_url)


def addText(content, fileName):
    with open(fileName, 'a', encoding='utf-8') as file:
        # 在文件末尾追加文本
        file.write(content)

if __name__ == '__main__':
    # 这边初始化选择数据库
    db.change_db(2)

    id = 0
    try:
        t = threading.Thread(target=run, args=(id, ))
        # 如果是单个，这样写 args = (age, )
        t.start()
    except Exception as e:
        print("线程出错！{}", e)
        pass
