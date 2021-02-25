from flask import Flask
app = Flask(__name__)



# 导入views.py,以注册视图函数
from foodisplay import views