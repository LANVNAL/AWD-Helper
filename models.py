#-*- coding:utf-8 -*-
from flask_sqlalchemy import SQLAlchemy
from __init__ import app
import re


db = SQLAlchemy(app)

class Target(db.Model):
    __tablename__ = 'target'
    id = db.Column(db.INT, primary_key=True)
    server = db.Column(db.String(64))
    ip = db.Column(db.String(64))
    time = db.Column(db.Time)
    status = db.Column(db.String(64))
    remarks = db.Column(db.String(64))

    def __init__(self, server, ip, time, status, remarks):
        self.server = server
        self.ip = ip
        self.time = time
        self.status = status
        self.remarks = remarks

    def __repr__(self):
        return '<server {},ip {}>'.format(self.server,self.ip)

