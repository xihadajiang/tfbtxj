# coding: gbk

"""
    本模块用于模仿pynode中的_tps模块
"""

CRITICAL = 5000
ERROR    = 4000
WARNING  = 3000
INFO     = 2000
DEBUG    = 1000
RPT_TO_LOG = 1
from datetime import datetime
def e_datetime(value ,  buflen = 0 , align = 'L' , fmt = '%Y%m%d%H%M%S' ,fillchar = ' ' ):
    """
    打包，日期 时间型打包为格式字符串
    参数列表：value:       字段内容
              buflen:      填充后总长度 
              align: 字段对齐(默认左对齐) L:左对齐 R:右对齐 C:居中
              format:      转换格式(默认'%Y%m%d%H%M%S')
              fillchar:    填充字符(默认空格符)
    """
    try:
        if value:
            tmpstr = value.strftime( fmt )
        else:
            tmpstr = ''
        return  tmpstr
    except:
        raise RuntimeError( '输入内容[%s]不是合法的格式' % value )

def e_now( buflen = 0 , align = 'L' , fmt = '%Y%m%d%H%M%S' ,fillchar = ' ' ):
    """
    打包，获取当前时间，并调用e_datetime方法返回一个日期时间型字段
    参数列表：buflen:      填充后总长度 
              align: 字段对齐(默认左对齐) L:左对齐 R:右对齐 C:居中
              format:      转换格式(默认'%Y%m%d%H%M%S')
              fillchar:    填充字符(默认空格符)
    """
    n = datetime.now()
    return e_datetime( n , buflen , align , fmt , fillchar )
def errLog( lvl , msg , kind ):
    print e_now() , msg
