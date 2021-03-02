import os
import sys
from flask import Flask
from flask_sqlalchemy import SQLAlchemy
from flask_login import LoginManager

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
login_manager = LoginManager(app)

from foodisplay.models import User

@login_manager.user_loader
def load_user(user):
    if isinstance(user, User):
        return user
    elif isinstance(user, int):
        return  User.query.get(int(user))
    else:
        raise ValueError("user is not User or account")

login_manager.login_view = 'login'
login_manager.login_message = 'welcome to foodisplay'

# 导入各个子模块以完成注册
from foodisplay import views,commands