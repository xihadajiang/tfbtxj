#coding:gbk
from utils.utils import tps
from utils.ftools import AttrDict
import flow.flow_utils
from utils import log
from tysf_uitls import *
from tysf_uitls import lnieno as LN
from tysf_uitls import funcname as FUNC
from tysf_uitls import cofilename as FN
from xml2json import *
import os
import sys
from conf import settings
settings.register( 'oaconf' )

BASE_DIR = os.path.dirname(os.path.dirname(__file__))
LOGDIR = os.path.join(os.path.dirname(__file__), '../logs').replace('\\','/')
@tps
def the_end( jyzd  ):
    log.info(jyzd.get("systemsign",""),'%s|%s|组件[%s]执行开始',FN(),LN(),FUNC())
    print '交易结束，更新流水'
    log.info(jyzd.get("systemsign",""),'%s|%s|组件[%s]执行结束',FN(),LN(),FUNC())
    print jyzd.req_msg
    return 0
@tps
def pub_error( jyzd   ):
    log.info(jyzd.get("systemsign",""),'%s|%s|组件[%s]执行开始',FN(),LN(),FUNC())
    log.info(jyzd.get("systemsign",""),'交易异常，更新响应码响应信息，更新流水，插入冲正表')
    print '交易异常，更新响应码响应信息，更新流水，插入冲正表'
    log.info(jyzd.get("systemsign",""),'%s|%s|组件[%s]执行结束',FN(),LN(),FUNC())
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
    log.info(jyzd.get("systemsign",""),'%s|%s|组件[%s]执行开始',FN(),LN(),FUNC())
    log.info(jyzd.get("systemsign",""),'%s|%s|组件[%s]执行结束',FN(),LN(),FUNC())
    return 0

@tps
def END( jyzd   ):
    """
    END
    输出：0 成功 
    """
    log.info(jyzd.get("systemsign",""),'%s|%s|组件[%s]执行开始',FN(),LN(),FUNC())
    print '流程执行结束'
    log.info(jyzd.get("systemsign",""),'%s|%s|组件[%s]执行结束',FN(),LN(),FUNC())
    return 0

@tps
def TRAC_Commbuf( jyzd   ):
    """
    TRAC_Commbuf
    在TRACE日志文件中打印通讯缓冲区内容。
    输入：/commbuf
    输出：0 成功 并打印内容
    """
    log.info(jyzd.get("systemsign",""),'%s|%s|组件[%s]执行开始',FN(),LN(),FUNC())
    print jyzd.TRAC_Commbuf
    print '在TRACE日志文件中打印通讯缓冲区内容。'
    log.info(jyzd.get("systemsign",""),'%s|%s|组件[%s]执行结束',FN(),LN(),FUNC())
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
    resp = """"""
    jyzd["resp"]="%s"%(resp)
    return 0
    
@tps
def DATA_ImpFromBuf(jyzd):
    """
    从通讯缓冲区中导入XML(XML解包)
    输入：/commbuf
    输出：/root
    """
    log.info(jyzd.get("systemsign",""),'%s|%s|组件[%s]执行开始',FN(),LN(),FUNC())
    log.info(jyzd.get("systemsign",""),'%s|%s|组件[%s]执行结束',FN(),LN(),FUNC())
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
    log.info(jyzd.get("systemsign",""),'%s|%s|组件[%s]执行开始',FN(),LN(),FUNC())
    TRAC_DICTTree(jyzd)
    log.info(jyzd.get("systemsign",""),'%s|%s|组件[%s]执行结束',FN(),LN(),FUNC())
    return 0
@tps
def Agentx_SysInit(jyzd):
    """系统参数环境初始化"""
    log.info(jyzd.get("systemsign",""),'%s|%s|组件[%s]执行开始',FN(),LN(),FUNC())
    log.info(jyzd.get("systemsign",""),'%s|%s|组件[%s]执行结束',FN(),LN(),FUNC())
    return 0
@tps
def SSYS_GetIniCfg(jyzd):
    """获取INI文件配置参数组件
    输入：
    1，输入ini文件名，若为相对路径，则取$GAPSETCDIR目录下的配置文件
    2，ini文件中小节的名称 如 ENV
    3，ini文件中参数的名称 如 DBNAME
    4，参数获取后存放的XML节点名称
    """
    log.info(jyzd.get("systemsign",""),'%s|%s|组件[%s]执行开始',FN(),LN(),FUNC())
    log.info(jyzd.get("systemsign",""),'%s|%s|GAPSETCDIR=[%s]',FN(),LN(),settings.GAPSETCDIR)
    import ConfigParser
    config = ConfigParser.ConfigParser()
    config.readfp(open(os.sep.join([settings.GAPSETCDIR,ass( jyzd.input.get('_1') , jyzd )])))
    res = config.get(ass( jyzd.input.get('_2') , jyzd ),ass( jyzd.input.get('_3') , jyzd ))
    ininame = ass( jyzd.input.get('_4') , jyzd )
    jyzd[ininame.replace('.','/').split('/')[-1]] = res
    log.info(jyzd.get("systemsign",""),'%s|%s|%s=%s',FN(),LN(),ininame,res)
    log.info(jyzd.get("systemsign",""),'%s|%s|组件[%s]执行结束',FN(),LN(),FUNC())
    return 0
@tps
def SAPEX_RESCHECK(jyzd):
    """资源检查扩展组件
    输入：
    1，请参考RMAtool命令,412-交易,415-流程
    2，资源名称
    """
    log.info(jyzd.get("systemsign",""),'%s|%s|组件[%s]执行开始',FN(),LN(),FUNC())
    log.info(jyzd.get("systemsign",""),'%s|%s|组件[%s]执行结束',FN(),LN(),FUNC())
    return 0
@tps
def PY_GetCipher(jyzd):
    """获取Cipher
    输入：
    1，resp需要返回的字段
    """
    log.info(jyzd.get("systemsign",""),'%s|%s|组件[%s]执行开始',FN(),LN(),FUNC())
    req = jyzd.get("REQ")
    log.info(jyzd.get("systemsign",""),'%s|%s|对字典req=%s进行处理',FN(),LN(),str(req))
    root = req.get("root",{})
    log.info(jyzd.get("systemsign",""),'%s|%s|字典root=%s',FN(),LN(),str(root))
    signdata = sort(root).encode('UTF-8') + "&key=%s"%jyzd.KEY
    log.info(jyzd.get("systemsign",""),'%s|%s|排序后的数据signdata=%s',FN(),LN(),str(signdata))
    sign_md5 = MD5(signdata)
    signdata = signdata + "&md5_sign=%s"%sign_md5
    log.info(jyzd.get("systemsign",""),'%s|%s|进行MD5运算后sign_md5=%s',FN(),LN(),sign_md5)
    pubkey = r'H:\share\work\银联全渠道\天付宝通讯机\tfb_txj\lib\gczf_rsa_public.pem' 
    cipher_data = getcipher(signdata,pubkey)
    from urllib import urlencode
    jyzd["cipher_data"] = urlencode({'cipher_data':cipher_data})
    log.info(jyzd.get("systemsign",""),'%s|%s|cipher_data[%s]',FN(),LN(),cipher_data)
    log.info(jyzd.get("systemsign",""),'%s|%s|组件[%s]执行结束',FN(),LN(),FUNC())
    return 0

@tps
def PY_MsgAddHead(jyzd):
    """
    给通讯报文增加通讯报文头
    输入：1,报文模板名称 2,报文体 3,增加报文头后的报文
    """
    log.info(jyzd.get("systemsign",""),'%s|%s|组件[%s]执行开始',FN(),LN(),FUNC())
    resp = settings.GUOCAI_TEMPLATE%{"txid":jyzd.REQ.get("root").get("TransCode"),"msg_len":len(jyzd.cipher_data),"msg":jyzd.cipher_data}
    jyzd["resp"] = resp
    log.info(jyzd.get("systemsign",""),'%s|%s|resp=[%s]',FN(),LN(),resp)
    log.info(jyzd.get("systemsign",""),'%s|%s|组件[%s]执行结束',FN(),LN(),FUNC())
    return 0
    
@tps
def SPKG_IXMLtoOXML(jyzd):
    """
    内部XML->外部XML报文转换
    输入：报文配置
    """
    log.info(jyzd.get("systemsign",""),'%s|%s|组件[%s]执行开始',FN(),LN(),FUNC())
    import json
    f = file("../flow/gp_sys_guocai_fail_resp.json")
    gp = f.read()
    f.close
    s = ass( gp , jyzd )
    log.info(jyzd.get("systemsign",""),'%s|%s|json[%s]',FN(),LN(),s)
    s = json.loads(s)
    import dicttoxml
    jyzd["resp"] = dicttoxml.dicttoxml(s,root=False,attr_type=False)
    log.info(jyzd.get("systemsign",""),'%s|%s|resp[%s]',FN(),LN(),jyzd["resp"])
    log.info(jyzd.get("systemsign",""),'%s|%s|组件[%s]执行结束',FN(),LN(),FUNC())
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
    log.info(jyzd.get("systemsign",""),'%s|%s|组件[%s]执行开始',FN(),LN(),FUNC())
    print jyzd.TRAC_Commbuf
    print '在TRACE日志文件中打印通讯缓冲区内容。'
    log.info(jyzd.get("systemsign",""),'%s|%s|组件[%s]执行结束',FN(),LN(),FUNC())
    return 0
    
@tps
def SAPEX_CONVERT( jyzd   ):
    """
    SAPEX_CONVERT
    数据码制转化组件。
    输入：1,数据格式 2,源码制代码 3,目标码制代码 4,源节点 5,目标节点
    输出：0 成功 并打印内容
    """
    log.info(jyzd.get("systemsign",""),'%s|%s|组件[%s]执行开始',FN(),LN(),FUNC())
    sjgs = ass( jyzd.input.get('_1') , jyzd )
    sou_coding = ass( jyzd.input.get('_2') , jyzd )
    tar_coding = ass( jyzd.input.get('_3') , jyzd )
    sou_data = jyzd.get(ass( jyzd.input.get('_4') , jyzd ).split("/")[-1])
    tar_data = ass( jyzd.input.get('_5') , jyzd ).split("/")[-1]
    exec("""jyzd['%s'] = sou_data.decode('%s').encode('%s')"""%(tar_data,sou_coding,tar_coding))
    log.info(jyzd.get("systemsign",""),'%s|%s|jyzd[%s]=[%s]',FN(),LN(),tar_data,jyzd[tar_data])
    log.info(jyzd.get("systemsign",""),'%s|%s|组件[%s]执行结束',FN(),LN(),FUNC())
    return 0
    

@tps
def STRAC_XMLTree(jyzd):
    """
    在TRACE日志文件中记录当前的XML结构树的内容。
    """
    log.info(jyzd.get("systemsign",""),'%s|%s|组件[%s]执行开始',FN(),LN(),FUNC())
    TRAC_DICTTree(jyzd)
    log.info(jyzd.get("systemsign",""),'%s|%s|组件[%s]执行结束',FN(),LN(),FUNC())
    return 0
    
    
@tps
def SDATA_MStrCompare(jyzd):
    """
    多字符比较组件
    输入：1：比较值 2：可以为：'=='，'!=' 3：比较值
    输出：0 假 1 真
    """
    log.info(jyzd.get("systemsign",""),'%s|%s|组件[%s]执行开始',FN(),LN(),FUNC())
    cmd = "'%s'%s'%s'"%(ass( jyzd.input.get('_1') , jyzd ),ass( jyzd.input.get('_2') , jyzd ),ass( jyzd.input.get('_3') , jyzd ))
    log.info(jyzd.get("systemsign",""),'%s|%s|执行[%s]',FN(),LN(),cmd)
    if eval(cmd):
        log.info(jyzd.get("systemsign",""),'%s|%s|组件[%s]执行结束 返回 1',FN(),LN(),FUNC())
        return 1
    else:
        log.info(jyzd.get("systemsign",""),'%s|%s|组件[%s]执行结束 返回 0',FN(),LN(),FUNC())
        return 0
@tps
def SDATA_MSetValue(jyzd):
    """
    多字符比较组件
    输入：1：比较值 2：可以为：'=='，'!=' 3：比较值
    输出：0 假 1 真
    """
    log.info(jyzd.get("systemsign",""),'%s|%s|组件[%s]执行开始',FN(),LN(),FUNC())
    log.info(jyzd.get("systemsign",""),'%s|%s|组件[%s]执行结束',FN(),LN(),FUNC())
    return 0
@tps
def SDATA_ImpFromBuf(jyzd):
    """
    多字符比较组件
    输入：1，/commbuf 2，/jyzd
    输出：0 假 1 真
    """
    log.info(jyzd.get("systemsign",""),'%s|%s|组件[%s]执行开始',FN(),LN(),FUNC())
    log.info(jyzd.get("systemsign",""),'%s|%s|将commbuf内容转换到字典中',FN(),LN())
    xml = getxml(jyzd.commbuf)
    xml = changeCode(xml,'UTF-8')
    resp_dict = Xml2Json(xml).result
    log.info(jyzd.get("systemsign",""),'%s|%s|转换后的字典resp_dict=%s',FN(),LN(),str(resp_dict))
    jyzd["REQ"] = resp_dict
    log.info(jyzd.get("systemsign",""),'%s|%s|组件[%s]执行结束',FN(),LN(),FUNC())
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
    log.info(jyzd.get("systemsign",""),'%s|%s|组件[%s]执行开始',FN(),LN(),FUNC())
    subflow = ass( jyzd.input.get('_1') , jyzd )
    print '执行指定的子流程[%s]'%subflow
    log.info(jyzd.get("systemsign",""),'执行[%s]'%subflow)
    TRAC_DICTTree(jyzd )
    log.info(jyzd.get("systemsign",""), 'jyzd[%s]'%( type(jyzd)))
    ret = flow.flow_utils.goflow("../flow/%s.flow"%subflow,jyzd)
    log.info(jyzd.get("systemsign",""),'%s|%s|组件[%s]执行结束',FN(),LN(),FUNC())
    return ret
    
