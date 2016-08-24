#!/usr/bin/env python
#coding:utf-8
import ConfigParser
import os
from optparse import OptionParser
import re
Usage = """python startcs.py 配置文件名
"""

def ini_get(INITXT):  #读取INI
    global SERVER
    global PORT
    config = ConfigParser.ConfigParser()
    config.readfp(open("../etc/%s"%INITXT))
    OIP = config.get("COMM","OIP")
    OPORT = config.get("COMM","OPORT")
    IPORT = config.get("COMM","IPORT")
    SYSTEMSIGN = config.get("COMM","SYSTEMSIGN")
    DEBUGFLAG = config.get("COMM","DEBUGFLAG")
    MAXSVR = config.get("COMM","MAXSVR")
    return OIP,OPORT,IPORT,SYSTEMSIGN,DEBUGFLAG,MAXSVR

def start(req):
    INITXT = req[0]
    OIP,OPORT,IPORT,SYSTEMSIGN,DEBUGFLAG,MAXSVR = ini_get("cs_%s.ini"%INITXT)
    print OIP,OPORT,IPORT,SYSTEMSIGN,DEBUGFLAG,MAXSVR
    print IPORT
    #os.system("""python guocai.py -l 0.0.0:8018 -r 127.0.01:8081 -s sys_jingdong -m 5 -f false -v"""%(SYSTEMSIGN))
    os.system("""python proxy.py -l 0.0.0.0:%s -r %s:%s -s %s -m %s -f %s -v"""%(IPORT,OIP,OPORT,SYSTEMSIGN,MAXSVR,DEBUGFLAG))
if __name__ == '__main__':
#    local_addr,local_port,remote_addr,remote_port,systemsign,maxsvr,debugflag,verbose = ParserClass().pares()
#    print local_addr,local_port,remote_addr,remote_port,systemsign,maxsvr,debugflag,verbose
    import sys
    fn = sys.argv[-1]
    if fn.endswith( 'startcs.py' ):
        print Usage
    else:
        print sys.argv
        start( sys.argv[1:2] )        
