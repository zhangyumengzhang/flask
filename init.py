import pymysql
from flask import Flask
from flask_sqlalchemy import SQLAlchemy

import config

pymysql.install_as_MySQLdb()
app = Flask(__name__)
app.config.from_object(config)
# 创建数据库对象
db = SQLAlchemy(app)