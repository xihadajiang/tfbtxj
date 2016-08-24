#!/usr/bin/python
import sys,time,json,logging
import Queue, threading, datetime
from lib.base.daemon import Daemon
from lib.queue.httpsqs.HttpsqsClient import HttpsqsClient
from lib.db.DbMongodb import DbMongodb
logging.basicConfig(level=logging.DEBUG,
                format='%(asctime)s %(filename)s[line:%(lineno)d] %(levelname)s %(message)s',
                datefmt='%a, %d %b %Y %H:%M:%S',
                filename='myapp.log',
                filemode='w')
                 
queue = Queue.Queue()       
httpsqs = HttpsqsClient('192.168.0.218','1218','httpsqs.com')
db = DbMongodb('192.168.0.119','testdb')
         
class ThreadGetHttpSqs(threading.Thread):
    def __init__(self):
        threading.Thread.__init__(self)
        self.httpsqs = httpsqs
        self.queue = queue
     
    def run(self):
        while True:
            data = self.httpsqs.get('logtest')
            if data is not None:
                self.queue.put(data)
                logging.info('get:id %s , tablename %s' % (self.getName(),data))
            else:
                time.sleep(3)
             
             
             
class ThreadInsertDB(threading.Thread):
    def __init__(self):
        threading.Thread.__init__(self)
        self.queue = queue
        self.db = db
         
    def run(self):
        while True:
            chunk = self.queue.get()
            s = json.loads(chunk)
            tablename = s['table']
            data = s['data']
            self.db.save(tablename,data)
            logging.info('insert:id %s , tablename %s' % (self.getName(),tablename))
            self.queue.task_done()
             
class MyDaemon(Daemon):
    def _run(self):
        while True:
            for i in range(2):
                t = ThreadGetHttpSqs()
                #t.setDaemon(True)
                t.start()
             
            for i in range(2):
                b = ThreadInsertDB()
                #t.setDaemon(True)
                b.start()
            #线程已经为永真循环，进程不能再循环
            time.wait()
             
                 
                
if __name__ == "__main__":
    daemon = MyDaemon('/tmp/daemon-example.pid')
    if len(sys.argv) == 2:
        if 'start' == sys.argv[1]:
            daemon.start()
        elif 'stop' == sys.argv[1]:
            daemon.stop()
        elif 'restart' == sys.argv[1]:
            daemon.restart()
        else:
            print "Unknown command"
            sys.exit(2)
        sys.exit(0)
    else:
        print "usage: %s start|stop|restart" % sys.argv[0]
        sys.exit(2)