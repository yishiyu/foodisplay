FROM python:3.6
WORKDIR /Program/Flask

# 安装依赖
COPY requirements.txt ./
RUN pip install -r requirements.txt -i https://pypi.tuna.tsinghua.edu.cn/simple

# 复制项目文件
COPY . .

# 启动命令
CMD ["gunicorn", "start:app", "-c", "./gunicorn.conf.py"]