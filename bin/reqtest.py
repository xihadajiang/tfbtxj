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
BUFLEN = 1024*10
TX_HOST = "127.0.0.1"
TX_PORT = 8028

class connector(threading.Thread):
    def __init__(self):
        threading.Thread.__init__(self)
        self.sock = socket.socket(socket.AF_INET, socket.SOCK_STREAM)
        #self.req = req
    def run(self,host,port,req):
        try:
            self.sock.connect((host,port))
            self.sock.send('%08d%s'%(len(req),req))
            print '>>>>>sent ','%08d%s'%(len(req),req)            
            rstr = self.sock.recv(BUFLEN)
            print 'received>>>>>>>',rstr
            self.sock.close()
            return rstr
        except socket.error,e:
            print e
            return e
body = """<?xml version="1.0" encoding="GB2312" ?><root><ver>1.0</ver><spid></spid><spbillno></spbillno><tfb_acp_listid></tfb_acp_listid><md5_sign></md5_sign><tid>api_acp_single_query</tid></root>"""
body = """<?xml version='1.0' encoding="GB2312"?><root><ver>1.0</ver><spid>11111</spid><spbillno>222222</spbillno><business_type>14900</business_type><business_no>444444</business_no><tran_amt>10000</tran_amt><cur_type></cur_type><true_name>11111</true_name><mobile></mobile><cre_id></cre_id><cre_type></cre_type><card_id>622384609891538799</card_id><card_type></card_type><bank_name>10000</bank_name><bank_ins_code>26520300</bank_ins_code><card_prov></card_prov><purpose></purpose><postscript></postscript><md5_sign></md5_sign><TransCode>api_acp_single.cgi</TransCode></root>"""
body = """<?xml version='1.0' encoding="GB2312" ?><root><ver>1.0</ver><spid>1800631877</spid><spbillno>222223</spbillno><business_type>14900</business_type><business_no>444444</business_no><tran_amt>10000</tran_amt><cur_type>1</cur_type><true_name>11111</true_name><mobile>13800000000</mobile><cre_id>371324198806065718</cre_id><cre_type>1</cre_type><card_id>622908115000352211</card_id><card_type>0</card_type><bank_name>兴业银行</bank_name><bank_ins_code>03090000</bank_ins_code><card_prov>上海</card_prov><purpose>通讯费</purpose><postscript></postscript><md5_sign></md5_sign><TransCode>api_acp_single.cgi</TransCode></root>"""

cn_tx = connector()
resp = cn_tx.run(TX_HOST,TX_PORT,'%s'%body)
resp = resp
#head,body = resp.split('\r\n\r\n')
print resp
