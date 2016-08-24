# coding: gbk
# 定义元数据对象
from sqlalchemy import *
from sqlalchemy.orm import *
import os
MQ_BACKEND = 'database'
# 数据库定义
DB_ENGINE = create_engine( 'oracle://gapsdb_sys:gaps32@10.3.8.17:1522/ora10' , echo=False , encoding = 'gbk' , pool_recycle = 600 , 
                           pool_size = 100 , max_overflow = 10 , strategy='threadlocal' )
DB_CONSTR = dict( database = 'ora10' , user = 'gapsdb_sys' , password = 'gaps32' )
DB_TYPE = 'oracle'
GAPSETCDIR = r'H:\share\work\银联全渠道\天付宝通讯机\tfb_txj\etc'
TEMPLATE_DIR = r'H:\share\work\银联全渠道\天付宝通讯机\tfb_txj\templates'
GUOCAI_TEMPLATE = """POST /cgi-bin/v2.0/%(txid)s HTTP/1.1\r\nContent-Length: %(msg_len)d\r\nHost: apitest.tfb8.com\r\nReferer: http://apitest.tfb8.com/cgi-bin/v2.0/%(txid)s\r\nAccept-Encoding: UTF-8, deflate\r\nCache-Control: no-cache\r\nAccept-Language: zh-cn\r\nContent-Type: application/x-www-form-urlencoded\r\nConnection: Keep-Alive\r\nAccept: image/gif, */*\r\nUser-Agent: Mozilla/4.0 (compatible; MSIE 6.0; Windows NT 5.1; SV1; .NET CLR 2.0.50727)\r\n\r\n%(msg)s"""
LOGDIR = os.path.join(os.path.dirname(__file__), '../logs').replace('\\','/')
DEBUG = True # 是否在调试状态下
