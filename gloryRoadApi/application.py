#encoding=utf-8

from flask import Flask
from flask_sqlalchemy import SQLAlchemy
import time

app = Flask('gloryRoadApi')

app.config.from_pyfile('settings.py')
app.jinja_env.trim_blocks = True
app.jinja_env.lstrip_blocks = True

# app传入SQLAlchemy类，返回SQLAlchemy对象赋值给db
db = SQLAlchemy(app)





