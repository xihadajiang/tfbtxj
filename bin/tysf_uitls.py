#coding:gbk
import sys,os,re
import hashlib 

def lnieno():
    frame = None
    try:
        raise ZeroDivisionError
    except ZeroDivisionError:
        frame = sys.exc_info()[2].tb_frame.f_back
    return frame.f_lineno

def funcname():
    frame = None
    try:
        raise ZeroDivisionError
    except ZeroDivisionError:
        frame = sys.exc_info()[2].tb_frame.f_back
    return frame.f_code.co_name

def cofilename():
    frame = None
    try:
        raise ZeroDivisionError
    except ZeroDivisionError:
        frame = sys.exc_info()[2].tb_frame.f_back
    return frame.f_code.co_filename.split(os.sep)[-1]

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
    
from Crypto import Random 
from Crypto.Cipher import PKCS1_v1_5 
from Crypto.Hash import SHA
from Crypto.Cipher import AES
from Crypto.PublicKey import RSA 
from Crypto.Signature import PKCS1_v1_5 as pk 
from Crypto.PublicKey import RSA 
import base64

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

def getcipher(signdata,pubkey):
    publickey = RSA.importKey(open(pubkey,'r').read()) 
    result = ''
    tmp_len = 0
    while tmp_len < len(signdata):
        signdata_tmp = signdata[tmp_len:tmp_len + 117].encode('utf-8') if type(signdata) == unicode else signdata[tmp_len:tmp_len + 117]
        result = result + rsa_base64_encrypt(signdata_tmp,publickey)
        tmp_len = tmp_len + 117
    return result

def uncipher(rdata,privkey):
    privatekey=RSA.importKey(open(privkey,'r').read()) 
    data = rdata
    result = ''
    tmp_len = 0
    data = base64.b64decode(data)
    while tmp_len < len(data):
        print tmp_len,len(data)
        result = result + rsa_base64_decrypt(data[tmp_len:tmp_len + 128],privatekey)
        tmp_len = tmp_len + 128
    return result
