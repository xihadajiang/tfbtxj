# coding: gbk
from ftools import register , AttrDict
import traceback2
import re
try:
    import _tps
except:
    import fake_tps as _tps
import log
@register()
def tps( func ):
    def _call( jyzd ):
        try:
            _jyzd = AttrDict( initd = jyzd , kword = None , nocopy = True )
#            _tps.errLog( _tps.DEBUG , '交易字典内容输出：%s' % _jyzd , _tps.RPT_TO_LOG )
#            # 校验流水是否已登记
#            if not _jyzd.LSBZ:
#                ins_lsz( lsh = _jyzd.SYS_XTLSH, jyrq = _jyzd.SYS_JYRQ, jysj = _jyzd.SYS_XTSJ, jym = _jyzd.SYS_JYBM, jgdm = _jyzd.JYJGM, gyh = _jyzd.CZGY )
#                _jyzd.LSBZ = '1'
            r = func( _jyzd )
            # 校验交易字典中的值，确定全部转换为str类型
#            for k , v in jyzd.items():
#                #v = jyzd[ k ]
#                if type(v) != str:
#                    #_tps.errLog( _tps.WARNING, '>>>>>>>>>>>>>>>>>>>[%s]类型错误[%s][%s]'%(k, type(v), repr(v)), _tps.RPT_TO_LOG )
#                    if v == None: jyzd[ k ] = ''
#                    else:         jyzd[ k ] = str( v )
            if r < 0:
                _tps.errLog( _tps.ERROR , '>>>>>>>>>>>>>>>>>>>函数返回：%s,%s' % ( _jyzd.SYS_RspCode , _jyzd.SYS_RspInfo ) , _tps.RPT_TO_LOG )
            return r
        except:
            msg = traceback2.format_exc( show_locals = True )
            log.error(jyzd.get("systemsign",""),msg)
            _tps.errLog( _tps.ERROR ,  msg , _tps.RPT_TO_LOG )
            jyzd['SYS_RspCode'] = 'TS0004'
            jyzd['SYS_RspInfo'] = msg
            _tps.errLog( _tps.DEBUG , '交易字典内容输出：%s' % _jyzd , _tps.RPT_TO_LOG )
            log.error(jyzd.get("systemsign",""), '交易字典内容输出：%s' % _jyzd)
            return -1
    return _call
import json
@register()
def TRAC_DICTTree(jyzd ):
    _jyzd = AttrDict( initd = jyzd , kword = None , nocopy = True )
    log.info(jyzd.get("systemsign",""), '交易字典内容输出：%s' % _jyzd)
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
                if type(ress) == type("string"):
                    ress = ""
                    continue
                ress = ress.get(i)
                if type(ress) == type("string") and "{" in ress:
                    ress = json.loads(ress)
        elif re.match(r"/jyzd+", blm):
            for i in blm.split('/')[2:]:
                if type(ress) == type("string"):
                    ress = ""
                    continue
                ress = ress.get(i)
                if type(ress) == type("string") and "{" in ress:
                    ress = json.loads(ress)
        else:
            for i in blm.split('/')[1:]:
                if type(ress) == type("string"):
                    ress = ""
                    continue
                ress = ress.get(i,"")
                if type(ress) == type("string") and "{" in ress:
                    ress = ress.replace("'",'"')
                    ress = json.loads(ress)
        arg = arg.replace('[%s]'%blm,str(ress) if type(ress) not in (str,unicode) else ress)
    return arg
#jyzd = {}
#REQ={u'root': {u'business_type': u'14900', u'bank_name': u'10000', u'cre_id': '', u'cre_type': '', u'tran_amt': u'10000', u'card_prov': '', u'mobile': '', u'md5_sign': '', u'true_name': u'11111', u'card_id': u'622384609891538799', u'spbillno': u'222222', u'card_type': '', u'postscript': '', u'TransCode': u'api_acp_single.cgi', u'purpose': '', u'spid': u'11111', u'business_no': u'444444', u'bank_ins_code': u'26520300', u'ver': u'1.0', u'cur_type': ''}}
#jyzd["REQ"]=REQ
#jyzd = AttrDict( initd = jyzd , kword = None , nocopy = False )
#print ass( 'pkg_guocai_[jyzd/REQ/root/TransCode]_req' , jyzd )
##tt = AttrDict( initd = tt , kword = None , nocopy = False )
#jyzd = {'aa':'1','LSBZ':'222','test':tt}
#jyzd = AttrDict( initd = jyzd , kword = None , nocopy = False )
#print jyzd.test.a
#@tps
#def test( jyzd ):
#    print jyzd.test
#test( jyzd )
#test( jyzd )
#print ass( 'subflow_[/jyzd/aa]_[/jyzd/LSBZ]_[/jyzd/test/a]unpack' , jyzd )