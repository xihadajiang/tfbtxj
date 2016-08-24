# -*- coding: gbk -*-
import logging , sys , traceback2
import loghandler
import os
LOGLEVEL= logging.DEBUG

def init_log( name = None , LOGDIR = '',screen = False ):
    return init_logger( name , LOGDIR , screen )

def init_logger( logname , logdir , screen = True ):
    logobj = logging.getLogger( logname )
    # 判断是否需要清理
    if logobj.handlers:
        return  logobj  # 日志已创建，跳过
        # 有处理句柄，则该日志对象需要清理
        #logobj.info( '日志[%s]重新初始化' , logname )
        #for hdl in logobj.handlers[:]:
        #    logobj.removeHandler( hdl )
    
    # 初始化日志文件处理句柄
    fn = '%s' % logname
    hdlr = loghandler.DateFileHandler( os.path.join( logdir , fn ) )
    formatter = logging.Formatter('%(asctime)s T%(thread)d %(levelname)s %(message)s')
#    hdlr = logging.handlers.TimedRotatingFileHandler(logname, "H", 24, 0)
#    hdlr.suffix = "%Y%m%d%H.log"  # 设置后缀
    hdlr.setFormatter(formatter)
    logobj.addHandler( hdlr )
    
    if screen:
        # 初始化屏幕打印处理句柄
        hdlr = logging.StreamHandler()
        formatter = logging.Formatter('%(asctime)s %(name)s：T%(thread)d %(levelname)s %(message)s')
        hdlr.setFormatter(formatter)
        logobj.addHandler( hdlr )

    logobj.setLevel( LOGLEVEL )
    return logobj

def debug( logname , *args , **kwargs ):
    if logname:
        logger = init_log( logname )
        logger.debug( *args , **kwargs )

def info( logname , *args , **kwargs ):
    if logname:
        logger = init_log( logname )
        logger.info( *args , **kwargs )
        
def warning( logname , *args , **kwargs ):
    if logname:
        logger = init_log( logname )
        logger.warning( *args , **kwargs )
        
def error( logname , *args , **kwargs ):
    if logname:
        logger = init_log( logname )
        logger.error( *args , **kwargs )
        
def critical( logname , *args , **kwargs ):
    if logname:
        logger = init_log( logname )
        logger.critical( *args , **kwargs )

def exception( logname , msg , *args ):
    if logname:
        logger = init_log( logname )
        msg = traceback2.format_exc( show_locals = True )
        logger.error( msg )
        return msg
        
def lineno():
    frame = None
    try:
        raise ZeroDivisionError
    except ZeroDivisionError:
        frame = sys.exc_info()[2].tb_frame.f_back
    return frame.f_lineno
