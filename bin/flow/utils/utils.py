# coding: gbk
from ftools import register , AttrDict
import traceback2
import re
try:
    import _tps
except:
    import fake_tps as _tps

@register()
def tps( func ):
    def _call( jyzd ):
        try:
            _jyzd = AttrDict( initd = jyzd , kword = None , nocopy = True )
            _tps.errLog( _tps.DEBUG , '交易字典内容输出：%s' % _jyzd , _tps.RPT_TO_LOG )
#            # 校验流水是否已登记
#            if not _jyzd.LSBZ:
#                ins_lsz( lsh = _jyzd.SYS_XTLSH, jyrq = _jyzd.SYS_JYRQ, jysj = _jyzd.SYS_XTSJ, jym = _jyzd.SYS_JYBM, jgdm = _jyzd.JYJGM, gyh = _jyzd.CZGY )
#                _jyzd.LSBZ = '1'
            r = func( _jyzd )
            # 校验交易字典中的值，确定全部转换为str类型
            for k , v in jyzd.items():
                #v = jyzd[ k ]
                if type(v) != str:
                    _tps.errLog( _tps.WARNING, '>>>>>>>>>>>>>>>>>>>[%s]类型错误[%s][%s]'%(k, type(v), repr(v)), _tps.RPT_TO_LOG )
                    if v == None: jyzd[ k ] = ''
                    else:         jyzd[ k ] = str( v )
            if r < 0:
                _tps.errLog( _tps.ERROR , '>>>>>>>>>>>>>>>>>>>函数返回：%s,%s' % ( _jyzd.SYS_RspCode , _jyzd.SYS_RspInfo ) , _tps.RPT_TO_LOG )
            return r
        except:
            msg = traceback2.format_exc( show_locals = True )
            _tps.errLog( _tps.ERROR ,  msg , _tps.RPT_TO_LOG )
            jyzd['SYS_RspCode'] = 'TS0004'
            jyzd['SYS_RspInfo'] = msg
            return -1
    return _call
import json
@register()
def TRAC_DICTTree(jyzd ):
    _jyzd = AttrDict( initd = jyzd , kword = None , nocopy = True )
    _tps.errLog( _tps.DEBUG , '交易字典内容输出：%s' % _jyzd , _tps.RPT_TO_LOG )
    return 0
    
@register()
def ass( arg , jyzd ):
    #tps(jyzd)
    jyzd = AttrDict( initd = jyzd , kword = None , nocopy = False )
    """subflow_[/pub/subsysname]_unpack"""
    name = re.compile('\[(.*?)\]' )
    g = name.findall(arg)
    for blm in g:
        ress = jyzd
        if re.match(r"jyzd+", blm):
            for i in blm.split('/')[1:]:
                ress = ress.get(i)
                if type(ress) == type("string") and "{" in ress:
                    ress = json.loads(ress)
        elif re.match(r"/jyzd+", blm):
            for i in blm.split('/')[2:]:
                ress = ress.get(i)
                if type(ress) == type("string") and "{" in ress:
                    ress = json.loads(ress)
        else:
            for i in blm.split('/')[1:]:
                ress = ress.get(i,"")
                if type(ress) == type("string") and "{" in ress:
                    ress = ress.replace("'",'"')
                    ress = json.loads(ress)
        arg = arg.replace('[%s]'%blm,ress)
    return arg
tt={'a':'1'}
tt = AttrDict( initd = tt , kword = None , nocopy = False )
jyzd = {'aa':'1','LSBZ':'222','test':tt}
jyzd = AttrDict( initd = jyzd , kword = None , nocopy = False )
print jyzd.test
@tps
def test( jyzd ):
    print jyzd.aa
#test( jyzd )
#print ass( 'subflow_[/jyzd/aa]_[/jyzd/LSBZ]_[/jyzd/test/a]unpack' , jyzd )