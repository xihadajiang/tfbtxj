# coding: gbk
# 定义元数据对象
from sqlalchemy import *
from sqlalchemy.orm import *
MQ_BACKEND = 'database'
# 数据库定义
#20120513注释掉
#DB_ENGINE = create_engine( 'postgres://oa:oa@localhost:5432/uni_manage' , echo=False , encoding = 'gbk' , pool_recycle = 600 , 
#                           pool_size = 100 , max_overflow = 10 , strategy='threadlocal' )
#DB_ENGINE = create_engine( 'postgres://oa:oa@127.0.0.1:5432/uni_manage' , echo=False , encoding = 'gbk' , pool_recycle = 600 , 
#                           pool_size = 100 , max_overflow = 10 , strategy='threadlocal' )
#DB_CONSTR = dict( database = 'uni_manage' , user = 'oa' , password = 'oa' )
#DB_ENGINE = create_engine( 'postgres://oa:oa@127.0.0.1:5432/oa_core' , echo=False , encoding = 'gbk' , pool_recycle = 600 , 
#                           pool_size = 100 , max_overflow = 10 , strategy='threadlocal' )
#DB_CONSTR = dict( database = 'oa_core' , user = 'oa' , password = 'oa' )
#DB_ENGINE = create_engine( 'postgres://oa:oa@127.0.0.1:5432/oa_jn_20120201' , echo=False , encoding = 'gbk' , pool_recycle = 600 , 
#                           pool_size = 100 , max_overflow = 10 , strategy='threadlocal' )
#DB_CONSTR = dict( database = 'oa_jn_20120201' , user = 'oa' , password = 'oa' )
#DB_ENGINE = create_engine( 'postgres://oa:oa@115.28.39.93:5432/oa' , echo=False , encoding = 'gbk' , pool_recycle = 600 , 
#                           pool_size = 100 , max_overflow = 10 , strategy='threadlocal' )
#DB_CONSTR = dict( database = 'oa' , user = 'oa' , password = 'oa' )
#DB_TYPE = 'postgresql'
DB_ENGINE = create_engine( 'oracle://gapsdb_sys:gaps32@10.3.8.17:1522/ora10' , echo=False , encoding = 'gbk' , pool_recycle = 600 , 
                           pool_size = 100 , max_overflow = 10 , strategy='threadlocal' )
DB_CONSTR = dict( database = 'ora10' , user = 'gapsdb_sys' , password = 'gaps32' )
#DB_TYPE = 'oracle'
# orcale
#DB_ENGINE = create_engine( 'oracle://gapsdb:gapsdb@138.138.2.130:1521/yypt' , echo=False , encoding = 'gbk' , pool_recycle = 600 , 
#                           pool_size = 100 , max_overflow = 10 , strategy='threadlocal' )
#DB_CONSTR = dict( database = 'yypt' , user = 'gapsdb' , password = 'gapsdb' )
#DB_TYPE = 'oracle'
# orcale
#DB_ENGINE = create_engine( 'oracle://gbismdb:gbism@127.0.0.1:1521/orcl' , echo=False , encoding = 'gbk' , pool_recycle = 600 , pool_size = 100 , max_overflow = 10 , strategy='threadlocal' )
#DB_CONSTR = dict( database = 'orcl' , user = 'gbismdb' , password = 'gbism' )
#DB_ENGINE = create_engine( 'oracle://oa:oa@127.0.0.1:1521/orcl' , echo=False , encoding = 'gbk' , pool_recycle = 600 , pool_size = 100 , max_overflow = 10 , strategy='threadlocal' )
#DB_CONSTR = dict( database = 'orcl' , user = 'oa' , password = 'oa' )
DB_TYPE = 'oracle'
#se = settings.DB_SESSION()
#yhdy = se.query( GL_HYDY ).get( '000287' )
#print yhdy.hydm,yhdy.xm

                           
DEBUG = True # 是否在调试状态下
