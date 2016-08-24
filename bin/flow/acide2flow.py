#coding:utf-8
from conf import settings
import copy
from mako.template import Template
settings.register( 'oaconf' )
#��ѯ�������
#resname ��Դ���� resclass ��Դ���� compcname ��Դ���� compfuncname ��Դ�������� compfile ���뺯�� sourcefile Դ�ļ�·��
sql = """select * from trc_compcfg where resname = 'TRAC_Commbuf'"""
#��ѯ�������output
#compstatus �ڵ�״̬ snote ˵��
sql = """select * from trc_compstatreg where resname = 'TRAC_Commbuf'"""
#��ѯ�������input
#parasn �������˳�� resclass ��Դ���� dftcont Ĭ������  
sql = """select * from trc_compparareg where resname = 'TRAC_Commbuf'"""
#���̰��������
sql = """select * from trc_flowcfg where resname = 'mainflow_bankxpay'"""
#��ѯ�����������
#resversn �ڵ����� flowsn ����ڵ��� parasn �������˳�� paracont ��������  resclass �������ͣ��ַ��������̣� snote ����˵��
sql = """select * from trc_fcompparacfg where resname = 'mainflow_bankxpay'"""
sql = """select * from trc_fcompparacfg where resname ='sys_guocai' and flowsn ='0'"""
#��ѯ���̽ڵ���ϵ
#flowsn �ڵ��� compstatus �ڵ�״̬ nextflowsn ��Ӧ״̬�µ���һ�ڵ� snote �ڵ�״̬˵��
sql = """select * from trc_fcompstatcfg where resname = 'mainflow_bankxpay'"""
#��ѯ��������
#select * from trc_appresreg where resname = 'sys_guocai'

#xml��������
#esname ��Դ���� resclass ��Դ����
sql = """select * from trc_xmlpcfg where resname = 'BQRes'"""
tmpl = Template( """#coding: gbk
<?xml version="1.0" encoding="GB2312"?>
<flow description="${ desc.encode( 'gbk' ) if type(desc) == unicode else desc }">
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
   <node desc="${ n['desc'].encode( 'gbk' ) if type(desc) == unicode else n['desc'] }" g="${ ( x,y,w,h ) }" nodeid="${ n['id'] }" identifier="${ n['id'] }">
    % if n['type'] == 'py':
      <function filename="libpynode.so" functionname="CallPython" type="so" >
         <input>
            <arg name="" origin="allparam" value="" />
        % for k,v in n['input'].items():
            <arg name="${ k }" origin="literal" value="${ v.encode( 'gbk' ) if type(desc) == unicode else v }" />
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
            <arg name="${ k }" origin="literal" value="${ v.encode( 'gbk' ) if type(desc) == unicode else v }" />
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
            default_dict( n , py_default )
            # ����py�ڵ㣬��δ�趨funcname�����Զ����ID
            #if not n['input'].get( 'FUNCNAME' ):
            resname =  n.get('idname','null')
            print resname
            FUNCNAME = getNamefromTable('trc_compcfg','COMPFUNCNAME',resname = resname)
            if FUNCNAME == 'null':
                FUNCNAME = 'pub_error' if resname == 'null' else n.get('idname','null')
            n['input']['FUNCNAME'] = FUNCNAME
            #if not n['input'].get( 'MODNAME' ):
            MODNAME = getNamefromTable('trc_compcfg','COMPFILE',resname = resname) 
            if MODNAME == 'null':
                MODNAME = 'guocai_txj'
            elif MODNAME[-3:] == '.py':
                MODNAME = MODNAME[:-3]
            elif MODNAME[-3:] == '.so':
                MODNAME = 'guocai_txj'
            n['input']['MODNAME'] = MODNAME
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
        desc = getNamefromTable('trc_appresreg','rescname',resname = filen)
        p = {'py_default': {'rets': {0: 'end'}, 'input': {'MODNAME': ''}}, 'desc':desc ,'start': '-300'}
        #nods = [] 
        nods = getnods_list(filen)
        #nods.append({'rets': {0: 'end', 1: 'end'}, 'type': 'py', 'id': 'pub_error', 'rank': 800, 'desc': '�쳣��������'})
        nods.append({'rets': {0: 'end', 1: 'end'}, 'type': 'py', 'id': '-8888', 'rank': 800, 'desc': '�쳣��������'})
        p['nods'] = nods
        f = open('acide_before_p1.txt','w')
        f.write(str(p))
        f.close()
        p = preprocess( p )
        f = open('acide_after_p1.txt','w')
        f.write(str(p))
        f.close()
        xml = tmpl.render( **p )
        fn = filen.rsplit( '.' , 1 )[0]
        open( fn + '.flow' , 'w' ).write( xml )

def getCompNamefromTrc_Flowcfg(resname,flowsn):
    session = settings.DB_SESSION()
    compname = session.execute( """select COMPNAME from trc_flowcfg where resname = '%s' and flowsn = %d"""%(resname,flowsn)).fetchone()
    if compname:
        return compname[0].strip()
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

def getnods_list(resname):
    session = settings.DB_SESSION()
    jd_list = session.execute( """select * from trc_flowcfg where resname = '%s'"""%resname)
    rest = []
    for jd in jd_list:
        d_tmp = {}
        d_tmp_rets = {}
        d_tmp['rank'] = 999
        d_tmp['idname'] = jd.compname.strip()
        d_tmp['id'] = jd.flowsn
        d_tmp['type'] = 'py'
        d_tmp['desc'] =  jd.snote.strip() if jd.snote else jd.snote
        input_list = getNameListfromTable('trc_fcompparacfg','paracont','parasn',resname = resname,flowsn = jd.flowsn)
        if len(input_list) >1:
            d_tmp['input'] = {}
        for para in input_list:
            d_tmp['input']['_%d'%para[1]] = para[0].strip() if para[0] else para[0]
        h = session.execute( """select * from trc_fcompstatcfg where resname = '%s' and flowsn = %d"""%(resname,jd.flowsn)  )
        h = h.fetchall()
        for i in h:
            print jd.compname.strip()
            if jd.compname.strip() == 'END':
                d_tmp_rets['0'] = 'end'
            #d_tmp_rets[i.compstatus] = getCompNamefromTrc_Flowcfg(resname,i.nextflowsn)
            d_tmp_rets[i.compstatus] = i.nextflowsn
        d_tmp['rets'] = d_tmp_rets
        rest.append(d_tmp)
    return rest
main( ["sys_guocai"] )
main( ["subflow_sys_guocai_local2remote"] )
main( ["subflow_sys_guocai_remote2local"] )
########################################## �����ֵ䵽xml����ת�� #################################################
def deepdict(fnodename,root,key,value):
    cmd = "root"
    for i in fnodename.split('/')[1:]:
        cmd = cmd + ".setdefault('%s',{})"%i
    if value == None:
        exec('%s["%s"]={}'%(cmd,key))
    else:
        exec('%s["%s"]="%s"'%(cmd,key,value))
    return root
def createxmlp(resname):
    session = settings.DB_SESSION()
    conut = session.execute( """select count(1) from trc_xmlpcfg where resname = '%s'"""%resname).fetchone()
    root = {}
    for i in range(int(conut[0])):
        h = session.execute( """select trim(nodename),trim(nodetype),trim(fnodename),trim(inodexp) from trc_xmlpcfg where resname = '%s' and fldsn ='%d' """%(resname,i))
        h = h.fetchone()
        nodename,nodetype,fnodename,inodexp = h
        if fnodename and nodetype != '1':
            deepdict(fnodename,root,nodename,inodexp)
    open( resname + '.json' , 'w' ).write( str(root).replace("'",'"') )
    return root

print createxmlp('gp_sys_guocai_fail_resp')
#import json
#f = file("BQRes.json");
#s = json.load(f)
#print s
#print s["Cartoon"]
#f.close
########################################## �����ֵ䵽xml����ת�� #################################################
#if __name__ == '__main__':
#    import sys
#    fn = sys.argv[-1]
#    if fn.endswith( 'yaml2flow.py' ):
#        print __doc__
#    else:
#        main( sys.argv[-1] )
