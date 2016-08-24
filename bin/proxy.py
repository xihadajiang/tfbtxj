#!/usr/bin/env jython
# coding: utf-8
import socket, re, sys, threading
from optparse import OptionParser
import sys
import logging,logging.handlers
import datetime
import cStringIO
import base64
import socket, threading  
import re
import changeMsgFamt
from utils.ftools import AttrDict
import flow.flow_utils
from conf import settings
settings.register( 'oaconf' )
SERVER = '127.0.0.1' #主机IP  
#SERVER = '192.168.30.137' #主机IP  
PORT = 9302 #端口号' 
BUFLEN = 1024*10
from utils import log
import os
class connector(threading.Thread):
    def __init__(self):
        threading.Thread.__init__(self)
        self.sock = socket.socket(socket.AF_INET, socket.SOCK_STREAM)
        #self.req = req

    def run(self,req):
        try:
            self.sock.connect((SERVER,PORT))
            self.sock.send(req)
            print '>>>>>sent ',req            
            rstr = self.sock.recv(BUFLEN)
            print 'received>>>>>>>',rstr
            self.sock.close()
            return rstr
        except socket.error,e:
            print e
            return e

today = datetime.datetime.today()
rq = today.strftime('%Y%m%d')
#def initlog(logfile):
#    LOG_FILENAME="../logs/%s"%logfile
#    log = logging.getLogger('')  # 拿到root logger，你也可以设置自己的logger
#    log.setLevel(logging.DEBUG)
#    format = "%(asctime)s %(filename)s[line:%(lineno)d]%(message)s"
#    formater = logging.Formatter(format)
#    handler = logging.handlers.TimedRotatingFileHandler(LOG_FILENAME, "H", 2, 0)
#    handler.suffix = "%Y%m%d%H.log"  # 设置后缀
#    handler.setFormatter(formater)
#    log.addHandler(handler)
#    return log

di = { '0' : '0000' ,
       '1' : '0001' ,
       '2' : '0010' ,
       '3' : '0011' ,
       '4' : '0100' ,
       '5' : '0101' ,
       '6' : '0110' ,
       '7' : '0111' ,
       '8' : '1000' ,
       '9' : '1001' ,
       'A' : '1010' ,
       'B' : '1011' ,
       'C' : '1100' ,
       'D' : '1101' ,
       'E' : '1110' ,
       'F' : '1111'
     }
def to_hex( s ):
    st = cStringIO.StringIO()

    def fmt( x ):
        if ord( ' ' ) <= ord( x ) <= ord( '\x7E' ):
            return x
        return '.'
    i = 0
    end = 0
    line = ''
    if type( s ) != str:
        s = str( s )
    for c in s:
        i += 1
        if i % 16 == 1:
            line += '%04X: ' % ( i - 1 , )
        line += '%02X ' % ord(c)
        if i % 8 == 0 and ( i / 8 ) % 2 == 1 :
            line += '- '
        if i % 16 == 0:
            line += ' ' + ''.join( map( fmt , s[i-16:i] ) )
            st.write( line + '\n' )
            line = ''
            end = i
    if line :
        line += ' ' * ( 56 - len( line ) )
        st.write( line )
        st.write( ' ' + ''.join( map( fmt , s[end:] ) ) + '\n' )
    return st.getvalue()


def lineno():
    frame = None
    try:
        raise ZeroDivisionError
    except ZeroDivisionError:
        frame = sys.exc_info()[2].tb_frame.f_back
    return frame.f_lineno

class Log():
    def __init__(self,msg):
        if verbose:
            #with threading.Lock():
            print msg

class ParserClass():
    def __init__(self):
        self.re_ip_port = r'^(?P<addr>.+:)?(?P<port>[0-9]{1,5})$'
    
    def pares(self):
        
        parser = OptionParser(usage='%prog -l [host:]port -r host:port [-m] [-v]', version='%prog 0.1')
        parser.add_option('-l', dest='local', help='local addr(optional) & port: 0.0.0.0:8208 or 8208')
        parser.add_option('-r', dest='remote', help='remote addr & & port: 0.0.0.0:3306 or 3306')
        parser.add_option('-s', dest='systemsign', help='接入标识')
        parser.add_option('-m', dest='maxsvr', default=5, help='print stat to screen')
        parser.add_option('-f', dest='debugflag', default=True,  help='print stat to screen')
        parser.add_option('-v', dest='verbose', default=False, action='store_true', help='print stat to screen')
        
        (options, args) = parser.parse_args()
        print (options, args)
        if not options.local or not options.remote:
            parser.print_usage()
            sys.exit(-1)
            
        x = re.match(self.re_ip_port, options.local)
        print x
        if not x:
            parser.error('local addr port parser error!')
        local_addr = x.group('addr') or '0.0.0.0'
        local_addr = local_addr.rstrip(':')
        print local_addr
        local_port = x.group('port')
        if not local_port:
            parser.error('local port error!')
        local_port = int(local_port)
        
        
        x = re.match(self.re_ip_port, options.remote)
        print x
        if not x:
            parser.error('remote addr port parser error')
        remote_addr = x.group('addr') or '0.0.0.0'
        remote_addr = remote_addr.rstrip(':')
        
        remote_port = x.group('port')
        if not remote_port:
            parser.error('remote port error')
        remote_port = int(remote_port)
        
        systemsign = options.systemsign
        maxsvr = options.maxsvr
        debugflag = options.debugflag
        verbose = options.verbose
        
        return local_addr,local_port,remote_addr,remote_port,systemsign,maxsvr,debugflag,verbose
    
class Dispatch(threading.Thread):
    def __init__(self, sock_in, sock_out, name):
        threading.Thread.__init__(self)
        self.sock_in = sock_in
        self.sock_out = sock_out
        self.name = name
        self.maxpack = 1024*5000
        
    def run(self):
        addr_in = '%s:%d' % self.sock_in.getpeername()
        addr_out = '%s:%d' % self.sock_out.getpeername()
        
        while True:
            try:
                data = self.sock_in.recv(self.maxpack)
            except Exception, e:
                log.info( systemsign , 'line[%s] Dispatch Socket read error of %s: %s' , lineno(),addr_in, str(e))
                break
            if not data:
                log.info( systemsign ,'无数据break')
                break
            elif data.strip() == '0':
                break
            log.info( systemsign ,'从GAPS接收到的数据：【%s】',data)
            jyzd = {}
            pub = {'subsysname':systemsign}
            jyzd["pub"] = pub
            jyzd["systemsign"] = systemsign
            jyzd["subsysname"] = systemsign
            jyzd["name"] = self.name
            jyzd["commbuf"] = data
            print 'start flow'
            #jyzd["systemsign"] = 'subflow_sys_guocai_local2remote'
            ret = flow.flow_utils.goflow("../flow/%s.flow"%jyzd.get("systemsign"),jyzd)
            print ret
            data = jyzd.get("resp","")
#            if self.name == 'local -> remote':
#                if len(data) > 4:
#                    print '%s line[%s]【%s】end\n'%(self.name,lineno(),data)
#                    logging.debug( """\n--------------开始分级日志 BEGIN[%s]---------------\n"""%(datetime.datetime.now()))
#                    logging.debug('从GAPS接收到的数据：【%s】'%data)
#                    logging.debug( "############# GAPS->SF ################:\n%s\n"%to_hex( data ))
#                    data = changeMsgFamt.local2remote(data)
#                    logging.debug('发往三方的数据：【%s】'%data)
#                    try:
#                        self.sock_out.sendall(data)
#                        logging.debug('报文发往送到三方成功')
#                    except Exception, e:
#                        logging.debug('line[%s] Dispatch Socket write error of %s: %s' % (lineno(),addr_out, str(e)))
#                        break
#            else:
#                if 'HTTP' not in data:
#                    print '%s line[%s]【%s】end\n'%(self.name,lineno(),data)
#                else:
#                    logging.debug('从三方接收到的数据：【%s】'%data)
#                    logging.debug( "############# SF->GAPS ################:\n%s\n"%to_hex( data ))
#                    data = changeMsgFamt.remote2local(data)
#                    logging.debug('发往GAPS的数据：【%s】'%data)
#                    try:
#                        self.sock_out.sendall(data)
#                        logging.debug('报文发往送到GAPS成功')
#                        logging.debug( """\n--------------提交缓冲日志 END[%s]---------------\n"""%(datetime.datetime.now()))
#                    except Exception, e:
#                        logging.debug('line[%s] Dispatch Socket write error of %s: %s' % (lineno(),addr_out, str(e)))
#                        break
            #print 'line[%s]【%s】end\n'%(lineno(),data)
            #Log('line[%s] %s => %s (%d bytes) %s ' % (lineno(),addr_in, addr_out, len(data), self.name))
            try:
                log.info( systemsign ,'从三方接收到的数据：【%s】',data)
                self.sock_out.sendall(data)
                log.info( systemsign ,'报文发往送到GAPS成功')
                log.info( systemsign , """\n--------------提交缓冲日志 END[%s]---------------\n"""%(datetime.datetime.now()))
            except Exception, e:
                log.info( systemsign ,'line[%s] Dispatch Socket write error of %s: %s' ,lineno(),addr_out, str(e))
                break
        try:
            self.sock_out.shutdown(2)
        except Exception, e:
            self.sock_out.close()
        try:
            self.sock_in.shutdown(2)
        except Exception, e:
            self.sock_in.close()

class Proxy(threading.Thread):
    def __init__(self,socket,remote_addr,remote_port):
        threading.Thread.__init__(self)
        self.sock_in = socket
        self.remote_addr = remote_addr
        self.remote_port = remote_port
        
    def run(self):
        sock_out = socket.socket(socket.AF_INET, socket.SOCK_STREAM)
        try:
            print remote_addr, remote_port
            sock_out.connect((remote_addr, remote_port))
        except socket.error, e:
            self.sock_in.close()
            log.info( systemsign ,'Remote error: %s' % str(e))
            return

        t = Dispatch(self.sock_in, sock_out, 'local2remote')
        t.start()
        
        t = Dispatch(sock_out, self.sock_in, 'remote2local')
        t.start()

class Checker(threading.Thread):
    def __init__(self,socket,num):
        threading.Thread.__init__(self)
        self.sock_master = socket
        self.num = num
        print 'thread started!'

    def run(self):
        #self.socket.listen(2)
        while True:
            try:
                sock, addr = sock_master.accept()
                print sock, addr 
            except (KeyboardInterrupt, SystemExit):
                print 'Closing master'
                Log('Closing master')
                sock_master.close()
                sys.exit(1)
                
            t = Proxy(sock,remote_addr, remote_port)
            t.start()
            #t.join(10)
            Log('New clients from %s:%d' % addr)



if __name__ == '__main__':
    local_addr,local_port,remote_addr,remote_port,systemsign,maxsvr,debugflag,verbose = ParserClass().pares()
    #print proxy.py -l 127.0.0.1:8208 -r 127.0.0.1:3306 -v
    #python proxy.py -l 192.168.40.241:8008 -r 192.168.100.37:8008 -v
    print local_addr,local_port,remote_addr,remote_port,systemsign,maxsvr,debugflag,verbose
    log.init_log( systemsign ,LOGDIR = settings.LOGDIR, screen = True )

    try:
        sock_master = socket.socket(socket.AF_INET, socket.SOCK_STREAM)
        sock_master.setsockopt(socket.SOL_SOCKET,socket.SO_REUSEADDR,1)
    except socket.error,e:
        log.info( systemsign , 'Strange error creating socket: %s' ,str(e) )
        sys.exit(1)
    try:
        print local_addr, local_port
        sock_master.bind((local_addr, local_port))
        sock_master.listen(5)
    except socket.error,e:
        log.info( systemsign , 'socket bind error : %s',str(e) )
        sock_master.close()
        sys.exit(1)
    log.info( systemsign , 'Listening at %s:%d ...' ,local_addr, local_port)
    i = 0
    chkerlist = []
    while i < int(maxsvr):
        chker = Checker(sock_master,i)
        chker.start()
        i = i + 1
        print i
        chkerlist.append(chker)
    for chker in chkerlist:
        chker
        chker.join()
    print 'ending'

