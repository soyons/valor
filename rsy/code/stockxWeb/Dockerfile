# 使用 Python 官方镜像作为基础镜像

FROM python:3.9.19-slim
RUN mkdir ~/.pip && \
    echo "[global]" > ~/.pip/pip.conf && \
    echo "index-url = https://pypi.tuna.tsinghua.edu.cn/simple" >> ~/.pip/pip.conf

# 将工作目录设置为 /app
WORKDIR /cache

# 将当前目录的内容复制到容器中的 /app 
COPY ./requirements.txt /cache

# 安装 pip 依赖
RUN pip install -r requirements.txt

# 指定容器启动的命令
WORKDIR /app
