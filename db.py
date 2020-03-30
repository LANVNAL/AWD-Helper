#-*- coding:utf-8 -*-
from flask_sqlalchemy import SQLAlchemy
from __init__ import app
import re, time


db = SQLAlchemy(app)

class Target(db.Model):
    __tablename__ = 'target'
    id = db.Column(db.INT, primary_key=True)
    server = db.Column(db.String(64))
    ip = db.Column(db.String(64))
    time = db.Column(db.Time)
    status = db.Column(db.String(64))
    remarks = db.Column(db.String(64))


    def __repr__(self):
        return str({'server': self.server, 'ip': self.ip, 'time': self.time, 'status': self.status, 'remarks': self.remarks})

    def __getitem__(self, item):
        data = {'server': self.server, 'ip': self.ip, 'time': self.time, 'status': self.status, 'remarks': self.remarks}
        return data[item]

class Shell(db.Model):
    __tablename__ = 'shell'
    id = db.Column(db.INT, primary_key=True)
    server = db.Column(db.String(64))
    ip = db.Column(db.String(64))
    shell = db.Column(db.String(64))
    all_same = db.Column(db.String(20))

    def __repr__(self):
        return str({'server': self.server, 'ip': self.ip, 'shell': self.shell, 'all_same': self.all_same})

    def __getitem__(self, item):
        data = {'id': self.id, 'server': self.server, 'shell': self.shell, 'all_same': self.all_same}
        return data[item]

class Shell_control(db.Model):
    __tablename__ = 'shell_control'
    id = db.Column(db.INT, primary_key=True)
    ip = db.Column(db.String(64))
    shell = db.Column(db.String(64))
    status = db.Column(db.String(64))

    def __repr__(self):
        return str({'ip': self.ip, 'shell': self.shell, 'status': self.status})

    def __getitem__(self, item):
        data = {'ip': self.ip, 'shell': self.shell, 'status': self.status}
        return data[item]

def add_target(server, ip, status="no control", remarks=""):
    add_time = time.strftime("%H:%M:%S", time.localtime())
    new_target = Target(server=server, ip=ip, status=status, remarks=remarks, time=add_time)
    db.session.add(new_target)
    db.session.commit()

def get_target(server):
    data = Target.query.filter_by(server=server).all()
    if len(data) == 0:
        return []
    else:
        return data


def get_target_server():
    s = db.session.query(Target.server).distinct().all()
    data=[]
    for i in s:
        data.append(i[0])
    return data

def update_target_status(ip,status):
    exist = Target.query.filter_by(ip=ip).first()
    exist.status = status
    db.session.commit()

def update_remarks(ip, remark):
    data = Target.query.filter_by(ip=ip).first()
    if data:
        data.remarks = remark
        db.session.commit()
    else:
        return False

def delete_target(ip):
    num = Target.query.filter_by(ip=ip).count()
    if num > 1:
        return 'error'
    else:
        data = Target.query.filter_by(ip=ip).first()
        db.session.delete(data)
        db.session.commit()
        return True



def add_shell(server, ip, shell, all_same):
    new_shell = Shell(server=server, ip=ip, shell=shell, all_same=all_same)
    db.session.add(new_shell)
    db.session.commit()



def get_shell_urls(server):
    urls = []
    no_same = Shell.query.filter_by(server=server, all_same='no').all()
    for i in no_same:
        urls.append(i['shell'])
    one = Shell.query.filter_by(server=server, all_same='yes').all()
    path = re.findall(r'http://.+?(/.*)', one)[0]
    ips = get_target(server)
    for ip in ips:      #路径一样的全部添加进去
        ip = ip['ip']
        url = 'http://' + ip + path
        urls.append(url)
    return urls

def update_shell_status(shell_url,status):
    exist = Shell_control.query.filter_by(shell=shell_url).first()
    if exist:
        exist.status = status   #更新
        db.session.commit()
    else:
        ip = re.findall(r'http://(.+?)/.*', shell_url)[0]
        add = Shell_control(ip=ip,shell=shell_url,status=status)
        db.session.add(add)
        db.session.commit()




def get_shell_status():
    data = Shell_control.query.all()
    if len(data) == 0:
        return []
    else:
        return data


#add_target('web2','127.0.0.2','control','QAQ')
#print get_target()
#print get_target_server()
#get_shell('web1')
