#!/usr/bin/env python
#-*- coding:utf-8 -*-
__author__ = 'wyf'
#import logp
#import logging
LOGDIR = "../../logs"
import log
log.init_log( 'yl2' , LOGDIR , screen = True )
log.info( 'yl2' , '[%s]发送子进程启动，%s:%s，pid: %s'  )
#logp.UNI_OUTPUT = output = []
#logp.LOG_MAP = { logging.DEBUG : log.debug , 
#                 logging.INFO  : log.info , 
#                 logging.WARNING: log.warning , 
#                 logging.ERROR : log.error , 
#                 logging.CRITICAL : log.error }
#logp._write_log = logp._write_log_2
#logp.info( '在[%s]发起的%s交易[%s:%s]成功返回'  , kind = 'SCHEDULE' )

import logging #导入logging模块
import logging.config #导入log模块配置文件
from logp import *
#_write_log( logging.WARNING , 'test root logger...' )

logging.config.fileConfig('logging.conf')#加载配置文件
logging.getLogger('root')#引入配置文件的日志实例
logging.debug('test root logger...')#输出日志
info( '在[%s]发起的%s交易[%s:%s]成功返回'  , kind = 'SCHEDULE' )
#root_logger.debug('test root logger...')#输出日志
#
#logger = logging.getLogger('main')#定义一个新的日志实例
#logger.info('test main logger')#输出信息
#logger.info('start import module \'mod\'...')#输出信息
#import mod
#
#logger.debug('let\'s test mod.testLogger()')#输出信息
#mod.testLogger()#调用mod模块的方法
#
#root_logger.info('finish test...')
