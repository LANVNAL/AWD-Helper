# -*- coding:utf-8 -*-
from flask import Flask
import sys
reload(sys)
sys.setdefaultencoding('utf8')

app = Flask(__name__)
app.config['SECRET_KEY'] = 'qweasdzxc!@#'
app.config['JSON_AS_ASCII'] = False
app.config['SQLALCHEMY_DATABASE_URI'] = 'mysql://root:Mysqlp@ssw0rd@localhost:3306/awdtest?charset=utf8mb4'
app.config['SQLALCHEMY_TRACK_MODIFICATIONS'] = True



