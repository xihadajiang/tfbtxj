#coding:gbk
from utils.utils import tps
from utils.ftools import AttrDict
import flow_utils

@tps
def the_end( jyzd  ):
    print '���׽�����������ˮ'
    print jyzd.req_msg
    return 0
@tps
def pub_error( jyzd   ):
    print '�����쳣��������Ӧ����Ӧ��Ϣ��������ˮ�����������'
    resp = """POST /cgi-bin/v2.0/api_acp_single.cgi HTTP/1.1

Content-Length: 557

Host: apitest.tfb8.com

Referer: http://apitest.tfb8.com/cgi-bin/v2.0/api_acp_single.cgi

Accept-Encoding: GBK, deflate

Cache-Control: no-cache

Accept-Language: zh-cn

Content-Type: application/x-www-form-urlencoded

Connection: Keep-Alive

Accept: image/gif, */*

User-Agent: Mozilla/4.0 (compatible; MSIE 6.0; Windows NT 5.1; SV1; .NET CLR 2.0.50727)



<?xml version='1.0' encoding="GB2312"?><root><ver>1.0</ver><spid>11111</spid><spbillno>222222</spbillno><business_type>14900</business_type><business_no>444444</business_no><tran_amt>10000</tran_amt><cur_type></cur_type><true_name>11111</true_name><mobile></mobile><cre_id></cre_id><cre_type></cre_type><card_id>622384609891538799</card_id><card_type></card_type><bank_name>10000</bank_name><bank_ins_code>26520300</bank_ins_code><card_prov></card_prov><purpose></purpose><postscript></postscript><md5_sign>42f5e82173b880a5213cfc640707a936</md5_sign></root>��
"""
    jyzd["resp"]="%s"%(resp)

    return 0
@tps
def GAPSMsgUnPack(jyzd  ):
    print 'GAPSMsgUnPack'
    return 0
@tps
def GCMsgUnPack(jyzd  ):
    print 'YLMsgUnPack'
    return 0
@tps
def GAPSMsgPack(jyzd  ):
    print 'GAPSMsgPack'
    return 0
@tps
def gc_sign( jyzd    ):
    print '====gc_sign====='
    return 0
@tps
def pack_gc_dk( jyzd   ):
    print '====pack_gc_dk====='
    return 0

@tps
def BEGIN( jyzd ):
    """
    BEGIN
    �����0 �ɹ� 
    """
    print '����ִ�п�ʼ'
    return 0

@tps
def END( jyzd   ):
    """
    END
    �����0 �ɹ� 
    """
    print '����ִ�н���'
    return 0

@tps
def TRAC_Commbuf( jyzd   ):
    """
    TRAC_Commbuf
    ��TRACE��־�ļ��д�ӡͨѶ���������ݡ�
    ���룺/commbuf
    �����0 �ɹ� ����ӡ����
    """
    print jyzd.TRAC_Commbuf
    print '��TRACE��־�ļ��д�ӡͨѶ���������ݡ�'
    return 0

@tps
def CNTR_CallSubFlow( jyzd  ):
    """
    CNTR_CallSubFlow
    ִ��ָ���������̡�
    ���룺subflow_[/pub/subsysname]_unpack
    �����0 �ɹ� 
    �����1 ʧ��
    """
    print ass( jyzd.input.get('_1') , jyzd )
    print 'ִ��ָ���������̡�'
    resp = """POST /cgi-bin/v2.0/api_acp_single.cgi HTTP/1.1

Content-Length: 557

Host: apitest.tfb8.com

Referer: http://apitest.tfb8.com/cgi-bin/v2.0/api_acp_single.cgi

Accept-Encoding: GBK, deflate

Cache-Control: no-cache

Accept-Language: zh-cn

Content-Type: application/x-www-form-urlencoded

Connection: Keep-Alive

Accept: image/gif, */*

User-Agent: Mozilla/4.0 (compatible; MSIE 6.0; Windows NT 5.1; SV1; .NET CLR 2.0.50727)



<?xml version='1.0' encoding="GB2312"?><root><ver>1.0</ver><spid>11111</spid><spbillno>222222</spbillno><business_type>14900</business_type><business_no>444444</business_no><tran_amt>10000</tran_amt><cur_type></cur_type><true_name>11111</true_name><mobile></mobile><cre_id></cre_id><cre_type></cre_type><card_id>622384609891538799</card_id><card_type></card_type><bank_name>10000</bank_name><bank_ins_code>26520300</bank_ins_code><card_prov></card_prov><purpose></purpose><postscript></postscript><md5_sign>42f5e82173b880a5213cfc640707a936</md5_sign></root>��
"""
    jyzd["resp"]="%s"%(resp)
    return 0
    
@tps
def DATA_ImpFromBuf(jyzd):
    """
    ��ͨѶ�������е���XML(XML���)
    ���룺/commbuf
    �����/root
    """
    return 0
@tps
def DATA_MStrCompare(jyzd):
    """
    ���ַ��Ƚ����
    ���룺1���Ƚ�ֵ 2������Ϊ��'=='��'!=' 3���Ƚ�ֵ
    �����0 �� 1 ��
    """
    return 1
@tps
def TRAC_XMLTree(jyzd):
    """
    ��TRACE��־�ļ��м�¼��ǰ��XML�ṹ�������ݡ�
    """
    TRAC_DICTTree(jyzd)
    return 0
@tps
def Agentx_SysInit(jyzd):
    """ϵͳ����������ʼ��"""
    return 0
@tps
def PKG_IXMLtoOXML(jyzd):
    """
    �ڲ�XML->�ⲿXML����ת��
    ���룺��������
    """
    return 0
    
@tps
def DATA_MSetValue():
    """
    Ϊ���ָ��XMLԪ�ؽ��н���ʽ�ַ���ֵ
    """
    for k,v in jyzd.input.items():
        print k,v
        ass( jyzd.input.get('_1') , jyzd )
    return 0
    
    

@tps
def STRAC_Commbuf( jyzd   ):
    """
    TRAC_Commbuf
    ��TRACE��־�ļ��д�ӡͨѶ���������ݡ�
    ���룺/commbuf
    �����0 �ɹ� ����ӡ����
    """
    print jyzd.TRAC_Commbuf
    print '��TRACE��־�ļ��д�ӡͨѶ���������ݡ�'
    return 0
    

@tps
def STRAC_XMLTree(jyzd):
    """
    ��TRACE��־�ļ��м�¼��ǰ��XML�ṹ�������ݡ�
    """
    TRAC_DICTTree(jyzd)
    return 0
    
    
@tps
def SDATA_MStrCompare(jyzd):
    """
    ���ַ��Ƚ����
    ���룺1���Ƚ�ֵ 2������Ϊ��'=='��'!=' 3���Ƚ�ֵ
    �����0 �� 1 ��
    """
    cmd = "'%s'%s'%s'"%(ass( jyzd.input.get('_1') , jyzd ),ass( jyzd.input.get('_2') , jyzd ),ass( jyzd.input.get('_3') , jyzd ))
    print cmd
    if eval(cmd):
        return 1
    else:
        return 0
@tps
def SDATA_MSetValue(jyzd):
    """
    ���ַ��Ƚ����
    ���룺1���Ƚ�ֵ 2������Ϊ��'=='��'!=' 3���Ƚ�ֵ
    �����0 �� 1 ��
    """
    for i in jyzd.input:
        print i
    return 0
@tps
def SDATA_ImpFromBuf(jyzd):
    """
    ���ַ��Ƚ����
    ���룺1���Ƚ�ֵ 2������Ϊ��'=='��'!=' 3���Ƚ�ֵ
    �����0 �� 1 ��
    """
    for i in jyzd.input:
        print i
    return 0
@tps
def SCNTR_CallSubFlow( jyzd  ):
    """
    CNTR_CallSubFlow
    ִ��ָ���������̡�
    ���룺subflow_[/pub/subsysname]_unpack
    �����0 �ɹ� 
    �����1 ʧ��
    """
    subflow = ass( jyzd.input.get('_1') , jyzd )
    print 'ִ��ָ����������[%s]'%subflow
    ret = flow.flow_utils.goflow("../flow/%s.flow"%subflow,jyzd)
    print ret
    return 0
    
