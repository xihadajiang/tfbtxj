#coding:utf-8
from conf import settings
import copy
from mako.template import Template
settings.register( 'oaconf' )
#查询组件定义
#resname 资源名称 resclass 资源类型 compcname 资源名称 compfuncname 资源函数名称 compfile 编译函数 sourcefile 源文件路径
sql = """select * from trc_compcfg where resname = 'TRAC_Commbuf'"""
#查询组件定义output
#compstatus 节点状态 snote 说明
sql = """select * from trc_compstatreg where resname = 'TRAC_Commbuf'"""
#查询组件定义input
#parasn 组件参数顺序 resclass 资源类型 dftcont 默认内容  
sql = """select * from trc_compparareg where resname = 'TRAC_Commbuf'"""
#流程包含的组件
sql = """select * from trc_flowcfg where resname = 'mainflow_bankxpay'"""
#查询输入参数定义
#resversn 节点总数 flowsn 组件节点编号 parasn 组件参数顺序 paracont 参数内容  resclass 参数类型（字符还是流程） snote 参数说明
sql = """select * from trc_fcompparacfg where resname = 'mainflow_bankxpay'"""
#查询流程节点间关系
#flowsn 节点编号 compstatus 节点状态 nextflowsn 响应状态下的下一节点 snote 节点状态说明
sql = """select * from trc_fcompstatcfg where resname = 'mainflow_bankxpay'"""
#查询流程描述
#select * from trc_appresreg where resname = 'sys_guocai'
#xml报文配置
#esname 资源名称 resclass 资源类型
sql = """select * from trc_xmlpcfg where resname = 'BQRes'"""
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
    #filelist = glob.glob( filename )
    filelist = filename
    for filen in filelist:
        #p = yaml.load( open( filen ).read().decode( 'gbk' ) )
        p = {'py_default': {'rets': {-1: 'pub_error'}, 'input': {'MODNAME': 'xmhht'}}, 'desc': u'\u7ba1\u7406\u7aef\uff0c\u6839\u636e\u4e0a\u4f20\u7684\u5ba2\u6237\u4fe1\u606f\u8fdb\u884c\u9a8c\u8bc1','start': 'BEGIN'}
        #nods = [] 
        nods = getnods_list(filen)
        p['nods'] = nods
        print p
        f = open('acide_before_p.txt','w')
        f.write(str(p))
        f.close()
        p = preprocess( p )
        print p
        f = open('acide_after_p.txt','w')
        f.write(str(p))
        f.close()
        xml = tmpl.render( **p )
        fn = filen.rsplit( '.' , 1 )[0]
        open( fn + '.flow' , 'w' ).write( xml )

def getnods_list(resname):
    session = settings.DB_SESSION()
    jd_list = session.execute( """select * from trc_flowcfg where resname = '%s'"""%resname)
    rest = []
    for jd in jd_list:
        d_tmp = {}
        d_tmp_rets = {}
        d_tmp['rank'] = 999
        d_tmp['id'] = jd.compname.strip()
        d_tmp['type'] = 'py'
        d_tmp['desc'] =  jd.snote.strip() if jd.snote else jd.snote
        h = session.execute( """select * from trc_fcompstatcfg where resname = '%s' and flowsn = %d"""%(resname,jd.flowsn)  )
        h = h.fetchall()
        for i in h:
            d_tmp_rets[i.compstatus] = i.nextflowsn
        d_tmp['rets'] = d_tmp_rets
        print d_tmp
        rest.append(d_tmp)
    return rest
def getCompNamefromTrc_Flowcfg(resname,flowsn):
    session = settings.DB_SESSION()
    compname = session.execute( """select COMPNAME from trc_flowcfg where resname = '%s' and flowsn = %d"""%(resname,flowsn))
    if compname.fetchone():
        return compname.fetchone()[0].strip()
    else:
        return "pub_error"
def getNamefromTable(table,name,**kwargs):
    where = '1 = 1'
    for k in kwargs:
        if type(kwargs[k]) == int:
            where = where + "and %s=%d"%(k,kwargs[k])
        else:
            where = where + "and %s='%s'"%(k,kwargs[k])
    sql = """select %s from %s where %s"""%(name,table,where)
    session = settings.DB_SESSION()
    compname = session.execute(sql).fetchone()
    if compname:
        return compname[0].strip()
    else:
        return "null"
def getNameListfromTable(table,*args,**kwargs):
    name = ','.join(args)
    where = '1 = 1'
    for k in kwargs:
        if type(kwargs[k]) == int:
            where = where + "and %s=%d"%(k,kwargs[k])
        else:
            where = where + "and %s='%s'"%(k,kwargs[k])
    sql = """select %s from %s where %s"""%(name,table,where)
    session = settings.DB_SESSION()
    compname = session.execute(sql).fetchall()
    if compname:
        return compname
    else:
        return []

input_list = getNameListfromTable('trc_fcompparacfg','paracont','parasn',resname = 'sys_guocai',flowsn = 0)
for para in input_list:
    print para
#print getNamefromTable('trc_flowcfg','COMPNAME',resname = 'sys_guocai',flowsn = 1)
#getNamefromTable('table','a','b','c',a='b',c='d')
#getCompNamefromTrc_Flowcfg('sys_guocai',-8888)
#session = settings.DB_SESSION()
#jd_list = session.execute( """select * from trc_flowcfg where resname = 'sys_guocai'""")
#print jd_list.fetchall()
#for jd in jd_list:
#    print jd
#main( ["sys_guocai"] )
#if __name__ == '__main__':
#    import sys
#    fn = sys.argv[-1]
#    if fn.endswith( 'yaml2flow.py' ):
#        print __doc__
#    else:
#        main( sys.argv[-1] )
