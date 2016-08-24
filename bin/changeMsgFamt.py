#!/usr/bin/env jython
# coding: utf-8
import socket, re, sys, threading
import sys
import logging,logging.handlers
import datetime
import cStringIO
import base64
import socket, threading  
import re
from xml2json import *
import hashlib   
REQ_TEMPLATE = """POST /cgi-bin/v2.0/%s HTTP/1.1\r\nContent-Length: %d\r\nHost: apitest.tfb8.com\r\nReferer: http://apitest.tfb8.com/cgi-bin/v2.0/%s\r\nAccept-Encoding: UTF-8, deflate\r\nCache-Control: no-cache\r\nAccept-Language: zh-cn\r\nContent-Type: application/x-www-form-urlencoded\r\nConnection: Keep-Alive\r\nAccept: image/gif, */*\r\nUser-Agent: Mozilla/4.0 (compatible; MSIE 6.0; Windows NT 5.1; SV1; .NET CLR 2.0.50727)\r\n\r\n%s"""
RESP_TEMPLATE = """%08d%s"""

req = """88888<?xml version='1.0' encoding="GB2312" ?><root><ver>1.0</ver><spid>1800631877</spid><spbillno>222223</spbillno><business_type>14900</business_type><business_no>444444</business_no><tran_amt>10000</tran_amt><cur_type>1</cur_type><true_name>11111</true_name><mobile>13800000000</mobile><cre_id>371324198806065718</cre_id><cre_type>1</cre_type><card_id>622908115000352211</card_id><card_type>0</card_type><bank_name>兴业银行</bank_name><bank_ins_code>03090000</bank_ins_code><card_prov>上海</card_prov><purpose>通讯费</purpose><postscript></postscript><md5_sign></md5_sign><TransCode>api_acp_single.cgi</TransCode></root>"""
TX_HOST = """apitest.tfb8.com"""
TX_PORT = 80
BUFLEN = 1024*10
KEY = '2d3c22048b300db8b347b7024b378053'
shh = '1800631877'
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

def MD5(data):
    m2 = hashlib.md5()   
    m2.update(data)   
    print m2.hexdigest()
    return m2.hexdigest()
def getxml(data):
    body = re.findall('<.*>',data,re.S)[0]
    return body

def changeCode(xml,coding):
    coding_before  = re.findall('encoding="(.*?)"',xml,re.S)[0]
    body = xml.decode(coding_before).encode(coding).replace('encoding="%s"'%coding_before,'encoding="%s"'%coding)
    return body

def sort(mes): 
    """ 
    作用类似与java的treemap, 
    取出key值,按照字母排序后将value拼接起来 
    返回字符串 
    """ 
    _par = [] 
    keys=mes.keys() 
    keys.sort() 
    for v in keys: 
        if mes[v].strip() != '' and v.strip() not in('TransCode','retcode','retmsg'):
            _par.append('%s=%s'%(v,mes[v])) 
    sep='&' 
    message=sep.join(_par) 
    return message 
        
def sign(req):
    stringSign = sort(req.get('root','')).encode('UTF-8')
    return MD5(stringSign+'&key=%s'%KEY)

def getsort(req):
    return sort(req.get('root','')).encode('UTF-8')

def checksign(req):
    stringSign = sort(req.get('root',''))
    return MD5(stringSign.encode('gbk'))

    
def remote2local(data):
    print data
    xml = getxml(data)
    xml = changeCode(xml,'UTF-8')
    resp_dict = Xml2Json(xml).result;
    checksign(resp_dict)
    return RESP_TEMPLATE%(len(xml),xml)
#def remote2local(data,logging):
def local2remote(data):
    print data
    TransCode_tag = re.findall('<TransCode>.*?</TransCode>',data,re.S)[0]
    TransCode = re.findall('<TransCode>(.*?)</TransCode>',data,re.S)[0]
    md5_sign_tag = re.findall('<md5_sign>.*?</md5_sign>',data,re.S)[0]
    xml = getxml(data)
    xml = changeCode(xml,'UTF-8')
    req_dict = Xml2Json(xml).result;
    print req_dict
    md5_sign = sign(req_dict)
    body = xml.replace(TransCode_tag,'').replace(md5_sign_tag,'<md5_sign>%s</md5_sign>'%md5_sign)
    return REQ_TEMPLATE%(TransCode,len(body),TransCode,body)

def gaps2tfb(data):
    print data
    TransCode_tag = re.findall('<TransCode>.*?</TransCode>',data,re.S)[0]
    TransCode = re.findall('<TransCode>(.*?)</TransCode>',data,re.S)[0]
    md5_sign_tag = re.findall('<md5_sign>.*?</md5_sign>',data,re.S)[0]
    xml = getxml(data)
    xml = changeCode(xml,'UTF-8')
    req_dict = Xml2Json(xml).result;
    print req_dict
    md5_sign = sign(req_dict)
    cipher_data = getsort(req_dict)+"&md5_sign=%s"%md5_sign
    print cipher_data
    cipher_data = getcipher(cipher_data)
    return {"""cipher_data""":cipher_data}
#tfb_body = local2remote(req)
#cn_tx = connector()
#resp = cn_tx.run(TX_HOST,TX_PORT,'%s'%tfb_body)
#print remote2local(resp)
s = 'cur_type=1&result=3&spbillno=1468481136372&spid=1800938830&tfb_acp_listid=2016071400161976&tran_amt=1&key=12345'
MD5(s)
print "395513d0348abeea96e1c0db03f955ad"
s2 = "bank_ins_code=01050000&bank_name=建设银行&business_no=10086&business_type=10101&card_id=6227003325370110828&card_prov=广东&card_type=0&cre_id=511702198002221308&cre_type=1&cur_type=1&mobile=18800000000&postscript=这是单条代扣API测试&purpose=保险代扣&spbillno=1468481136371&spid=1800938830&tran_amt=1&true_name=奚兰若&ver=1.0&key=12345"
MD5(s2.decode('GBK').encode('UTF-8'))
print "781169d01489166c873b152d2b8204a7"
from Crypto import Random 
from Crypto.Cipher import PKCS1_v1_5 
from Crypto.Hash import SHA
from Crypto.Cipher import AES
from rsa import key, common, encrypt 
from Crypto.PublicKey import RSA 
from Crypto.Signature import PKCS1_v1_5 as pk 
from Crypto.PublicKey import RSA 
#publickey = RSA.importKey(open(r'H:\share\work\财付通\通讯机\证书\cert.pem','r').read()) 
#publickey = RSA.importKey(open(r'H:\share\work\银联全渠道\天付宝通讯机\rsa_public_key.pem','r').read()) 
publickey = RSA.importKey(open(r'H:\share\work\银联全渠道\天付宝通讯机\tfb_txj\lib\gczf_rsa_public.pem','r').read()) 
#privatekey=RSA.importKey(open(r'H:\share\work\财付通\通讯机\证书\key.pem','r').read()) 
privatekey=RSA.importKey(open(r'H:\share\work\银联全渠道\天付宝通讯机\tfb_txj\lib\1800208886_private_rsa.pem','r').read()) 
""" 
rsa加密 
""" 
def rsa_base64_encrypt(data,key): 
    """ 
    1. rsa encrypt 
    2. base64 encrypt 
    """ 
    cipher = PKCS1_v1_5.new(key) 
    return base64.b64encode(cipher.encrypt(data)) 
  
""" 
rsa解密 
""" 
def rsa_base64_decrypt(data,key): 
    """ 
    1. base64 decrypt 
    2. rsa decrypt 
    示例代码 
      
   key = RSA.importKey(open('privkey.der').read()) 
    >>> 
    >>> dsize = SHA.digest_size 
    >>> sentinel = Random.new().read(15+dsize) # Let's assume that average data length is 15 
    >>> 
    >>> cipher = PKCS1_v1_5.new(key) 
    >>> message = cipher.decrypt(ciphertext, sentinel) 
    >>> 
    >>> digest = SHA.new(message[:-dsize]).digest() 
    >>> if digest==message[-dsize:]: # Note how we DO NOT look for the sentinel 
    >>> print "Encryption was correct." 
    >>> else: 
    >>> print "Encryption was not correct." 
    """ 
    cipher = PKCS1_v1_5.new(key) 
    return cipher.decrypt(data, Random.new().read(15+SHA.digest_size)) 
def getcipher(signdata):
    result = ''
    tmp_len = 0
    while tmp_len < len(signdata):
        signdata_tmp = signdata[tmp_len:tmp_len + 117].encode('utf-8') if type(signdata) == unicode else signdata[tmp_len:tmp_len + 117]
        result = result + rsa_base64_encrypt(signdata_tmp,publickey)
        tmp_len = tmp_len + 117
    return result
def uncipher(rdata):
    data = rdata
    result = ''
    tmp_len = 0
    data = base64.b64decode(data)
    while tmp_len < len(data):
        print tmp_len,len(data)
        result = result + rsa_base64_decrypt(data[tmp_len:tmp_len + 128],privatekey)
        tmp_len = tmp_len + 128
    return result
""" 
RSA签名 
""" 
def sign_RSA(signdata): 
    """ 
    @param signdata: 需要签名的字符串 
    """ 
    #print 'sign',signdata
    h=SHA.new(signdata) 
    signer = pk.new(privatekey) 
    signn=signer.sign(h) 
    print len(signn)
    signn=base64.b64encode(signn) 
    return signn 
     
""" 
RSA验签 
结果：如果验签通过，则返回The signature is authentic 
     如果验签不通过，则返回"The signature is not authentic." 
""" 
def checksign_RSA(rdata): 
    print 'checksign',rdata
    signn=base64.b64decode(rdata) 
    signdata= sort(rdata) 
    verifier = pk.new(publickey) 
    if verifier.verify(SHA.new(signdata), signn): 
        print "The signature is authentic." 
    else: 
        print "The signature is not authentic." 
def testrsa():
    key2 = rsa.PrivateKey.load_pkcs1(key_file.read())
    msg8 = msg.encode('utf-8')
    msg_dis = md5(msg8).digest()
    rsa.encrypt(msg_dis,key2)

body = """<?xml version="1.0" encoding="UTF-8" ?>
<root>
<cipher_data>
iPd3xfXM1wB2W9kM0K4WZRBQ+IBiKE5/WzW3lPz9Ketz9YMTAv2KmZ2UYFrTqPuWHtZ7ar1aNPeKRHrkqyS8vX4vbvw6pPXKN/R6keu72ZyPwMDkKbr+cnYc+kK9zabN7KAWM0tLjADuTHQv3fZOcf9VGap1uGaYiSKVpp/b2tVhwzW01IHIML1hyi+Exao4/4beBszBlEsmA5LoLgOcx7tuWBBYWplZN/3UbuJ9yUUxFrw4zgD7wYuRszYmbSVRqbrMTvmT9UrfMEK4GOi3Qk8BIX95m1W0hsuHu2xbBdTjmRm30p9NlWxteOlkOYS/BLpr/kLH4NVGwxLsU+d3sA==
</cipher_data>
</root>"""
body = gaps2tfb(req)
from urllib import urlencode
body = urlencode(body)
#body = """cipher_data= C6+Qn3hPSQtmc38N2dgKOUB2fa6GII6K+5ch3GZLB4xed9vrtZVAit1kQlLjvnQYBaOZj+RosN3Ty7x5+FKbO0J+QPRCn+RfqMSl4B365P4tgCLiGDyuLjQCnseNq1ym2GNiiFmil1WvUCRRtqCnTV+/6hevtutyGR4sKdGqwAxXAGZ183tOkYpCS8fNs+kXSEUJNTDxUNzO+4b1YzWjFPjLL8bPD3fgQw9XB47U7QKm2ef6L0Df6aAUSSXbTg6LV8/ZM+mszVAfArB/ZeBnab+JU0RqODohV8ZYxkCvayGXGUYUpnn6xyrGuPusK7+IyykcUfttuLveW45Am2COxlnVb1Cl0s5ozWgYV3womDrQZTKJ5Z43+2W9FUHn+pxnupIOV+ngq5RX+6uDv12eKvm9lK51swcZWXv/nluvwirW+0aU2gH9N06ja3r2KFyw0DdxnGY49QSd7RFd89qSX8DNdsxJiOiWkyDDX7ZVTAi181YwxZItBHgoXzOsHB5Gad8ugSFowBq69taJR0kqmkiuwXkPJrCEjNWSSgzuOtPxUpc1k+jVQgC/ZHYB5FUcXcNZ1b+7UZ02L7BAgowhQ6TXplFkE2sjJXY6DkGrRQa3h1vim0f2NC/mFmv9vuQGvsJ5b/DwNSQbC4qRwgyk+aR6HVue7ajd3Tbfbp3reqA="""
tfb_body = REQ_TEMPLATE%("api_acp_single.cgi",len(body),"api_acp_single.cgi",body)
print tfb_body
cn_tx = connector()
resp = cn_tx.run(TX_HOST,TX_PORT,'%s'%tfb_body)
print resp.decode('utf-8')
resp_c = """wWLd/tXP8F6fYKTDCyR/q/Z6N9ZjVa7aAK+Jm/vincxc/oTnNnViGV8ewEWzXLNEgEL5n7BvCsGP7WJb7b1URPMhMqej6KMqRAYShxQLYJaXFYc2orCjelPKg0pVw/8TRQCSGVYQi3LhgZX2VfJwCGv0zRgi37W1uvyQWI9CCYGWdS3u5sCSgGNjh+NIeds1ITcLAaG3XpbuMeRkoPPTbbzI4HvEzwTrmbjTaD4p4MgbPzsCA7ulnZ06xLcVcrFwV8awJ3DmjY2fqk6mdJxMIp+1BqEoQc8o/CWZompYL+auYJRazF2bL0XVzxJtgK+yYJDN0EyNh91xj/BeqloCKQ=="""
print '-----',uncipher(resp_c)

signdata = "cur_type=1&result=3&spbillno=1468481136372&spid=1800938830&tfb_acp_listid=2016071400161976&tran_amt=1&md5_sign=395513d0348abeea96e1c0db03f955ad"
print len(signdata)
output = getcipher(signdata)
print output
print uncipher(output)
#print len(output),output
real = "iPd3xfXM1wB2W9kM0K4WZRBQ+IBiKE5/WzW3lPz9Ketz9YMTAv2KmZ2UYFrTqPuWHtZ7ar1aNPeKRHrkqyS8vX4vbvw6pPXKN/R6keu72ZyPwMDkKbr+cnYc+kK9zabN7KAWM0tLjADuTHQv3fZOcf9VGap1uGaYiSKVpp/b2tVhwzW01IHIML1hyi+Exao4/4beBszBlEsmA5LoLgOcx7tuWBBYWplZN/3UbuJ9yUUxFrw4zgD7wYuRszYmbSVRqbrMTvmT9UrfMEK4GOi3Qk8BIX95m1W0hsuHu2xbBdTjmRm30p9NlWxteOlkOYS/BLpr/kLH4NVGwxLsU+d3sA=="
print len(real),real