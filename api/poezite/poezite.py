import threading
from utils.file_util import FileUtil
from common.mysql_operate import db
import html2text
import re


def run(params):
    try:
        sql = "SELECT * FROM article where id in(44,45,46,47,49,53,54,55,56,57,58,59,61,63,64,65,66,78,95,116)"
        # sql = "SELECT * FROM article where id in(51)"
        list = db.select_db(sql)
        for item in list:
            articleContent = item['article_content']
            id = item['id']
            print("\n now id is:" + str(id))

            # 3.处理内容第一张图片为封面
            matchFirstImg(id, articleContent)


            # 2.处理图片
            # matchImg(articleContent)

            # 1.处理html转markdown
            # newArticleContent = html2text.html2text(articleContent)
            # newArticleContent = newArticleContent.replace("'", "\"")
            # sql3 = "UPDATE article SET article_content = '{}' " \
            #        "WHERE id = {}".format(newArticleContent, id)
            # db.execute_db(sql3)

    except Exception as e:
        print("run error:{}", e)
        exit()

def matchFirstImg(id, content):
    # pattern = r"http?://.*?\.(?:png|jpg|jpeg)"
    pattern = r'!\[.*?\]\((https?://[^\s]+)\)'
    # pattern = r'(https?://\S+\.(?:png|jpg|jpeg|gif))'
    pattern = r'!\[.*?\]\((http[s]?://[^\s]+)\)'
    # pattern = r"http?://[^/]+/(.*)"
    # pattern = r"http?://.*?\.(?:png|jpg|jpeg)"



    match = re.search(pattern, content)
    if match:
        firstImg = match.group(1)
        sql = "UPDATE article SET article_cover = '{}' " \
                       "WHERE id = {}".format(firstImg, id)
        db.execute_db(sql)


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
