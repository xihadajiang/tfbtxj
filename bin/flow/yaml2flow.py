# coding: gbk
"""
�÷���
    yaml2flow.py �ļ���(֧��ͨ�������ֻ��ƥ��һ���ļ�ʱ��ϵͳ�Զ���Ԥ������Ԥ�����ɵ�����ͼ��
˵����
    ���ڽ�yaml�ļ�ת��Ϊflow�Ľű���
    ���̽ű��Ĵ���xml��ǲ������Ķ���ʹ��yaml����ɴ������˹�ά����Ч�ʡ�
YAML����
    desc: ��������
    start: ��ʼ��һ���ڵ�
    py_default:                # py�ڵ��ȱʡ���������ڼ�¥��PY�ڵ����ã�ȱʡ������ֱ�ӻ�ȡ
        input:
            MODNAME: ȱʡ����  # �ṹ���ڵ�ṹ��
        rets:
            -1: pub_error
    c_default:                 # c�ڵ��ȱʡ����
        ...
    flow_default:               # �����̵�ȱʡ����
        ...
    nods:
        - type: py             # py ��Ӧpynode
          desc: �ڵ�����
          id: �ڵ�ID
          rank: ����           # ���֣����ڻ�ͼʱ�Ľڵ�ڷ�λ�ã�ͬ�����ֵĽڵ��ڷŵ�ͬһ�㡣0����ͬstartһ�㣬999����ͬendһ��
          input:
            MODNAME: ģ������  
            FUNCNAME: ģ���ں������� # ������ʡ�ԣ���ʹ�ýڵ�ID
            ������: ����ֵ   
          rets:
            ������: ָ��ڵ�ID
        - type: c              # c��Ӧso��sub��Ӧ������
          desc: �ڵ�����       
          filen: so�ļ���      # ȫ·��
          funcn: ������        # ������
          input:
            allparam:          # ��ʶ����ȫ������
            ������: var        # ��ʶ�������
            ������: ����ֵ     # ���볣��
          output:
            [ allparam , ������ ]
          rets:
            ͬpynode
        - type: flow           # ������
          desc: �ڵ�����
          id: �ڵ�ID
          filen: �������ļ���
          rets:
            ͬ��
    
������yaml�ļ���ʽ�ľ�����
# YAML�ļ���ʼ
desc: ETC�ֹ�����
start: PktMsgUnPack
py_default:
    input:
        MODNAME: tjetc
    rets:
        -1: pub_error
nods:
    - type: c
      rank: 0
      desc: �ۺ�ǰ�ý��
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
      desc: ��������ۺ�ǰ��
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
      desc: ͨ���쳣����
      id: pub_error
      rets:
        0: PktMsgPack
        -1: PktMsgPack
    - type: py
      rank: 0
      desc: ���״����ж�
      id: pub_jycs
      rets:
        0: trans409140_cxdfje
        1: beai_510001
    - type: py
      desc: ��ѯ�渶���
      id: trans409140_cxdfje
      rets:
        0: PktMsgPack
    - type: flow
      id: beai_510001
      desc: BEAI����
      filen: public.510001.flow
      rets:
        0: trans409140_dfjech
        -1: pub_error
    - type: py
      desc: �渶����
      id: trans409140_dfjech
      rets:
        0: PktMsgPack
# YAML�ļ�����
"""

import copy
import yaml
from mako.template import Template

# ������������ͼ
from shangjie.utils import pydot

tmpl = Template( """#coding: gbk
<?xml version="1.0" encoding="GB2312"?>
<flow description="${ desc.encode( 'gbk' ) }">
   <node desc="���̿�ʼ" g="35,10,48,48" nodeid="null" identifier="start">
      <return>
         <next g="-11,-17" value="0" identifier="${ start }"/>
      </return>
   </node>
   <node desc="���̽���" g="35,386,48,48" nodeid="null" identifier="end">
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
    // �ڵ��嵥
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
    // �ڵ��ų���
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
    // ��֯�ڵ��ϵ
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
    """ ����d���ֵ�����,����n��û���趨ֵ���ֵ�����
        d��n�п�����Ƕ�׵��ֵ�
    """
    if type( d ) is not dict:
        return
    # �Ƚ���Ӽ���ȱʡֵ
    for k,v in n.items():
        if type( v ) is dict and k in d:
            default_dict( v , d[k] )
    # �ٽ��ͬ����ȱʡֵ
    n_keys = set( n.keys() )
    d_keys = set( d.keys() )
    diff = d_keys - n_keys
    for k in diff:
        n[k] = copy.deepcopy( d[k] )
    
def preprocess( d ):
    """ ����ȱʡ���ø��½ڵ���Ϣ """
    py_default = d.get( 'py_default' , {} )
    c_default  = d.get( 'c_default' , {} )
    flow_default = d.get( 'flow_default' , {} )
    for n in d['nods']:
        if n['type'] == 'py':
            print '===',n , py_default
            default_dict( n , py_default )
            print '---',n , py_default
            # ����py�ڵ㣬��δ�趨funcname�����Զ����ID
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
        # ��������ͼ
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
    