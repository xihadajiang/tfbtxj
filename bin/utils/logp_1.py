# coding: gbk
try:
    import _tps
except:
    import fake_tps as _tps
import traceback2
from ftools import register , AttrDict

def _write_log( level , *args , **kwargs ):
    if len( args ) > 1:
        msg = args[0] % args[1:]
    elif len( args ) == 1:
        msg = args[0]
    else:
        msg = ''
    
    # 处理block
    block = kwargs.get( 'block' , None )
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
    
    output = msg + block
    
    _tps.errLog( level , output , _tps.RPT_TO_LOG )

@register()
def log_debug( *args , **kwargs ):
    _write_log( _tps.DEBUG , *args , **kwargs )

@register()
def log_info( *args , **kwargs ):
    _write_log( _tps.INFO , *args , **kwargs )

@register()
def log_warning( *args , **kwargs ):
    _write_log( _tps.WARNING , *args , **kwargs )

@register()
def log_error( *args , **kwargs ):
    _write_log( _tps.ERROR , *args , **kwargs )

@register()
def log_critical( *args , **kwargs ):
    _write_log( _tps.CRITICAL , *args , **kwargs )

@register()
def log_exception( *args , **kwargs ):
    from shangjie.utils import traceback2
    exc_msg = traceback2.format_exc( show_locals = True )
    args = list( args )
    if args:
        args[0] += '\n%s'
    else:
        args.append( '%s' )
    args.append( exc_msg )
    _write_log( _tps.ERROR , *args , **kwargs )