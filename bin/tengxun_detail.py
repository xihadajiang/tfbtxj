#!/usr/bin/env python
#coding: utf-8
import socket, re, sys, threading
from optparse import OptionParser
import sys
import logging,logging.handlers
import datetime
import cStringIO
import base64
import socket, threading  
import re
import binascii
import hashlib
from const import *
def getwjzy(filename):
    fp = open(filename,'rb');
    fdata = fp.read();
    fp.close();
    sha1 = hashlib.sha1();
    sha1.update(fdata);
    s = binascii.a2b_hex(sha1.hexdigest())
    return base64.b64encode(s)

BUFLEN = 1024*10
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

class connector(threading.Thread):
    def __init__(self):
        threading.Thread.__init__(self)
        self.sock = socket.socket(socket.AF_INET, socket.SOCK_STREAM)
        #self.req = req
    def run(self,host,port,req):
        try:
            self.sock.connect((host,port))
            self.sock.send(req)
            print '>>>>>sent ',req            
            rstr = self.sock.recv(BUFLEN)
            print 'received>>>>>>>',rstr
            self.sock.close()
            return rstr
        except socket.error,e:
            print e
            return e

def sendfile(data):
    date = data
    filename = '/home/gaps32/file/xpay/9990000307/TCCF_%s_1'%data
    print filename
    #body = '/home/gaps32/file/xpay/9990000307/TCCF_%s_1.zip#/home/gaps32/file/xpay/9990000307/TCCF_%s_1'%(date,date)
    date = re.findall('TCCF_(.*?)_1',filename,re.S)[0]
    print date
    body = '%s.zip#%s'%(filename,filename)
    print body,date
    cn = connector()
    result = cn.run(SERVER,PORT,'ZIP\r\n%s'%body)
    print result
    cn = connector()
    degist = cn.run(SERVER,PORT,'WJZY\r\n%s.zip'%filename)
    print degist
    degist = getwjzy(filename)
    if result == 'success':
        f = open('%s.zip'%filename,'rb')
        s = f.read()
        f.close()
        file_body = """--V7u0v4R-qXziigN4XM7FmiyjBzbbHMwWVn\r\nContent-Disposition: form-data; name="TCCF_%s_1.zip"; filename="TCCF_%s_1.zip"\r\nContent-Type: multipart/x-zip\r\nContent-Transfer-Encoding: binary\r\n\r\n%s\r\n--V7u0v4R-qXziigN4XM7FmiyjBzbbHMwWVn--\r\n"""%(date,date,s)
        url = "/upload/HFB_FP_D/%s/TCCF_%s_1.zip"%(date,date)
        cn = connector()
        sign = cn.run(SERVER,PORT,'URL\r\n%s'%base64.b64encode(url))
        print sign
        tx_body = """POST /fastpay%s?certId=BKT0982010062739&sign=%s HTTP/1.1\r\nMULE_REMOTE_CLIENT_ADDRESS: /127.0.0.1:12929\r\nHost: 192.168.96.109:11014\r\nUser-Agent: AHC/1.0\r\nConnection: keep-alive\r\nAccept: */*\r\nContent-Type: multipart/form-data; boundary=V7u0v4R-qXziigN4XM7FmiyjBzbbHMwWVn\r\nContent-Length: %d\r\n\r\n%s\r\n"""%(url,sign,len(file_body),file_body)
        #print tx_body
        cn_tx = connector()
        res = cn_tx.run(TX_HOST,TX_PORT,'%s'%tx_body)
        print res
    resp = """<?xml version="1.0" encoding="utf-8"?><Cartoon><message_id>Success_Hundsun</message_id><comm_id>Success</comm_id><comm_trans>Success</comm_trans><version>1.0.1</version><wjzy>%s</wjzy><respcode>00000</respcode><respmsg>文件上传成功</respmsg></Cartoon>"""%degist
#    return resp
#def sendbw(data):
    today = datetime.datetime.today()
    lsh = today.strftime('%Y%m%d%H%M%S')
    date = today.strftime('%Y%m%d %H:%M:%S')
    filename = '/home/gaps32/file/xpay/9990000307/TCCF_%s_1'%data
    rq = data
    print filename
    cn = connector()
    degist = cn.run(SERVER,PORT,'WJZY\r\n%s.zip'%filename)
    print degist
    degist = getwjzy(filename)
    
    body = """<Tenpay><Message id="%s"><CCNotify id="CCNotify"><version>1.5.0</version><instId>HFB_FP_D</instId><certId>BKT0982010062739</certId><date>%s</date><fileName>TCCF_%s_1.zip</fileName><clearingDate>%s</clearingDate><digest>%s</digest><Extension></Extension></CCNotify></Message></Tenpay>"""%(lsh,date,rq,rq,degist)
    cn = connector()
    result = cn.run(SERVER,PORT,'GAPS\r\n%s'%base64.b64encode(body.decode('gbk').encode('utf-8')))
    print result
    body = base64.b64decode(result.encode('utf-8'))
    tx_body = """POST /fastpay/receiver HTTP/1.1\r\nContent-Type: application/xml; charset=utf-8\r\nUser-Agent: Jakarta Commons-HttpClient/3.1\r\nHost: 192.168.96.109:11014\r\nContent-Length: %d\r\nAccept-Encoding: gzip,deflate\r\nConnection: close\r\n\r\n%s"""%(len(body),body)
    print tx_body
    cn_tx = connector()
    resp = cn_tx.run(TX_HOST,TX_PORT,'%s'%tx_body)
    resp = resp.decode('utf-8').encode('gbk')
    head,body = resp.split('\r\n\r\n')
    print body
    cn = connector()
    result = cn.run(SERVER,PORT,'HTTP\r\n%s'%base64.b64encode(body.decode('gbk').encode('utf-8')))
    print base64.b64decode(result.encode('utf-8'))
if __name__ == '__main__':
    import sys
    dzrq = sys.argv[-1]
    print dzrq
    sendfile(dzrq)
#    sendbw(dzrq)
