# -*- coding:utf-8 -*-
from  xml.dom import  minidom
import codecs

def getTagText(root, tag):
    """
    ���ڼ򵥵�Ԫ�أ��磺<caption>Python</caption>�����ǿ��Ա�д����һ���������õ��������ݣ�����ΪPython����
    """
    node = root.getElementsByTagName(tag)[0]
    rc = ""
    for node in node.childNodes:
        if node.nodeType in ( node.TEXT_NODE, node.CDATA_SECTION_NODE):
            rc = rc + node.data
    return rc

def changeDict(root , nodeName , jyzd ={}):
    """
    ��xmlת��Ϊ�ֵ����ʽ����ǩ��Ϊ��ֵ
    ����˵����
    root:xml����
    jyzd�����ɽ����ŵ��ֵ�
    nodeName���ڵ�ֵ���˽ڵ���ȫ��ת��Ϊ�ֵ�
    """
    node = root.getElementsByTagName(nodeName)[0]
    for nod in node.childNodes:
        #s_xml = unicode(s_xml,"gb2312").encode("utf-8")
        if nod.nodeType == nod.ELEMENT_NODE:
            jyzd[str(nod.nodeName)] = str(getTagText(root, nod.nodeName).encode("gb2312"))
    return jyzd
    

def makeEasyTag(dom, tagname, value, type='text'):
    """  
    ��������д��һ��С���������ڼ򵥵����������ڣ�
    <caption>test</caption>
    ����˵����
    	domΪdom����
    	tagnameΪҪ����Ԫ�ص����֣���'item'
    	valueΪ���ı����ݣ�����Ϊ����
    	typeΪ�ı����ĸ�ʽ��'text'Ϊһ��Text��㣬'cdata'ΪCDATA���
    ��������˵����
    	���ȴ���Ԫ�ؽ��
    	�����ı������Ƿ���']]>'������ҵ�������ı����ֻ������Text���
    	����������Ϊ'text'������ı������е�'<'�滻Ϊ'&lt;'��'&'�滻Ϊ'&amp;'���������ı����
    	����������Ϊ'cdata'��������CDATA���
    	�����ɵ��ı����׷�ӵ�Ԫ�ؽ����
    ������С���������Զ��ش����ַ�ת��������CDATA����г���']]>'����
    """
    tag = dom.createElement(tagname)
    if value.find(']]>') > -1:
        type = 'text'
    if type == 'text':
        value = value.replace('&', '&amp;')
        value = value.replace('<', '&lt;')
        text = dom.createTextNode(value)
        tag.appendChild(text)
    elif type == 'cdata':
        text = dom.createCDATASection(value)
        tag.appendChild(text)
    return tag

def xmlraplace(node , TagName1 , TagName , text):
    """
    �滻xml�б�ǩ��ֵ
    ����˵����
    node��xml��Ͳ�ڵ����
    TagName:���滻��ǩ��
    text:��ֵ
    """
    #��ȡxml��ʽ��������
    s_xml = """<?xml version="1.0" encoding="UTF-8" ?>
    <users>
        <user id="1000001">
            <username>Admin</username>
            <email>admin@live.cn</email>
            <age>23</age>
            <sex>12134</sex>
        </user>
    </users>"""
    #xmlDom = minidom.parseString(s_xml)
#    node = xmlDom.documentElement
    root = node.getElementsByTagName(TagName1)[0]
    tmp = root.getElementsByTagName(TagName)[0]
    root.removeChild(tmp)
    #����/ɾ���ڵ�
    ####node = xmlDom.createElement('node')
    ####root.removeChild(node)
    text = unicode(text, 'cp936')
    import xml.dom.minidom
    impl = xml.dom.minidom.getDOMImplementation()
    dom = impl.createDocument(None, 'catalog', None)
    item = makeEasyTag(dom, TagName, text)
    root.appendChild(item)
    
    #print root.toxml(),'iiiiii'
    return node

def fun1(content ,tag ,text ):
    """ 
    �滻xml�б�ǩ���������³���xml�б�
    """
    i = 0
    f = 0
    l = []
    k = 1
    for line in content:
        tl = '<' + tag + '>'
        tr = '</' + tag + '>'
        if tl in line and tr in line and k:
            s = tl + text + tr + '\n'
#            tmp1 = unicode(s,"gb2312").encode("utf-8")
#            tmp1 = unicode(s,"gb2312").encode("GB18030")
            l.append(s)
#            content[i] = tmp1
#            f = 1
        elif tl in line and k:
            k = 0
        elif tr in line and not k:
            s = tl + text + tr + '\n'
            l.append(s)
            k = 1
        elif k:
            l.append(line)
        i = i + 1
    return l
