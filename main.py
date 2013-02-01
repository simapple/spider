#coding:cp936
import threading,Queue
from collections import deque
from toolhand import *
class multigeturl(threading.Thread):
    '''线程'''
    global temp
    def __init__(self,queue,threadname,logger,lock):
        threading.Thread.__init__(self,name=threadname)
        self.queue = queue
        self.lock = lock
        self.logger = logger
        self.tmp = []
    def run(self):
        while True:
            info = self.queue.get()
            if self.lock.locked():
                self.tmp.append(info)
                pass
            else:
                self.lock.acquire()
                db = dbhand(self.logger)
                dbfile = "todayb.db"
                db.dbconnect(dbfile)
                db.initdatabase()#数据表初始化
                print info,self.getName()
                for tt in self.tmp:
                    allstar(tt,db)
                self.tmp = []
                self.lock.release()
            self.queue.task_done()
        self.queue.task_done()
def main():
    start = {}
    start['url'] = "http://www.hao123.com"
    logop = {}
    logop['logfile'] = "log.txt"#uop['logfile']
    logop['loglevel'] = "INFO"#uop['level']
    global logger
    logger = getlog(logop)#构造log对象
    global db
    db = dbhand(logger)
    dbfile = "todayb.db"
    db.dbconnect(dbfile)
    db.initdatabase()#数据表初始化
    db.selecturls2()
    db.insertone(start,'urls')
    queue = Queue()
    threadnumber = 30
    lock = threading.Lock()
    for i in range(threadnumber):#初始化线程池
        t1 = multigeturl(queue,'urlt_'+str(i),logger,lock)
        t1.setDaemon(True)
        t1.start()
    allurl = db.selecturls2()

    while True:
        while len(allurl) > 0:

            t = allurl.pop()
            queue.put(t)
        allurl = db.selecturls2()
        queue.join()

if __name__ == "__main__":
    main()
