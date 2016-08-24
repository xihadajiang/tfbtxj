#!/usr/bin/env python
# coding: gbk

import os , cStringIO

def get_process( name , filter ):
    r = os.popen( 'ps -ef|grep ' + name )
    s = cStringIO.StringIO( r.read() )
    pid = None
    for l in s:
        if filter( l ):
            return l.split()[1]

def fcgi( x ):
    if 'python suning.pid' in x:
        d = x.split()
        if d[2] == '1':
            return d[1]
            
def start():
    print '启动 suning ...'
    if get_process( 'suning' , lambda x: 'python suning' in x ):
        print 'suning 已经启动'
    else:
        os.system( 'nohup python suning.py -l 192.168.30.137:11014 -r 192.168.30.137:20054 -v > myout.log 2>&1 &' )
        print 'suning 启动完毕'
        
    print '启动 httpserver ...'
    if get_process( 'httpserver' , lambda x: 'jython.jar httpserver'  in x ):
        print 'httpserver 已经启动'
    else:
        os.system( 'nohup java -jar /home/gaps32/Jython/jython.jar tx_httpserver.py > tx_httpserver.log 2>&1 &')
        #os.system( 'nohup java  -Dfile.encoding=utf-8 -jar /home/gaps32/Jython/jython.jar tx_httpserver1.py > tx_httpserver.log 2>&1 &')
        print 'httpserver 启动完毕'
    
    #print '启动 用户在线状态处理进程'
    #os.system( 'python %s/schrun.py start' % os.path.join( os.environ[ 'HOME' ] , 'bin' ) )
    #print '启动nginx：nginx -c /home/kxst/bin/httpd.conf'
    #print '启动memcached: memcached -m 256 -d'

def stop():
    pid = get_process( 'python suning' , fcgi )
    if pid:
        os.system( 'kill -15 ' + pid )
        print '苏宁通讯机关闭成功'
    else:
        print '苏宁通讯机未启动，不需关闭'
        
    #print '停止 用户在线状态处理进程'
    #os.system( 'python %s/schrun.py stop' % os.path.join( os.environ[ 'HOME' ] , 'bin' ) )
    
def stopall():
    stop()
    pid = get_process( 'httpserver' , lambda x: 'jython.jar httpserver' in x )
    if pid:
        os.system( 'kill ' + pid )
        print 'httpserver 关闭成功'
    else:
        print 'httpserver未启动，不需要关闭'

    pid = get_process( 'suning' , lambda x: 'python suning' in x )
    if pid:
        os.system( 'kill ' + pid )
        print 'suning 关闭成功'
    else:
        print 'suning未启动，不需要关闭'
    
if __name__ == '__main__':
    import sys
    n = sys.argv[-1]
    if n.lower() == 'start':
        start()
    elif n.lower() == 'stop':
        stop()
    elif n.lower() == 'stopall':
        stopall()
    else:
        print '不支持该命令：' , n