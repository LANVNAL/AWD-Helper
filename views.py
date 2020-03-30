#-*- coding:utf-8 -*-
from flask import render_template, request, redirect, url_for, flash
from db import *
from __init__ import app
from func import *
import os,time

@app.route('/')
def hello_world():
    return 'Hello World!'

@app.route('/target', methods=['GET', 'POST'])
def target(server=None,data=None):
    target_server = get_target_server()
    control_status = get_shell_status()
    target_msg = []
    if request.args.get("server"):
        servers = request.args.get("server")
        target_msg = get_target(servers)
    else:
        if len(target_server) != 0:
            target_msg = get_target(target_server[0])
        else:
            target_server = []
    if request.form.get('add_one', None) == '手动添加':
        server = request.form['server']
        ip = request.form['ip']
        status = request.form['status']
        remarks = request.form['remarks']
        add_target(server, ip, status, remarks)
        return redirect(url_for('target',server=server))
    if request.form.get('nmap', None) == 'Nmap扫描':
        server = request.form['server']
        ips = request.form['ips']
        do_background(live_host, ips, server)
        return redirect(url_for('target', server=server))
    if request.form.get('status', None) == '开始监测各主机状态':
        second = int(request.form['second'])
        do_background(cycle_do, second, test_live)
    if request.form.get('flush_remarks', None) == '更新':
        new = request.form['new_remark']
        ip = request.form['hid_ip']
        update_remarks(ip, new)
    if request.form.get('delete', None) == '确认删除':
        ip = request.form['hid_ip']
        print ip
        delete = delete_target(ip)
        if delete == 'error':
            flash("存在相同ip的多条记录")
            return redirect(url_for('target', server=server))
        return redirect(url_for('target', server=server))
    return render_template('target.html', server=target_server, data=target_msg, control_status=control_status)

@app.route('/shell', methods=['GET', 'POST'])
def shell(server_show=None,server=None):
    module_path = os.path.dirname(__file__)
    shell_path = module_path + '/file/shell/'
    shells = os.listdir(shell_path)
    target_server = get_target_server()
    if request.args.get("server"):
        server_show = request.args.get("server")
        target_msg = get_target(server_show)
    else:
        if len(target_server) != 0:
            target_msg = get_target(target_server[0])
        else:
            target_msg = []
    if request.form.get('add_one', None) == '提交':
        server = request.form['server']
        ip = request.form['ip']
        shell = request.form['one-shell']
        if request.form.get("all_same") != None:
            all_same = 'yes'
        else:
            all_same = 'no'
        add_shell(server, ip, shell, all_same)
        return redirect(url_for('shell', server=server))
    if request.form.get('memory_shell', None) == '一键上内存马':
        server = request.form['server']
        pwd = request.form['pwd']
        if request.form['shell_path']:
            path = request.form['shell_path']
        else:
            path = './.config.php'
        one_key_shell(server,pwd,path)
    if request.form.get('send_bshell', None) == '上大马':
        ip = request.form['ip']
        bshell_path = request.form['bshell_path']
        bshell = request.form['big_shell']
        msg = send_bshell(ip, bshell, bshell_path)    #会返回是否成功

    return render_template('shell.html', server=target_server, server_show=server_show, data=target_msg, shells=shells)

@app.route('/flag/<int:method>',methods=['GET', 'POST'])
def flag(method):
    if method == 1: #获取flag本地提交
        if request.args.get("submit"):
            command = request.form['command']
            receive = request.form['receive']
        return render_template('flag1.html')

@app.route('/filelog', methods=['GET', 'POST'])
def filelog():
    module_path = os.path.dirname(__file__)
    path = module_path + '/file/logs/filelog.txt'
    if request.values.get('msg'):
        log = open(path,'a')
        msg = request.values.get('msg')
        log.write('======'+time.strftime("%H:%M:%S", time.localtime())+'======' + '\n')
        log.write(msg + '\n')
        log.close()
        return 'OK'
    log = open(path, 'r').read().replace('\n', '<br>')
    return render_template("filelog.html", log=log)

@app.route('/processlog', methods=['GET', 'POST'])
def processlog():
    module_path = os.path.dirname(__file__)
    path = module_path + '/file/logs/processlog.txt'
    if request.values.get('msg'):
        log = open(path,'a')
        msg = request.values.get('msg')
        log.write(msg + '\n')
        log.close()
        return 'OK'
    log = open(path, 'r').read().replace('\n', '<br>')
    return render_template("processlog.html", log=log)