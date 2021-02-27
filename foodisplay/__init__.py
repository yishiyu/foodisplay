import os
import sys
from flask import Flask
from flask_sqlalchemy import SQLAlchemy

app = Flask(__name__)

# mysql URI compatible
import pymysql
pymysql.install_as_MySQLdb()
# 读取配置文件
import configparser
config = configparser.ConfigParser()
config.read("foodisplay.ini")
prefix = 'mysql://'
username = config['DATABASE']['username']
passwd = config['DATABASE']['passwd']
host = config['DATABASE']['host']
databasename = config['DATABASE']['databasename']
DATABASE_URI = '{}{}:{}@{}/{}'.format(prefix,username,passwd,host,databasename)

app.config['SECRET_KEY'] = os.getenv('SECRET_KEY', 'dev')
app.config['SQLALCHEMY_DATABASE_URI'] = DATABASE_URI
app.config['SQLALCHEMY_TRACK_MODIFICATIONS'] = False

db = SQLAlchemy(app)

# 导入各个子模块以完成注册
from foodisplay import views,commands