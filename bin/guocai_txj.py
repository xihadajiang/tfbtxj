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
    log.info(jyzd.get("systemsign",""),'%s|%s|���[%s]ִ�п�ʼ',FN(),LN(),FUNC())
    print '���׽�����������ˮ'
    log.info(jyzd.get("systemsign",""),'%s|%s|���[%s]ִ�н���',FN(),LN(),FUNC())
    print jyzd.req_msg
    return 0
@tps
def pub_error( jyzd   ):
    log.info(jyzd.get("systemsign",""),'%s|%s|���[%s]ִ�п�ʼ',FN(),LN(),FUNC())
    log.info(jyzd.get("systemsign",""),'�����쳣��������Ӧ����Ӧ��Ϣ��������ˮ�����������')
    print '�����쳣��������Ӧ����Ӧ��Ϣ��������ˮ�����������'
    log.info(jyzd.get("systemsign",""),'%s|%s|���[%s]ִ�н���',FN(),LN(),FUNC())
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
    log.info(jyzd.get("systemsign",""),'%s|%s|���[%s]ִ�п�ʼ',FN(),LN(),FUNC())
    log.info(jyzd.get("systemsign",""),'%s|%s|���[%s]ִ�н���',FN(),LN(),FUNC())
    return 0

@tps
def END( jyzd   ):
    """
    END
    �����0 �ɹ� 
    """
    log.info(jyzd.get("systemsign",""),'%s|%s|���[%s]ִ�п�ʼ',FN(),LN(),FUNC())
    print '����ִ�н���'
    log.info(jyzd.get("systemsign",""),'%s|%s|���[%s]ִ�н���',FN(),LN(),FUNC())
    return 0

@tps
def TRAC_Commbuf( jyzd   ):
    """
    TRAC_Commbuf
    ��TRACE��־�ļ��д�ӡͨѶ���������ݡ�
    ���룺/commbuf
    �����0 �ɹ� ����ӡ����
    """
    log.info(jyzd.get("systemsign",""),'%s|%s|���[%s]ִ�п�ʼ',FN(),LN(),FUNC())
    print jyzd.TRAC_Commbuf
    print '��TRACE��־�ļ��д�ӡͨѶ���������ݡ�'
    log.info(jyzd.get("systemsign",""),'%s|%s|���[%s]ִ�н���',FN(),LN(),FUNC())
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
    resp = """"""
    jyzd["resp"]="%s"%(resp)
    return 0
    
@tps
def DATA_ImpFromBuf(jyzd):
    """
    ��ͨѶ�������е���XML(XML���)
    ���룺/commbuf
    �����/root
    """
    log.info(jyzd.get("systemsign",""),'%s|%s|���[%s]ִ�п�ʼ',FN(),LN(),FUNC())
    log.info(jyzd.get("systemsign",""),'%s|%s|���[%s]ִ�н���',FN(),LN(),FUNC())
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
    log.info(jyzd.get("systemsign",""),'%s|%s|���[%s]ִ�п�ʼ',FN(),LN(),FUNC())
    TRAC_DICTTree(jyzd)
    log.info(jyzd.get("systemsign",""),'%s|%s|���[%s]ִ�н���',FN(),LN(),FUNC())
    return 0
@tps
def Agentx_SysInit(jyzd):
    """ϵͳ����������ʼ��"""
    log.info(jyzd.get("systemsign",""),'%s|%s|���[%s]ִ�п�ʼ',FN(),LN(),FUNC())
    log.info(jyzd.get("systemsign",""),'%s|%s|���[%s]ִ�н���',FN(),LN(),FUNC())
    return 0
@tps
def SSYS_GetIniCfg(jyzd):
    """��ȡINI�ļ����ò������
    ���룺
    1������ini�ļ�������Ϊ���·������ȡ$GAPSETCDIRĿ¼�µ������ļ�
    2��ini�ļ���С�ڵ����� �� ENV
    3��ini�ļ��в��������� �� DBNAME
    4��������ȡ���ŵ�XML�ڵ�����
    """
    log.info(jyzd.get("systemsign",""),'%s|%s|���[%s]ִ�п�ʼ',FN(),LN(),FUNC())
    log.info(jyzd.get("systemsign",""),'%s|%s|GAPSETCDIR=[%s]',FN(),LN(),settings.GAPSETCDIR)
    import ConfigParser
    config = ConfigParser.ConfigParser()
    config.readfp(open(os.sep.join([settings.GAPSETCDIR,ass( jyzd.input.get('_1') , jyzd )])))
    res = config.get(ass( jyzd.input.get('_2') , jyzd ),ass( jyzd.input.get('_3') , jyzd ))
    ininame = ass( jyzd.input.get('_4') , jyzd )
    jyzd[ininame.replace('.','/').split('/')[-1]] = res
    log.info(jyzd.get("systemsign",""),'%s|%s|%s=%s',FN(),LN(),ininame,res)
    log.info(jyzd.get("systemsign",""),'%s|%s|���[%s]ִ�н���',FN(),LN(),FUNC())
    return 0
@tps
def SAPEX_RESCHECK(jyzd):
    """��Դ�����չ���
    ���룺
    1����ο�RMAtool����,412-����,415-����
    2����Դ����
    """
    log.info(jyzd.get("systemsign",""),'%s|%s|���[%s]ִ�п�ʼ',FN(),LN(),FUNC())
    log.info(jyzd.get("systemsign",""),'%s|%s|���[%s]ִ�н���',FN(),LN(),FUNC())
    return 0
@tps
def PY_GetCipher(jyzd):
    """��ȡCipher
    ���룺
    1��resp��Ҫ���ص��ֶ�
    """
    log.info(jyzd.get("systemsign",""),'%s|%s|���[%s]ִ�п�ʼ',FN(),LN(),FUNC())
    req = jyzd.get("REQ")
    log.info(jyzd.get("systemsign",""),'%s|%s|���ֵ�req=%s���д���',FN(),LN(),str(req))
    root = req.get("root",{})
    log.info(jyzd.get("systemsign",""),'%s|%s|�ֵ�root=%s',FN(),LN(),str(root))
    signdata = sort(root).encode('UTF-8') + "&key=%s"%jyzd.KEY
    log.info(jyzd.get("systemsign",""),'%s|%s|����������signdata=%s',FN(),LN(),str(signdata))
    sign_md5 = MD5(signdata)
    signdata = signdata + "&md5_sign=%s"%sign_md5
    log.info(jyzd.get("systemsign",""),'%s|%s|����MD5�����sign_md5=%s',FN(),LN(),sign_md5)
    pubkey = r'H:\share\work\����ȫ����\�츶��ͨѶ��\tfb_txj\lib\gczf_rsa_public.pem' 
    cipher_data = getcipher(signdata,pubkey)
    from urllib import urlencode
    jyzd["cipher_data"] = urlencode({'cipher_data':cipher_data})
    log.info(jyzd.get("systemsign",""),'%s|%s|cipher_data[%s]',FN(),LN(),cipher_data)
    log.info(jyzd.get("systemsign",""),'%s|%s|���[%s]ִ�н���',FN(),LN(),FUNC())
    return 0

@tps
def PY_MsgAddHead(jyzd):
    """
    ��ͨѶ��������ͨѶ����ͷ
    ���룺1,����ģ������ 2,������ 3,���ӱ���ͷ��ı���
    """
    log.info(jyzd.get("systemsign",""),'%s|%s|���[%s]ִ�п�ʼ',FN(),LN(),FUNC())
    resp = settings.GUOCAI_TEMPLATE%{"txid":jyzd.REQ.get("root").get("TransCode"),"msg_len":len(jyzd.cipher_data),"msg":jyzd.cipher_data}
    jyzd["resp"] = resp
    log.info(jyzd.get("systemsign",""),'%s|%s|resp=[%s]',FN(),LN(),resp)
    log.info(jyzd.get("systemsign",""),'%s|%s|���[%s]ִ�н���',FN(),LN(),FUNC())
    return 0
    
@tps
def SPKG_IXMLtoOXML(jyzd):
    """
    �ڲ�XML->�ⲿXML����ת��
    ���룺��������
    """
    log.info(jyzd.get("systemsign",""),'%s|%s|���[%s]ִ�п�ʼ',FN(),LN(),FUNC())
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
    log.info(jyzd.get("systemsign",""),'%s|%s|���[%s]ִ�н���',FN(),LN(),FUNC())
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
    log.info(jyzd.get("systemsign",""),'%s|%s|���[%s]ִ�п�ʼ',FN(),LN(),FUNC())
    print jyzd.TRAC_Commbuf
    print '��TRACE��־�ļ��д�ӡͨѶ���������ݡ�'
    log.info(jyzd.get("systemsign",""),'%s|%s|���[%s]ִ�н���',FN(),LN(),FUNC())
    return 0
    
@tps
def SAPEX_CONVERT( jyzd   ):
    """
    SAPEX_CONVERT
    ��������ת�������
    ���룺1,���ݸ�ʽ 2,Դ���ƴ��� 3,Ŀ�����ƴ��� 4,Դ�ڵ� 5,Ŀ��ڵ�
    �����0 �ɹ� ����ӡ����
    """
    log.info(jyzd.get("systemsign",""),'%s|%s|���[%s]ִ�п�ʼ',FN(),LN(),FUNC())
    sjgs = ass( jyzd.input.get('_1') , jyzd )
    sou_coding = ass( jyzd.input.get('_2') , jyzd )
    tar_coding = ass( jyzd.input.get('_3') , jyzd )
    sou_data = jyzd.get(ass( jyzd.input.get('_4') , jyzd ).split("/")[-1])
    tar_data = ass( jyzd.input.get('_5') , jyzd ).split("/")[-1]
    exec("""jyzd['%s'] = sou_data.decode('%s').encode('%s')"""%(tar_data,sou_coding,tar_coding))
    log.info(jyzd.get("systemsign",""),'%s|%s|jyzd[%s]=[%s]',FN(),LN(),tar_data,jyzd[tar_data])
    log.info(jyzd.get("systemsign",""),'%s|%s|���[%s]ִ�н���',FN(),LN(),FUNC())
    return 0
    

@tps
def STRAC_XMLTree(jyzd):
    """
    ��TRACE��־�ļ��м�¼��ǰ��XML�ṹ�������ݡ�
    """
    log.info(jyzd.get("systemsign",""),'%s|%s|���[%s]ִ�п�ʼ',FN(),LN(),FUNC())
    TRAC_DICTTree(jyzd)
    log.info(jyzd.get("systemsign",""),'%s|%s|���[%s]ִ�н���',FN(),LN(),FUNC())
    return 0
    
    
@tps
def SDATA_MStrCompare(jyzd):
    """
    ���ַ��Ƚ����
    ���룺1���Ƚ�ֵ 2������Ϊ��'=='��'!=' 3���Ƚ�ֵ
    �����0 �� 1 ��
    """
    log.info(jyzd.get("systemsign",""),'%s|%s|���[%s]ִ�п�ʼ',FN(),LN(),FUNC())
    cmd = "'%s'%s'%s'"%(ass( jyzd.input.get('_1') , jyzd ),ass( jyzd.input.get('_2') , jyzd ),ass( jyzd.input.get('_3') , jyzd ))
    log.info(jyzd.get("systemsign",""),'%s|%s|ִ��[%s]',FN(),LN(),cmd)
    if eval(cmd):
        log.info(jyzd.get("systemsign",""),'%s|%s|���[%s]ִ�н��� ���� 1',FN(),LN(),FUNC())
        return 1
    else:
        log.info(jyzd.get("systemsign",""),'%s|%s|���[%s]ִ�н��� ���� 0',FN(),LN(),FUNC())
        return 0
@tps
def SDATA_MSetValue(jyzd):
    """
    ���ַ��Ƚ����
    ���룺1���Ƚ�ֵ 2������Ϊ��'=='��'!=' 3���Ƚ�ֵ
    �����0 �� 1 ��
    """
    log.info(jyzd.get("systemsign",""),'%s|%s|���[%s]ִ�п�ʼ',FN(),LN(),FUNC())
    log.info(jyzd.get("systemsign",""),'%s|%s|���[%s]ִ�н���',FN(),LN(),FUNC())
    return 0
@tps
def SDATA_ImpFromBuf(jyzd):
    """
    ���ַ��Ƚ����
    ���룺1��/commbuf 2��/jyzd
    �����0 �� 1 ��
    """
    log.info(jyzd.get("systemsign",""),'%s|%s|���[%s]ִ�п�ʼ',FN(),LN(),FUNC())
    log.info(jyzd.get("systemsign",""),'%s|%s|��commbuf����ת�����ֵ���',FN(),LN())
    xml = getxml(jyzd.commbuf)
    xml = changeCode(xml,'UTF-8')
    resp_dict = Xml2Json(xml).result
    log.info(jyzd.get("systemsign",""),'%s|%s|ת������ֵ�resp_dict=%s',FN(),LN(),str(resp_dict))
    jyzd["REQ"] = resp_dict
    log.info(jyzd.get("systemsign",""),'%s|%s|���[%s]ִ�н���',FN(),LN(),FUNC())
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
    log.info(jyzd.get("systemsign",""),'%s|%s|���[%s]ִ�п�ʼ',FN(),LN(),FUNC())
    subflow = ass( jyzd.input.get('_1') , jyzd )
    print 'ִ��ָ����������[%s]'%subflow
    log.info(jyzd.get("systemsign",""),'ִ��[%s]'%subflow)
    TRAC_DICTTree(jyzd )
    log.info(jyzd.get("systemsign",""), 'jyzd[%s]'%( type(jyzd)))
    ret = flow.flow_utils.goflow("../flow/%s.flow"%subflow,jyzd)
    log.info(jyzd.get("systemsign",""),'%s|%s|���[%s]ִ�н���',FN(),LN(),FUNC())
    return ret
    
