#coding:utf-8
import socket, re, sys, threading
from optparse import OptionParser
import sys
import logging
import datetime
today = datetime.datetime.today()
rq = today.strftime('%Y%m%d')
LOG_FILENAME="txj_%s.log"%rq
logging.basicConfig(filename=LOG_FILENAME,level=logging.DEBUG)

import cStringIO
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
            with threading.Lock():
                print msg

class ParserClass():
    def __init__(self):
        self.re_ip_port = r'^(?P<addr>.+:)?(?P<port>[0-9]{1,5})$'
    
    def pares(self):
        
        parser = OptionParser(usage='%prog -l [host:]port -r host:port [-v]', version='%prog 0.1')
        parser.add_option('-l', dest='local', help='local addr(optional) & port: 0.0.0.0:8208 or 8208')
        parser.add_option('-r', dest='remote', help='remote addr & & port: 0.0.0.0:3306 or 3306')
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
        
        verbose = options.verbose
        
        return local_addr,local_port,remote_addr,remote_port,verbose
    
class Dispatch(threading.Thread):
    def __init__(self, sock_in, sock_out, name):
        threading.Thread.__init__(self)
        self.sock_in = sock_in
        self.sock_out = sock_out
        self.name = name
        self.maxpack = 1024*4
        
    def run(self):
        addr_in = '%s:%d' % self.sock_in.getpeername()
        addr_out = '%s:%d' % self.sock_out.getpeername()
        
        while True:
            try:
                data = self.sock_in.recv(self.maxpack)
            except Exception, e:
                Log('line[%s] Dispatch Socket read error of %s: %s' % (lineno(),addr_in, str(e)))
                break
    
            if not data:
                Log('line[%s] Dispatch Socket closed by %s: %s ' % (lineno(),addr_in,self.name))
                break
            if self.name == 'local -> remote':
                if 'POST11' in data:
                    print '%s line[%s]��%s��end\n'%(self.name,lineno(),data)
                    logging.debug('%s line[%s]��%s��end\n'%(self.name,lineno(),data))
                else:
                    print '%s line[%s]��%s��end\n'%(self.name,lineno(),data)
                    logging.debug('%s line[%s]��%s��end\n'%(self.name,lineno(),data))
                    print "############# SP->MSG ################:\n%s\n"%to_hex( data )
                    #from bwzh import *
                    #data = "%08d%s"%(len(http2gaps(data)),http2gaps(data))
                    print data
                    try:
                        self.sock_out.sendall(data)
                    except Exception, e:
                        Log('line[%s] Dispatch Socket write error of %s: %s' % (lineno(),addr_out, str(e)))
                        break
            else:
                if data.isdigit():
                    print '%s line[%s]��%s��end\n'%(self.name,lineno(),data)
                else:
                    print '%s line[%s]��%s��end\n'%(self.name,lineno(),data)
                    logging.debug('%s line[%s]��%s��end\n'%(self.name,lineno(),data))
                    #from bwzh import *
                    #data = gaps2http(data[8:])
                    #print '%s line[%s]ת��֮��%s��end\n'%(self.name,lineno(),data)
                    try:
                        self.sock_out.sendall(data)
                    except Exception, e:
                        Log('line[%s] Dispatch Socket write error of %s: %s' % (lineno(),addr_out, str(e)))
                        break
            #print 'line[%s]��%s��end\n'%(lineno(),data)
            Log('line[%s] %s => %s (%d bytes) %s ' % (lineno(),addr_in, addr_out, len(data), self.name))
            
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
            Log('Remote error: %s' % str(e))
            return

        t = Dispatch(self.sock_in, sock_out, 'local -> remote')
        t.start()
        
        t = Dispatch(sock_out, self.sock_in, 'remote -> local')
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
    local_addr, local_port, remote_addr, remote_port, verbose = ParserClass().pares()
    #print proxy.py -l 127.0.0.1:8208 -r 127.0.0.1:3306 -v
    #python proxy.py -l 192.168.40.241:8008 -r 192.168.100.37:8008 -v
    #python proxy.py -l 192.168.40.241:8080 -r 192.168.100.37:8080 -v
    #python proxy.py -l 192.168.40.241:1521 -r 192.168.100.37:1521 -v
    #python proxy.py -l 192.168.40.241:23 -r 192.168.100.37:23 -v
    #python proxy.py -l 192.168.40.241:21 -r 192.168.100.37:21 -v
    #python proxy.py -l 172.20.103.144:1522 -r 192.168.153.4:1521 -v
    #python proxy.py -l 192.168.253.64:22 -r 192.168.153.4:22 -v
    #python proxy.py -l 25.0.171.125:8008 -r 119.147.214.132:80 -v
    #python proxy.py -l 172.20.103.128:22 -r 192.168.153.4:22 -v
    #python proxy.py -l 172.20.103.128:22 -r 192.168.153.4:22 -v
    #python proxy.py -l 172.20.103.144:5006 -r 192.168.153.4:5006 -v    
    #python proxy.py -l 172.20.103.144:5007 -r 192.168.153.4:5007 -v    
    #python proxy.py -l 172.20.103.144:5008 -r 192.168.153.4:5008 -v    
    #python proxy.py -l 172.20.103.144:5011 -r 192.168.153.4:5011 -v    
    #python proxy.py -l 172.20.103.144:5012 -r 192.168.153.4:5012 -v    
    #python proxy.py -l 172.20.103.144:5013 -r 192.168.153.4:5013 -v    
    #python proxy.py -l 127.0.0.1:8081 -r 127.0.0.1:8080 -v    
    #python proxy.py -l 192.168.30.137:11018 -r 192.168.30.137:20055 -v    
    #python proxy.py -l 192.168.30.137:11016 -r 192.168.30.137:20056 -v    
    #python proxy.py -l 192.168.30.137:11014 -r 192.168.30.137:20054 -v    
    print local_addr, local_port, remote_addr, remote_port, verbose
    try:
        sock_master = socket.socket(socket.AF_INET, socket.SOCK_STREAM)
        sock_master.setsockopt(socket.SOL_SOCKET,socket.SO_REUSEADDR,1)
    except socket.error,e:
        print 'Strange error creating socket: %s' % str(e)
        sys.exit(1)
    try:
        print local_addr, local_port
        sock_master.bind((local_addr, local_port))
        sock_master.listen(5)
    except socket.error,e:
        print 'socket bind error : %s' % str(e)
        sock_master.close()
        sys.exit(1)
        
    Log('Listening at %s:%d ...' % (local_addr, local_port))
    
#    while True:
#        try:
#            sock, addr = sock_master.accept()
#            print sock, addr 
#        except (KeyboardInterrupt, SystemExit):
#            print 'Closing master'
#            Log('Closing master')
#            sock_master.close()
#            sys.exit(1)
#            
#        t = Proxy(sock,remote_addr, remote_port)
#        t.start()
#        #t.join(10)
#        Log('New clients from %s:%d' % addr)
    i = 0
    chkerlist = []
    while i<100:
        chker = Checker(sock_master,i)
        chker.start()
        i = i + 1
        print i
        chkerlist.append(chker)
    for chker in chkerlist:
        chker
        chker.join()
    print 'ending'
