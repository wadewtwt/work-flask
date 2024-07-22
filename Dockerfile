# 使用官方的Python运行时作为父镜像
FROM python:3.8
# 设置工作目录为/app
WORKDIR /app
# 将当前目录内容复制到位于 /app 的容器中
COPY . /app
# 安装任何需要的包
RUN pip install -r requirements.txt
# RUN pip install -r requirements.txt -i https://pypi.tuna.tsinghua.edu.cn/simple

# 对外暴露的端口号
EXPOSE 13003

# 当容器启动时运行python app
.py
#CMD ["python", "app.py"]
