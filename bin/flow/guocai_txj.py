#coding:gbk
from utils.utils import tps
from utils.ftools import AttrDict
import flow_utils

@tps
def the_end( jyzd  ):
    print '交易结束，更新流水'
    print jyzd.req_msg
    return 0
@tps
def pub_error( jyzd   ):
    print '交易异常，更新响应码响应信息，更新流水，插入冲正表'
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



<?xml version='1.0' encoding="GB2312"?><root><ver>1.0</ver><spid>11111</spid><spbillno>222222</spbillno><business_type>14900</business_type><business_no>444444</business_no><tran_amt>10000</tran_amt><cur_type></cur_type><true_name>11111</true_name><mobile></mobile><cre_id></cre_id><cre_type></cre_type><card_id>622384609891538799</card_id><card_type></card_type><bank_name>10000</bank_name><bank_ins_code>26520300</bank_ins_code><card_prov></card_prov><purpose></purpose><postscript></postscript><md5_sign>42f5e82173b880a5213cfc640707a936</md5_sign></root>】
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
    输出：0 成功 
    """
    print '流程执行开始'
    return 0

@tps
def END( jyzd   ):
    """
    END
    输出：0 成功 
    """
    print '流程执行结束'
    return 0

@tps
def TRAC_Commbuf( jyzd   ):
    """
    TRAC_Commbuf
    在TRACE日志文件中打印通讯缓冲区内容。
    输入：/commbuf
    输出：0 成功 并打印内容
    """
    print jyzd.TRAC_Commbuf
    print '在TRACE日志文件中打印通讯缓冲区内容。'
    return 0

@tps
def CNTR_CallSubFlow( jyzd  ):
    """
    CNTR_CallSubFlow
    执行指定的子流程。
    输入：subflow_[/pub/subsysname]_unpack
    输出：0 成功 
    输出：1 失败
    """
    print ass( jyzd.input.get('_1') , jyzd )
    print '执行指定的子流程。'
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



<?xml version='1.0' encoding="GB2312"?><root><ver>1.0</ver><spid>11111</spid><spbillno>222222</spbillno><business_type>14900</business_type><business_no>444444</business_no><tran_amt>10000</tran_amt><cur_type></cur_type><true_name>11111</true_name><mobile></mobile><cre_id></cre_id><cre_type></cre_type><card_id>622384609891538799</card_id><card_type></card_type><bank_name>10000</bank_name><bank_ins_code>26520300</bank_ins_code><card_prov></card_prov><purpose></purpose><postscript></postscript><md5_sign>42f5e82173b880a5213cfc640707a936</md5_sign></root>】
"""
    jyzd["resp"]="%s"%(resp)
    return 0
    
@tps
def DATA_ImpFromBuf(jyzd):
    """
    从通讯缓冲区中导入XML(XML解包)
    输入：/commbuf
    输出：/root
    """
    return 0
@tps
def DATA_MStrCompare(jyzd):
    """
    多字符比较组件
    输入：1：比较值 2：可以为：'=='，'!=' 3：比较值
    输出：0 假 1 真
    """
    return 1
@tps
def TRAC_XMLTree(jyzd):
    """
    在TRACE日志文件中记录当前的XML结构树的内容。
    """
    TRAC_DICTTree(jyzd)
    return 0
@tps
def Agentx_SysInit(jyzd):
    """系统参数环境初始化"""
    return 0
@tps
def PKG_IXMLtoOXML(jyzd):
    """
    内部XML->外部XML报文转换
    输入：报文配置
    """
    return 0
    
@tps
def DATA_MSetValue():
    """
    为多个指定XML元素进行解析式字符赋值
    """
    for k,v in jyzd.input.items():
        print k,v
        ass( jyzd.input.get('_1') , jyzd )
    return 0
    
    

@tps
def STRAC_Commbuf( jyzd   ):
    """
    TRAC_Commbuf
    在TRACE日志文件中打印通讯缓冲区内容。
    输入：/commbuf
    输出：0 成功 并打印内容
    """
    print jyzd.TRAC_Commbuf
    print '在TRACE日志文件中打印通讯缓冲区内容。'
    return 0
    

@tps
def STRAC_XMLTree(jyzd):
    """
    在TRACE日志文件中记录当前的XML结构树的内容。
    """
    TRAC_DICTTree(jyzd)
    return 0
    
    
@tps
def SDATA_MStrCompare(jyzd):
    """
    多字符比较组件
    输入：1：比较值 2：可以为：'=='，'!=' 3：比较值
    输出：0 假 1 真
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
    多字符比较组件
    输入：1：比较值 2：可以为：'=='，'!=' 3：比较值
    输出：0 假 1 真
    """
    for i in jyzd.input:
        print i
    return 0
@tps
def SDATA_ImpFromBuf(jyzd):
    """
    多字符比较组件
    输入：1：比较值 2：可以为：'=='，'!=' 3：比较值
    输出：0 假 1 真
    """
    for i in jyzd.input:
        print i
    return 0
@tps
def SCNTR_CallSubFlow( jyzd  ):
    """
    CNTR_CallSubFlow
    执行指定的子流程。
    输入：subflow_[/pub/subsysname]_unpack
    输出：0 成功 
    输出：1 失败
    """
    subflow = ass( jyzd.input.get('_1') , jyzd )
    print '执行指定的子流程[%s]'%subflow
    ret = flow.flow_utils.goflow("../flow/%s.flow"%subflow,jyzd)
    print ret
    return 0
    
