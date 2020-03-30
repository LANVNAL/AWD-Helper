from func import *
import requests
import threading
import sched, time


def test_live(s,second):
    ips = db.session.query(Target.ip).all()
    for i in range(len(ips)):
        ips[i] = ips[i][0]

    for ip in ips:
        url = 'http://' + ip
        try:
            test = requests.get(url=url, timeout=0.5)
            if test.status_code == 200:
                print 'ok'
            else:
                print 'no'
        except:
            print 'no'
    print 'finish once'
    s.enter(second, 1, test_live,(s,second))


def do(second):
    s = sched.scheduler(time.time, time.sleep)
    s.enter(second, 1, test_live,(s,second))
    s.run()

thread = threading.Thread(target=do,args=(10,))
thread.start()
print 'aa'