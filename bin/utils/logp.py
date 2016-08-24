# coding: gbk

# ��ģ�����ڷ�װ��־���̴������, ���ṩ��־��������

# ��־������������:
#   debug( msg , args , lsh =  , kind = , block = , bin = True )
# �����Զ������Ƿ���lsh�������ý�����־, û�е���ϵͳ��־(��kind������,��Ĭ����DEFAULT), 
#                   ����,��lsh��ֵʱ, kwargs���ṩ��������
#             �Ƿ���block�������ÿ���־( bin�Ƿ�ΪTrue������block����ת��Ϊhex )
# ����exception,ϵͳ�����⴦��,�Ὣexception�����������msg�ĺ���(����һ��), ����Ϊ����,����Ҫ�����߲���
# 
# ���д��־��ɵ��Ŷ������ʹ�ö��к��߳̿���

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
# ϵͳ����ʱ����������̨��־�߳�
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

# 2010-4-20 11:26 �ſ�
# ������־����
def _write_log( level , *args , **kwargs ):
    init_log()
    if len( args ) > 1:
        msg = args[0] % args[1:]
    elif len( args ) == 1:
        msg = args[0]
    else:
        msg = ''
    
    # ����block
    block = kwargs.get( 'block' )
    if type(block) is str:
        # �ǿ���־
        bin = kwargs.get( 'bin' , True )
        if bin:
            block = to_hex( block )
    
    lsh = kwargs.get( 'lsh' )
    sj  = datetime.datetime.now().strftime( '%Y%m%d %H:%M:%S.%f' )
    
    output_log( lsh , level , msg , sj , block , kwargs )

# ��Ե�Ԫ���ԣ����ӵ�Ԫ������_write_log�汾
UNI_OUTPUT = None
LOG_MAP    = None
def _write_log_2( level , *args , **kwargs ):
    if len( args ) > 1:
        msg = args[0] % args[1:]
    elif len( args ) == 1:
        msg = args[0]
    else:
        msg = ''
    
    # ����block
    block = kwargs.get( 'block' )
    if type(block) is str:
        # �ǿ���־
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
    
