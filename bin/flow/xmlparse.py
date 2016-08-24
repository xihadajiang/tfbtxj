 # coding: gbk
from xml.etree import ElementTree as et
from xml.dom import minidom
import re
import copy
from shangjie.utils.ftools import AttrDict , register

xml_encoding = re.compile( '\<\?.*\?\>' )
xml_parser_err = re.compile('.*?(?P<line>\d+),.*?(?P<col>\d+)')

@register()
def xmlroot( tagname , text=None , attrib={} , encoding='gbk', **kwargs ):
    """
    将传入的内容生成一个ElementTree的根结点，并用encoding进行了解码转换
    传入参数
    tagname 根节点名称
    text 根节点对应的text
    attrib 根节点对应的属性
    encoding 传入内容的编码方式
    kwargs  根节点的补充内容
    """
    if type( tagname ) == str:
        tagname = tagname.decode( encoding )
    
    d = {}
    for k, v in attrib.items():
        if type( k ) == str:
            k = k.decode( encoding )
        if type( v ) == str:
            v = v.decode( encoding )
        elif v is None:
            v = ''
        elif type( v ) != unicode:
            v = str( v )
        d[ k ] = v
    
    for k, v in kwargs.items():
        if type( v ) == str:
            v = v.decode( encoding )
        elif v is None:
            v = ''
        elif type( v ) != unicode:
            v = str( v )
        d[ k ] = v
    
    e = et.Element( tagname , d )
    if text:
        if type( text ) == str:
            text = text.decode( encoding )
        e.text = text
    return e

@register()
def xmlappend( parent, tagname, text=None, attrib={}, encoding='gbk', **kwargs ):
    """
    将传入的内容生成一个ElementTree的结点，并作为parent的子节点，用encoding进行了解码转换
    传入参数
    parent 父节点名称
    tagname 子树根节点名称
    text 根节点对应的text
    attrib 根节点对应的属性
    encoding 传入内容的编码方式
    kwargs  根节点的补充内容
    """
    if type( tagname ) == str:
        tagname = tagname.decode( encoding )
    
    d = {}
    for k, v in attrib.items():
        if type( k ) == str:
            k = k.decode( encoding )
        if type( v ) == str:
            v = v.decode( encoding )
        elif v is None:
            v = ''
        elif type( v ) != unicode:
            v = str( v )
        d[ k ] = v
    
    for k, v in kwargs.items():
        if type( v ) == str:
            v = v.decode( encoding )
        elif v is None:
            v = ''
        elif type( v ) != unicode:
            v = str( v )
        d[ k ] = v
    
    e = et.SubElement( parent, tagname, d )
    if text:
        if type( text ) == str:
            text = text.decode( encoding )
        e.text = text
    return e

@register()
def xmlout( ele , encoding = 'gbk' , with_header = True , pretty = False ):
    """
    将ElementTree对象转换成xml报文输出
    参数列表
    ele ElementTree对象
    encoding 编码格式
    with_header 是否要加文件头（<?xml version='1.0' encoding='%s'?>\n）
    pretty 是否以xml的形式展现，否的话是一行输出没有xml的缩进等
    """
    s = et.tostring( ele , 'utf-8' )
    if pretty:
        reparsed = minidom.parseString( s )
        return reparsed.toprettyxml( indent="    " , encoding = encoding )
        
    ret = s.split( '\n' , 1 )[-1]
    
    if encoding != 'utf-8':
        ret = ret.decode( 'utf-8' ).encode( encoding )
    
    if with_header:
        return "<?xml version='1.0' encoding='%s'?>\n" % encoding + ret
    else:
        return ret

from xml.parsers.expat import ExpatError

@register()
def xml( buf , encoding = 'gbk' ):
    """读取xml报文，并返回根的elementtree对象
      该函数关注的是报文的编码转换
      参数列表：buf，报文内容
      encoding ：报文的编码格式
    """
    buf = buf.strip().decode( encoding ).encode( 'utf8' )
    g = xml_encoding.match(buf)
    if g:
        encode_old = g.group()
        buf = buf.replace(encode_old,"<?xml version='1.0' encoding='utf-8'?>")
    else:
        buf = "<?xml version='1.0' encoding='utf-8'?>\n" + buf
    try:
        return et.XML( buf )
    except ExpatError , e :
        m = xml_parser_err.match(e.args[0])
        if m:
            errdict = m.groupdict()
            raise  RuntimeError( '报文在第[%s]行第[%s]列出错，请检查此报文:\n%s' % ( errdict['line'], errdict['col'] ,e.args[0] ) )

@register()
def xmlread( e , path , attrs = None , encoding = 'gbk' , shrink = True ):
    """读取指定的相对E节点的路径数据。
    参数列表:
    e 节点
    path 相对e节点的路径
    attrs 为列表或元组
      其中：None表示text
            其他字符串表示属性名称
    返回结果：
      属性内容。当只有一个属性时，仅返回一个值，不返回元组
      另外，当path会找到N个值时，返回所有节点对应的内容
    """ 
    if type( path ) != 'unicode':
        path = path.decode( encoding )
    
    ll = e.findall( path )
    result = []
    for i in ll:
        if attrs is None:
            attrs = ( None , )
        if type( attrs ) not in ( list , tuple ):
            attrs = ( attrs , )
        r2 = []
        for a in attrs:
            if a is None:
                # 取Text属性
                r2.append( i.text.encode( encoding ) if i.text else '' )
            else:
                # 取属性
                r2.append( i.attrib.get( a , '' ).encode( encoding ) )
        
        result.append( r2[0] if len( r2 ) == 1 else r2 )
    if result:
        return result[0] if ( len( result ) == 1 and shrink ) else result

#返回所有具有相同标签的子
@register()
def xmlreadobj( e , path , encoding = 'gbk' ):
    if type( path ) != 'unicode':
        path = path.decode( encoding )
    ll = e.findall( path )
    return ll

def pretty_dict(obj, indent=' '):
    def _pretty(obj, indent):
        for i, tup in enumerate(obj.items()):
            k, v = tup
            #如果是字符串则拼上""
            if isinstance(k, basestring): k = '"%s"'% k
            if isinstance(v, basestring): v = '"%s"'% v
            #如果是字典则递归
            if isinstance(v, dict):
                print indent,len(indent)
                #v = ''.join(_pretty(v, indent + ' '* len(str(k) + ': {')))#计算下一层的indent
                v = ''.join(_pretty(v, indent + ' '* len("1")))#计算下一层的indent
            #case,根据(k,v)对在哪个位置确定拼接什么
            if i == 0:#开头,拼左花括号
                if len(obj) == 1:
                    yield '{%s: %s}'% (k, v)
                else:
                    yield '{%s: %s,\n'% (k, v)
            elif i == len(obj) - 1:#结尾,拼右花括号
                yield '%s%s: %s}'% (indent, k, v)
            else:#中间
                yield '%s%s: %s,\n'% (indent, k, v)
    print ''.join(_pretty(obj, indent))

d = { "root": { "folder2": { "item2": None, "item1": None }, "folder1": { "subfolder1": { "item2": None, "item1": None }, "subfolder2": { "item3": None } } } }
pretty_dict(d)
d1 = {"Tenpay":{
                "Head":{
                    "@":{"ID":"1"},
                    "BQRes":{
                        "code":"22",
                        }
                    },
                "Message":{
                    "@":{"ID":"1"},
                    "BQRes":{
                        "respmsg":"[/pub/respmsg]",
                        "respcode":"111"
                        }
                    }
                }
            }

def xml_dict(obj, indent='root'):
    r = xmlroot( '%s'%indent)
    def _xml(obj, indent ):
        for i, tup in enumerate(obj.items()):
            k, v = tup
            print '0000',i,tup
            #如果是字符串则拼上""
            #if isinstance(k, basestring): print k
            if isinstance(v, basestring): xmlappend( indent , k , text = v )
            #如果是字典则递归
            if isinstance(v, dict):
                if k != '@':
                    att = v.get('@','')
                    if len(att) > 0:
                        indent = xmlappend( indent ,k , attrib = att )
                    else:
                        indent = xmlappend( indent ,k )
                    #case,根据(k,v)对在哪个位置确定拼接什么
                    if i == 0:#开头,拼左花括号
                        if len(obj) == 1:
                            yield '{%s: %s}'% (k, v)
                        else:
                            yield '{%s: %s,\n'% (k, v)
                    elif i == len(obj) - 1:#结尾,拼右花括号
                        yield '%s%s: %s}'% (indent, k, v)
                    else:#中间
                        yield '%s%s: %s,\n'% (indent, k, v)
    _xml(obj, r)
    return xmlout( r , encoding = 'gbk' , pretty = True )
#print type(xml_dict(d)),xml_dict(d)
if __name__ == '__main__':
#    fn = "9999999901020001_9999999912020001_17_810C028E88E835739BAAB694136B35FB.xml" # 文件名称
#    dir = "D:/20100925/" + fn
#    f= open(dir,'r')
#    buf = f.read()
#    buf = buf[buf.find('<'):]
#    root = xml( buf , 'utf8' )
#    print '>>>>>>>>>>>>>>>>>',xmlread(root,'Header/MessageClass'),xmlread(root,'Header/MessageType')
#    print '>>>>>>>>>>>>>>>>>>>>',root.tag ,xmlread(root,'Body','ContentType')
#    ll = xmlreadobj(root,'Body/Transaction')
#    for i in ll:
#        #在此处调用你写的通用函数
#        print i.tag,i.text
#        print xmlread(i,'TransId')

#    buf="""<CFX>
#        <HEAD>
#            <SRC>6001</SRC>
#            <DES>9999</DES>
#            <APP>财税</APP>
#        </HEAD>
#        <MSG>
#            <交易码  val="1104"/>
#            <纳税人编号  val="012345678901234567"/>
#            <税务机构  val="1"/>
#            <发起机构  val="6001"/>
#        </MSG>
#</CFX>
#"""
    buf = """<CFX>
    <HEAD>
        <SRC>9999</SRC>
        <DES>6001</DES>
        <APP>财税</APP>
    </HEAD>
    <MSG>
        <交易码  val="1&lt;101&gt;"/>
        <流水号 val='108002221656000000'/>
        <凭证号码 val='0123456789'/>
        <账务日期 val='2008-06-07'/>
        <所属场次 val="01"/>
        <响应码  val="000"/>
        <响应描述  val="交易成功"/>
    </MSG>
    <MSG>
        <交易码  val="1&lt;101&gt;"/>
        <流水号 val='108002221656000000'/>
        <凭证号码 val='0123456789'/>
        <账务日期 val='2008-06-07'/>
        <所属场次 val="01"/>
        <响应码  val="000"/>
        <响应描述  val="交易成功"/>
    </MSG>
</CFX>"""
#    root = xml( buf , 'gbk' )
#    print xmlread( root , 'MSG/交易码' , 'val' )
#    r = xmlroot( 'Message ' , TYPE = 'REQUEST' )
#    h = xmlappend( r , 'HEAD' )
#    xmlappend( h , 'TRAN_CODE' , text = '10' )
#    xmlappend( h , 'USER' , text = 'test_user' )
#    xmlappend( h , 'PASSWORD' , text = 'user321' )
#    body = xmlappend( r , 'BODY' )
#    base = xmlappend( body , 'BASE' )
#    xmlappend( base , 'BANK_CODE' , text = '00000001' )
#    xmlappend( base , 'INSURE_ID' , text = '00000001' )
#    xmlappend( base , 'MIDNO' , text = '120000000000001' )
#    xmlappend( base , 'TIDNO' , text = '00000001' )
#    xmlappend( base , 'BK_ACCT_DATE' , text='20080312' )
#    xmlappend( base , 'BK_ACCT_TIME' , text='162710' )
#    xmlappend( base , '中文' , text='000000000000000001' )
#    xmlappend( base , 'BK_TRAN_CHNL' , text='POS' )
#    xmlappend( base , 'PAY_APP_NO' , text='010800000001' )
#    xmlappend( base , 'CHECKCODE' , text='1234' )
#
    r = xmlroot( 'Message '  )
    h = xmlappend( r , 'Header' )
    b = xmlappend( r , 'Body',attrib={'ContentType':'1'}  )
    xmlappend( h , 'MessageClass' , text = '10' )
    xmlappend( h , 'MessageType' , text = 'test_user' )
    xmlappend( b , 'MessageId' , text = 'MessageId' )
    xmlappend( b , 'ProcessTime' , text = 'MessageId' )
    xmlappend( b , 'Result' , text = '' )
#    print xmlout( r , encoding = 'gbk' , pretty = True )
    
    xml_dict = {"/Tenpay":{
                    "/Message":{
                        "/Message/BQRes":{
                            "/Message/BQRes/respmsg":"[/pub/respmsg]",
                            "/Message/BQRes/respcode":"111"
                            }
                        }
                    }
                }
#    for k,v in xml_dict.items():
#        print k,v
        
