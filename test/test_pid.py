import psutil, time, sys, requests


#for pid in pids:
#    p = psutil.Process(pid)
#    print("pid-%d,pname-%s" % (pid, p.name()))

def get_pids():
    process = {}
    pids = psutil.pids()
    for pid in pids:
        p = psutil.Process(pid)
        try:
            command = " ".join(p.cmdline())
        except:
            command = ""
        process[pid] = p.name() + " " + command
    return process

def compare(url):
    now_pids = get_pids()
    global pids
    for pid in now_pids:
        if pid not in pids:
            print "@" + time.strftime("%H:%M:%S", time.localtime()) + "--add--" + str(pid) + "--" + now_pids[pid]
            msg = "@" + time.strftime("%H:%M:%S", time.localtime()) + "--add--" + str(pid) + "--" + now_pids[pid]
            send_diff(msg, url)
    for pid in pids:
        if pid not in now_pids:
            print "@" + time.strftime("%H:%M:%S", time.localtime()) + "---loss--" + str(pid) + "--" + pids[pid]
            msg = "@" + time.strftime("%H:%M:%S", time.localtime()) + "---loss--" + str(pid) + "--" + pids[pid]
            send_diff(msg, url)
    pids = now_pids

def send_diff(msg,url):
    data = {'msg':msg}
    try:
        requests.post(url=url,data=data)
    except:
        return

if __name__ == "__main__":
    if len(sys.argv) != 2:
        print 'Usage: ' + sys.argv[0] + "receive_url"
    pids = get_pids()
    while True:
        compare(sys.argv[1])
        time.sleep(5)