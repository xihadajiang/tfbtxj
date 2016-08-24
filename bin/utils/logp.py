# coding: gbk

# 本模块用于封装日志进程代理对象, 并提供日志操作函数

# 日志函数操作如下:
#   debug( msg , args , lsh =  , kind = , block = , bin = True )
# 函数自动根据是否有lsh决定调用交易日志, 没有调用系统日志(若kind不存在,则默认用DEFAULT), 
#                   另外,当lsh有值时, kwargs中提供交易日期
#             是否有block决定调用块日志( bin是否为True决定将block内容转换为hex )
# 对于exception,系统有特殊处理,会将exception的内容输出到msg的后面(另起一行), 该行为隐含,不需要调用者操作
# 
# 针对写日志造成的排队情况，使用队列和线程控制

import logging
import datetime
import threading
import Queue

LOG_QUE = Queue.Queue()
THREAD_RUN = False
BG_LOCK = threading.Lock()

def bg_log_writer():
    while True:
        try:
            lvl , args , kwargs = LOG_QUE.get()
            print '--',lvl , args , kwargs
            _write_log( lvl , *args , **kwargs )
        except:
            pass
            
def thread_start():
    global THREAD_RUN
    with BG_LOCK:
        if not THREAD_RUN :
            t = threading.Thread( target = bg_log_writer )
            t.setDaemon( True )
            t.start()
            THREAD_RUN = True
# 系统启动时，即启动后台日志线程
thread_start()

def debug( *args , **kwargs ):
    LOG_QUE.put( ( logging.DEBUG , args , kwargs ) )
def info( *args , **kwargs ):
    print args,kwargs
    LOG_QUE.put( ( logging.INFO , args , kwargs ) )
def warning( *args , **kwargs ):
    LOG_QUE.put( ( logging.WARNING , args , kwargs ) )
def error( *args , **kwargs ):
    LOG_QUE.put( ( logging.ERROR , args , kwargs ) )
def critical( *args , **kwargs ):
    LOG_QUE.put( ( logging.CRITICAL , args , kwargs ) )
def exception( *args , **kwargs ):
    from shangjie.utils import traceback2
    exc_msg = traceback2.format_exc( show_locals = True )
    args = list( args )
    if args:
        args[0] += '\n%s'
    else:
        args.append( '%s' )
    args.append( exc_msg )
    LOG_QUE.put( ( logging.ERROR , args , kwargs ) )

# 2010-4-20 11:26 张骏
# 核心日志函数
def _write_log( level , *args , **kwargs ):
    init_log()
    if len( args ) > 1:
        msg = args[0] % args[1:]
    elif len( args ) == 1:
        msg = args[0]
    else:
        msg = ''
    
    # 处理block
    block = kwargs.get( 'block' )
    if type(block) is str:
        # 是块日志
        bin = kwargs.get( 'bin' , True )
        if bin:
            block = to_hex( block )
    
    lsh = kwargs.get( 'lsh' )
    sj  = datetime.datetime.now().strftime( '%Y%m%d %H:%M:%S.%f' )
    
    output_log( lsh , level , msg , sj , block , kwargs )

# 针对单元测试，增加单元测试用_write_log版本
UNI_OUTPUT = None
LOG_MAP    = None
def _write_log_2( level , *args , **kwargs ):
    if len( args ) > 1:
        msg = args[0] % args[1:]
    elif len( args ) == 1:
        msg = args[0]
    else:
        msg = ''
    
    # 处理block
    block = kwargs.get( 'block' )
    if type(block) is str:
        # 是块日志
        bin = kwargs.get( 'bin' , True )
        if bin:
            block = to_hex( block )
    
    if block:
        block = '\n'+'='*40+'\n'+block+ ('\n' if block[-1] != '\n' else '' ) +'='*40 + '\n'
    elif msg[-1] == '\n':
        block = ''
    else:
        block = '\n'
    UNI_OUTPUT.append( ( LOG_MAP[ level ] , msg + block ) )

def switch( u , m ):
    global UNI_OUTPUT , LOG_MAP
    UNI_OUTPUT = u
    LOG_MAP = m
    _write_log = _write_log_2
    
