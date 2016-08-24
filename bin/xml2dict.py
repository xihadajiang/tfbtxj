#coding:utf-8
#! /usr/bin/env python
# -*- coding:utf-8 -*-

from xml.parsers.expat import ParserCreate
try:
    import json
except:
    import simplejson as json
#def changeDict(root , nodeName , jyzd ={}):
#    """
#    将xml转换为字典的形式，标签作为键值
#    参数说明：
#    root:xml对象
#    jyzd：生成结果存放的字典
#    nodeName：节点值，此节点下全部转换为字典
#    """
#    node = root.getElementsByTagName(nodeName)[0]
#    for nod in node.childNodes:
#        #s_xml = unicode(s_xml,"gb2312").encode("utf-8")
#        if nod.nodeType == nod.ELEMENT_NODE:
#            jyzd[str(nod.nodeName)] = str(getTagText(root, nod.nodeName).encode("gb2312"))
#    return jyzd

class Xml2Json:
    LIST_TAGS = ['COMMANDS']

    def __init__(self, data = None):
        self._parser = ParserCreate()
        self._parser.StartElementHandler = self.start
        self._parser.EndElementHandler = self.end
        self._parser.CharacterDataHandler = self.data
        self.result = None
        if data:
            self.feed(data)
            self.close()

    def feed(self, data):
        self._stack = []
        self._data = ''
        self._parser.Parse(data, 0)

    def close(self):
        self._parser.Parse("", 1)
        del self._parser

    def start(self, tag, attrs):
        assert attrs == {}
        print self._data.strip(),'--------'
        #assert self._data.strip() == ''
        self._stack.append([tag])
        self._data = ''

    def end(self, tag):
        last_tag = self._stack.pop()
        assert last_tag[0] == tag
        if len(last_tag) == 1: #leaf
            data = self._data
        else:
            if tag not in Xml2Json.LIST_TAGS:
                # build a dict, repeating pairs get pushed into lists
                data = {}
                for k, v in last_tag[1:]:
                    if k not in data:
                        data[k] = v
                    else:
                        el = data[k]
                        if type(el) is not list:
                            data[k] = [el, v]
                        else:
                            el.append(v)
            else: #force into a list
                data = [{k:v} for k, v in last_tag[1:]]
        if self._stack:
            self._stack[-1].append((tag, data))
        else:
            self.result = {tag:data}
            self._data = ''

    def data(self, data):
        self._data = data

if __name__ == '__main__':
    xml = """<?xml version="1.0" encoding="utf-8"?>
<student>
<stid>10213</stid>
<info>
<name>name</name>
<mail>xxx@xxx.com</mail>
<sex>male</sex>
</info>
<course>
<name>math</name>
<age>90</age>
</course>
<course>
<name>english</name>
<age>88</age>
</course>
</student>
"""
    xml = """<?xml version="1.0" encoding="utf-8"?>
<root>
 <person>
    <name>2</name>
    <sex>3</sex>
 </person>
 <person>
    <name>5</name>
    <sex>6</sex>
 </person>
</root>
"""
    xml = """<?xml version='1.0' encoding="utf-8"?><root><ver>1.0</ver><spid>11111</spid><spbillno>222222</spbillno><business_type>14900</business_type><business_no>444444</business_no><tran_amt>10000</tran_amt><cur_type></cur_type><true_name>11111</true_name><mobile></mobile><cre_id></cre_id><cre_type></cre_type><card_id>622384609891538799</card_id><card_type></card_type><bank_name>10000</bank_name><bank_ins_code>26520300</bank_ins_code><card_prov></card_prov><purpose></purpose><postscript></postscript><md5_sign></md5_sign><TransCode>api_acp_single.cgi</TransCode></root>"""

    result = Xml2Json(xml).result;
    print(result)
    print("*" * 80)
    print("*" * 80)
    print(json.dumps(result))



from xml.etree import ElementTree as et;
import json
xml = """<?xml version="1.0" encoding="utf-8"?>
<root>
 <person age="18">
    <name>张三</name>
    <sex>男</sex>
 </person>
 <person age="19" des="您好">
    <name>李四</name>
    <sex>女</sex>
 </person>
</root>
"""
#从xml文件读取结点 转换为json格式，并保存到文件中
#print('read node from xmlfile, transfer them to json, and save into jsonFile:')
#root=et.parse("testXml.xml");
#f=open('testJson.json','a',encoding="utf8");
#for each in root.getiterator("person"):
#    tempDict=each.attrib
#    for childNode in each.getchildren():
#        tempDict[childNode.tag]=childNode.text
#    tempJson=json.dumps(tempDict,ensure_ascii=False)
#    print(tempJson)
#    f.write(tempJson+"\n");
#f.close()
#
##从json文件中读取，并打印
#print('read json from jsonfile:')
#for eachJson in open('testJson.json','r',encoding='utf8'):
#    tempStr=json.loads(eachJson);
#    print(tempStr)
