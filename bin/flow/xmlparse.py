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
    ���������������һ��ElementTree�ĸ���㣬����encoding�����˽���ת��
    �������
    tagname ���ڵ�����
    text ���ڵ��Ӧ��text
    attrib ���ڵ��Ӧ������
    encoding �������ݵı��뷽ʽ
    kwargs  ���ڵ�Ĳ�������
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
    ���������������һ��ElementTree�Ľ�㣬����Ϊparent���ӽڵ㣬��encoding�����˽���ת��
    �������
    parent ���ڵ�����
    tagname �������ڵ�����
    text ���ڵ��Ӧ��text
    attrib ���ڵ��Ӧ������
    encoding �������ݵı��뷽ʽ
    kwargs  ���ڵ�Ĳ�������
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
    ��ElementTree����ת����xml�������
    �����б�
    ele ElementTree����
    encoding �����ʽ
    with_header �Ƿ�Ҫ���ļ�ͷ��<?xml version='1.0' encoding='%s'?>\n��
    pretty �Ƿ���xml����ʽչ�֣���Ļ���һ�����û��xml��������
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
    """��ȡxml���ģ������ظ���elementtree����
      �ú�����ע���Ǳ��ĵı���ת��
      �����б�buf����������
      encoding �����ĵı����ʽ
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
            raise  RuntimeError( '�����ڵ�[%s]�е�[%s]�г�������˱���:\n%s' % ( errdict['line'], errdict['col'] ,e.args[0] ) )

@register()
def xmlread( e , path , attrs = None , encoding = 'gbk' , shrink = True ):
    """��ȡָ�������E�ڵ��·�����ݡ�
    �����б�:
    e �ڵ�
    path ���e�ڵ��·��
    attrs Ϊ�б��Ԫ��
      ���У�None��ʾtext
            �����ַ�����ʾ��������
    ���ؽ����
      �������ݡ���ֻ��һ������ʱ��������һ��ֵ��������Ԫ��
      ���⣬��path���ҵ�N��ֵʱ���������нڵ��Ӧ������
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
                # ȡText����
                r2.append( i.text.encode( encoding ) if i.text else '' )
            else:
                # ȡ����
                r2.append( i.attrib.get( a , '' ).encode( encoding ) )
        
        result.append( r2[0] if len( r2 ) == 1 else r2 )
    if result:
        return result[0] if ( len( result ) == 1 and shrink ) else result

#�������о�����ͬ��ǩ����
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
            #������ַ�����ƴ��""
            if isinstance(k, basestring): k = '"%s"'% k
            if isinstance(v, basestring): v = '"%s"'% v
            #������ֵ���ݹ�
            if isinstance(v, dict):
                print indent,len(indent)
                #v = ''.join(_pretty(v, indent + ' '* len(str(k) + ': {')))#������һ���indent
                v = ''.join(_pretty(v, indent + ' '* len("1")))#������һ���indent
            #case,����(k,v)�����ĸ�λ��ȷ��ƴ��ʲô
            if i == 0:#��ͷ,ƴ������
                if len(obj) == 1:
                    yield '{%s: %s}'% (k, v)
                else:
                    yield '{%s: %s,\n'% (k, v)
            elif i == len(obj) - 1:#��β,ƴ�һ�����
                yield '%s%s: %s}'% (indent, k, v)
            else:#�м�
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
            #������ַ�����ƴ��""
            #if isinstance(k, basestring): print k
            if isinstance(v, basestring): xmlappend( indent , k , text = v )
            #������ֵ���ݹ�
            if isinstance(v, dict):
                if k != '@':
                    att = v.get('@','')
                    if len(att) > 0:
                        indent = xmlappend( indent ,k , attrib = att )
                    else:
                        indent = xmlappend( indent ,k )
                    #case,����(k,v)�����ĸ�λ��ȷ��ƴ��ʲô
                    if i == 0:#��ͷ,ƴ������
                        if len(obj) == 1:
                            yield '{%s: %s}'% (k, v)
                        else:
                            yield '{%s: %s,\n'% (k, v)
                    elif i == len(obj) - 1:#��β,ƴ�һ�����
                        yield '%s%s: %s}'% (indent, k, v)
                    else:#�м�
                        yield '%s%s: %s,\n'% (indent, k, v)
    _xml(obj, r)
    return xmlout( r , encoding = 'gbk' , pretty = True )
#print type(xml_dict(d)),xml_dict(d)
if __name__ == '__main__':
#    fn = "9999999901020001_9999999912020001_17_810C028E88E835739BAAB694136B35FB.xml" # �ļ�����
#    dir = "D:/20100925/" + fn
#    f= open(dir,'r')
#    buf = f.read()
#    buf = buf[buf.find('<'):]
#    root = xml( buf , 'utf8' )
#    print '>>>>>>>>>>>>>>>>>',xmlread(root,'Header/MessageClass'),xmlread(root,'Header/MessageType')
#    print '>>>>>>>>>>>>>>>>>>>>',root.tag ,xmlread(root,'Body','ContentType')
#    ll = xmlreadobj(root,'Body/Transaction')
#    for i in ll:
#        #�ڴ˴�������д��ͨ�ú���
#        print i.tag,i.text
#        print xmlread(i,'TransId')

#    buf="""<CFX>
#        <HEAD>
#            <SRC>6001</SRC>
#            <DES>9999</DES>
#            <APP>��˰</APP>
#        </HEAD>
#        <MSG>
#            <������  val="1104"/>
#            <��˰�˱��  val="012345678901234567"/>
#            <˰�����  val="1"/>
#            <�������  val="6001"/>
#        </MSG>
#</CFX>
#"""
    buf = """<CFX>
    <HEAD>
        <SRC>9999</SRC>
        <DES>6001</DES>
        <APP>��˰</APP>
    </HEAD>
    <MSG>
        <������  val="1&lt;101&gt;"/>
        <��ˮ�� val='108002221656000000'/>
        <ƾ֤���� val='0123456789'/>
        <�������� val='2008-06-07'/>
        <�������� val="01"/>
        <��Ӧ��  val="000"/>
        <��Ӧ����  val="���׳ɹ�"/>
    </MSG>
    <MSG>
        <������  val="1&lt;101&gt;"/>
        <��ˮ�� val='108002221656000000'/>
        <ƾ֤���� val='0123456789'/>
        <�������� val='2008-06-07'/>
        <�������� val="01"/>
        <��Ӧ��  val="000"/>
        <��Ӧ����  val="���׳ɹ�"/>
    </MSG>
</CFX>"""
#    root = xml( buf , 'gbk' )
#    print xmlread( root , 'MSG/������' , 'val' )
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
#    xmlappend( base , '����' , text='000000000000000001' )
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
        
