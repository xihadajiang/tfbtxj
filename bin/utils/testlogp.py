#!/usr/bin/env python
#-*- coding:utf-8 -*-
__author__ = 'wyf'
#import logp
#import logging
LOGDIR = "../../logs"
import log
log.init_log( 'yl2' , LOGDIR , screen = True )
log.info( 'yl2' , '[%s]�����ӽ���������%s:%s��pid: %s'  )
#logp.UNI_OUTPUT = output = []
#logp.LOG_MAP = { logging.DEBUG : log.debug , 
#                 logging.INFO  : log.info , 
#                 logging.WARNING: log.warning , 
#                 logging.ERROR : log.error , 
#                 logging.CRITICAL : log.error }
#logp._write_log = logp._write_log_2
#logp.info( '��[%s]�����%s����[%s:%s]�ɹ�����'  , kind = 'SCHEDULE' )

import logging #����loggingģ��
import logging.config #����logģ�������ļ�
from logp import *
#_write_log( logging.WARNING , 'test root logger...' )

logging.config.fileConfig('logging.conf')#���������ļ�
logging.getLogger('root')#���������ļ�����־ʵ��
logging.debug('test root logger...')#�����־
info( '��[%s]�����%s����[%s:%s]�ɹ�����'  , kind = 'SCHEDULE' )
#root_logger.debug('test root logger...')#�����־
#
#logger = logging.getLogger('main')#����һ���µ���־ʵ��
#logger.info('test main logger')#�����Ϣ
#logger.info('start import module \'mod\'...')#�����Ϣ
#import mod
#
#logger.debug('let\'s test mod.testLogger()')#�����Ϣ
#mod.testLogger()#����modģ��ķ���
#
#root_logger.info('finish test...')
