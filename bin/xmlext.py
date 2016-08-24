# -*- coding:utf-8 -*-
from  xml.dom import  minidom
import codecs

def getTagText(root, tag):
    """
    对于简单的元素，如：<caption>Python</caption>，我们可以编写这样一个函数来得到它的内容（这里为Python）。
    """
    node = root.getElementsByTagName(tag)[0]
    rc = ""
    for node in node.childNodes:
        if node.nodeType in ( node.TEXT_NODE, node.CDATA_SECTION_NODE):
            rc = rc + node.data
    return rc

def changeDict(root , nodeName , jyzd ={}):
    """
    将xml转换为字典的形式，标签作为键值
    参数说明：
    root:xml对象
    jyzd：生成结果存放的字典
    nodeName：节点值，此节点下全部转换为字典
    """
    node = root.getElementsByTagName(nodeName)[0]
    for nod in node.childNodes:
        #s_xml = unicode(s_xml,"gb2312").encode("utf-8")
        if nod.nodeType == nod.ELEMENT_NODE:
            jyzd[str(nod.nodeName)] = str(getTagText(root, nod.nodeName).encode("gb2312"))
    return jyzd
    

def makeEasyTag(dom, tagname, value, type='text'):
    """  
    下面是我写的一个小函数，用于简单的生成类似于：
    <caption>test</caption>
    参数说明：
    	dom为dom对象
    	tagname为要生成元素的名字，如'item'
    	value为其文本内容，可以为多行
    	type为文本结点的格式，'text'为一般Text结点，'cdata'为CDATA结点
    函数处理说明：
    	首先创建元素结点
    	查找文本内容是否有']]>'，如果找到，则此文本结点只可以是Text结点
    	如果结点类型为'text'，则对文本内容中的'<'替换为'&lt;'，'&'替换为'&amp;'，再生成文本结点
    	如果结点类型为'cdata'，则生成CDATA结点
    	将生成的文本结点追加到元素结点上
    因此这个小函数可以自动地处理字符转化及避免CDATA结点中出现']]>'串。
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
    替换xml中标签的值
    参数说明：
    node：xml最低层节点对象
    TagName:被替换标签名
    text:新值
    """
    #读取xml格式的数据流
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
    #创建/删除节点
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
    替换xml中标签内容生成新出的xml列表
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
