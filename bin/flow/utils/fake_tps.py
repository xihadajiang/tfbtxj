# coding: gbk

"""
    ��ģ������ģ��pynode�е�_tpsģ��
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
    ��������� ʱ���ʹ��Ϊ��ʽ�ַ���
    �����б�value:       �ֶ�����
              buflen:      �����ܳ��� 
              align: �ֶζ���(Ĭ�������) L:����� R:�Ҷ��� C:����
              format:      ת����ʽ(Ĭ��'%Y%m%d%H%M%S')
              fillchar:    ����ַ�(Ĭ�Ͽո��)
    """
    try:
        if value:
            tmpstr = value.strftime( fmt )
        else:
            tmpstr = ''
        return  tmpstr
    except:
        raise RuntimeError( '��������[%s]���ǺϷ��ĸ�ʽ' % value )

def e_now( buflen = 0 , align = 'L' , fmt = '%Y%m%d%H%M%S' ,fillchar = ' ' ):
    """
    �������ȡ��ǰʱ�䣬������e_datetime��������һ������ʱ�����ֶ�
    �����б�buflen:      �����ܳ��� 
              align: �ֶζ���(Ĭ�������) L:����� R:�Ҷ��� C:����
              format:      ת����ʽ(Ĭ��'%Y%m%d%H%M%S')
              fillchar:    ����ַ�(Ĭ�Ͽո��)
    """
    n = datetime.now()
    return e_datetime( n , buflen , align , fmt , fillchar )
def errLog( lvl , msg , kind ):
    print e_now() , msg
