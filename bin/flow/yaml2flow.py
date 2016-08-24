# coding: gbk
"""
用法：
    yaml2flow.py 文件名(支持通配符，当只能匹配一个文件时，系统自动打开预览工具预览生成的流程图）
说明：
    用于将yaml文件转换为flow的脚本。
    流程脚本的大量xml标记不利于阅读，使用yaml，则可大大提高人工维护的效率。
YAML规则：
    desc: 交易描述
    start: 开始第一个节点
    py_default:                # py节点的缺省参数，用于简化楼下PY节点配置，缺省参数会直接获取
        input:
            MODNAME: 缺省数据  # 结构按节点结构来
        rets:
            -1: pub_error
    c_default:                 # c节点的缺省参数
        ...
    flow_default:               # 子流程的缺省参数
        ...
    nods:
        - type: py             # py 对应pynode
          desc: 节点名称
          id: 节点ID
          rank: 级别           # 数字，用于绘图时的节点摆放位置，同样数字的节点会摆放到同一层。0代表同start一层，999代表同end一层
          input:
            MODNAME: 模块名称  
            FUNCNAME: 模块内函数名称 # 若该项省略，则使用节点ID
            参数名: 参数值   
          rets:
            返回码: 指向节点ID
        - type: c              # c对应so，sub对应子流程
          desc: 节点描述       
          filen: so文件名      # 全路径
          funcn: 函数名        # 函数名
          input:
            allparam:          # 标识传入全部数据
            参数名: var        # 标识传入变量
            参数名: 参数值     # 传入常量
          output:
            [ allparam , 参数名 ]
          rets:
            同pynode
        - type: flow           # 子流程
          desc: 节点名称
          id: 节点ID
          filen: 子流程文件名
          rets:
            同上
    
下面是yaml文件格式的举例：
# YAML文件开始
desc: ETC手工垫款偿付
start: PktMsgUnPack
py_default:
    input:
        MODNAME: tjetc
    rets:
        -1: pub_error
nods:
    - type: c
      rank: 0
      desc: 综合前置解包
      id: PktMsgUnPack
      filen: libsyspacknode.so
      funcn: PktMsgUnPack
      input: 
        JYBM: var
        MBLYBS: var
        JSDDBW: var
        JSDDBWDZD: var
      output:
        allparam: 
      rets:
        0: pub_jycs
        -1: PktMsgPack
    - type: c
      rank: 999
      desc: 组包返回综合前置
      id: PktMsgPack
      filen: libsyspacknode.so
      funcn: PktMsgPack
      input:
        allparam:
      output:
        YFSDBWDZD: var
        YFSDBW: var
      rets:
        0: end
        -1: end
    - type: py
      desc: 通用异常处理
      id: pub_error
      rets:
        0: PktMsgPack
        -1: PktMsgPack
    - type: py
      rank: 0
      desc: 交易次数判断
      id: pub_jycs
      rets:
        0: trans409140_cxdfje
        1: beai_510001
    - type: py
      desc: 查询垫付金额
      id: trans409140_cxdfje
      rets:
        0: PktMsgPack
    - type: flow
      id: beai_510001
      desc: BEAI记账
      filen: public.510001.flow
      rets:
        0: trans409140_dfjech
        -1: pub_error
    - type: py
      desc: 垫付金额偿还
      id: trans409140_dfjech
      rets:
        0: PktMsgPack
# YAML文件结束
"""

import copy
import yaml
from mako.template import Template

# 用于生成流程图
from shangjie.utils import pydot

tmpl = Template( """#coding: gbk
<?xml version="1.0" encoding="GB2312"?>
<flow description="${ desc.encode( 'gbk' ) }">
   <node desc="流程开始" g="35,10,48,48" nodeid="null" identifier="start">
      <return>
         <next g="-11,-17" value="0" identifier="${ start }"/>
      </return>
   </node>
   <node desc="流程结束" g="35,386,48,48" nodeid="null" identifier="end">
      <return/>
   </node>\
<% x,y,w,h,step = 340 , 10 , 92 , 52 , 70 %>
% for n in nods:
   <node desc="${ n['desc'].encode( 'gbk' ) }" g="${ ( x,y,w,h ) }" nodeid="${ n['id'] }" identifier="${ n['id'] }">
    % if n['type'] == 'py':
      <function filename="libpynode.so" functionname="CallPython" type="so" >
         <input>
            <arg name="" origin="allparam" value="" />
        % for k,v in n['input'].items():
            <arg name="${ k }" origin="literal" value="${ v.encode( 'gbk' ) if v else '' }" />
        % endfor
         </input>
         <output>
            <arg name="" origin="allparam" value="" />
         </output>
      </function>
    % elif n['type'] == 'c':
      <function filename="${ n['filen'] }" functionname="${ n['funcn'] }" type="so" >
         <input>
        % for k,v in n.get( 'input' , {} ).items():
            % if k == 'allparam':
            <arg name="" origin="allparam" value="" />
            % elif v == 'var':
            <arg name="${ k }" origin="variable" value="" />
            % else:
            <arg name="${ k }" origin="literal" value="${ v.encode( 'gbk' ) if v else '' }" />
            % endif
        % endfor
         </input>
         <output>
        % for k in n.get( 'output' , [] ):
            % if k == 'allparam':
            <arg name="" origin="allparam" value="" />
            % else:
            <arg name="${ k }" origin="variable" value="" />
            % endif
        % endfor
         </output>
      </function>
    % else:
      <function filename="${ n['filen'] }" functionname="${ n['filen'] }" type="flow" >
         <input>
            <arg name="" origin="allparam" value="" />
         </input>
         <output>
            <arg name="" origin="allparam" value="" />
         </output>
      </function>
    % endif
      <return>
    % for k,v in n['rets'].items():
         <next g="6,-16" value="${ k }" identifier="${ v }"/>
    % endfor
      </return>
   </node>\
<% y+= step %>
% endfor
</flow>
""" , disable_unicode = True )

dot_tmpl = Template( """#coding: gbk
digraph G {
    edge [fontname=".\YaHei.Consolas.1.12.ttf" , fontsize = 10 ];
    node [fontname=".\YaHei.Consolas.1.12.ttf" , fontsize = 10 ];
    // 节点清单
    start [ shape = circle , color = green , style = filled , size = 10 ];
    end   [ shape = doublecircle , color = red , style = filled ] ;
% for n in nods:
    % if n['type'] == 'py':
    ${ n['id'].replace( '.' , '_' ) } [ label = "${ n['desc' ].encode( 'utf8' ) }"  ] ;
    % elif n['type'] == 'c':
    ${ n['id'].replace( '.' , '_' ) } [ color = blue , label = "${ n['desc' ].encode( 'utf8' ) }"  ] ;
    % else:
    ${ n['id'].replace( '.' , '_' ) } [ shape = octagon , color = darkorange , label = "${ n['desc' ].encode( 'utf8' ) }"  ] ;
    % endif
% endfor
    // 节点排成行
<%
lines = {}
for n in nods:
    if n.get( 'rank' , None ) is not None:
        k = int( n['rank'] )
        line = lines.get( k , [''] )
        line.insert( 0 , n['id'].replace( '.' , '_' ) )
        lines[k] = line
%>
% for k in sorted( lines.keys() ):
    // rank k
    { rank = same; ${ 'start; ' if k == 0 else '' }${ 'end; ' if k == 999 else ''}${';'.join( lines[k] )} };
% endfor
    // 组织节点关系
    start -> ${ start } [ arrowsize = 0.5 ];
% for n in nods:
    % for k,v in n['rets'].items():
    % if v:
    ${ n['id'].replace( '.' , '_' ) } -> ${ v.replace( '.' , '_' ) } [ arrowsize = 0.5 , label = "${k}" ];
    % endif
    % endfor
% endfor
}
""" , disable_unicode = True )

import copy

def default_dict( n , d ):
    """ 根据d的字典内容,更新n中没有设定值的字典内容
        d和n有可能有嵌套的字典
    """
    if type( d ) is not dict:
        return
    # 先解决子级别缺省值
    for k,v in n.items():
        if type( v ) is dict and k in d:
            default_dict( v , d[k] )
    # 再解决同级别缺省值
    n_keys = set( n.keys() )
    d_keys = set( d.keys() )
    diff = d_keys - n_keys
    for k in diff:
        n[k] = copy.deepcopy( d[k] )
    
def preprocess( d ):
    """ 根据缺省配置更新节点信息 """
    py_default = d.get( 'py_default' , {} )
    c_default  = d.get( 'c_default' , {} )
    flow_default = d.get( 'flow_default' , {} )
    for n in d['nods']:
        if n['type'] == 'py':
            print '===',n , py_default
            default_dict( n , py_default )
            print '---',n , py_default
            # 对于py节点，若未设定funcname，则自动填充ID
            if not n['input'].get( 'FUNCNAME' ):
                n['input']['FUNCNAME'] = n['id']
        elif n[ 'type' ] == 'c':
            default_dict( n , c_default )
        else:
            default_dict( n , flow_default )
    return d

import os , glob
def main( filename ):
    filelist = glob.glob( filename )
    for filen in filelist:
        p = yaml.load( open( filen ).read().decode( 'gbk' ) )
        print p
        f = open('before_p.txt','w')
        f.write(str(p))
        f.close()
        p = preprocess( p )
        f = open('after_p.txt','w')
        f.write(str(p))
        f.close()
        print p,type(p)
        xml = tmpl.render( **p )
        fn = filen.rsplit( '.' , 1 )[0]
        open( fn + '.flow' , 'w' ).write( xml )
        # 生成流程图
        s = dot_tmpl.render( **p )
        g = pydot.graph_from_dot_data( s )
        g.write_gif( fn + ".png" )
        if len( filelist ) == 1:
            os.system( "start %s.png" % fn )

if __name__ == '__main__':
    import sys
    fn = sys.argv[-1]
    if fn.endswith( 'yaml2flow.py' ):
        print __doc__
    else:
        main( sys.argv[-1] )
    