import requests
from urllib.parse import urlparse
import re
import os

from utils.time_util import TimeUtil


class FileUtil:
    # 追加文字记录
    def append_text(self, filename, text):
        timeUtil = TimeUtil()
        """
        将文本内容追加到文件末尾。
        :param text: 要追加的字符串。
        """
        with open(filename, 'a', encoding='utf-8') as file:
            file.write(timeUtil.getNowFormatTimeString() + ":" + text)

    # 下载图片
    def download_image(self, remoteUrl, pathFilename):
        pathFilename = ""
        if pathFilename == "":
            pathFilename = FileUtil.get_path_filename_from_url(remoteUrl)

        # 发送HTTP GET请求
        response = requests.get(remoteUrl, proxies={"http": None, "https": None})

        # 检查请求是否成功
        if response.status_code == 200:
            # directory = os.path.dirname(pathFilename)
            # if directory != "":
            #     if not os.path.exists(directory):
            #         os.makedirs(directory)
            # 打开一个文件用于写入二进制数据
            with open(pathFilename, 'wb') as file:
                # 写入图片的二进制数据
                file.write(response.content)
            print(f"图片已下载并保存为：{pathFilename}")
        else:
            print(f"图片下载失败，状态码：{response.status_code}")

    def get_filename_from_url(url):
        """
        从图片URL中提取文件名。
        :param url: 图片的URL地址。
        :return: 提取的文件名。
        """
        # 解析URL
        parsed_url = urlparse(url)
        # 获取URL中的路径部分
        path = parsed_url.path
        # 从路径中提取文件名
        filename = path.split('/')[-1]
        return filename

    # 获取这个url上除了域名的整个包含文件名的路径
    def get_path_filename_from_url(url):
        match = re.search(r"https?://[^/]+/(.*)", url)
        path = ""
        if match:
            # 打印匹配到的路径部分
            path = match.group(1)

            # 加的
            if path.find("?"):
                pattern = r'^(.*?)\?'
                match2 = re.search(pattern, path)
                if match2:
                    path = match2.group(1)

        return path

