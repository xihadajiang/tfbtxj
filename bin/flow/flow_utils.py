#!/bin/usr/env python
# coding: gbk
# ���̶�ȡ
from xmlparse import *
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

class FlowNode:
    # ���̽ڵ㶨�����
    def __init__( self , obj ):
        self.desc , self._id = xmlread( obj , '' , [ 'desc' , 'identifier' ] )
        ret = xmlread( obj , 'function' , [ 'functionname' , 'filename' , 'type' ] )
        if ret:
            self.functionname , self.filename , self.type = ret
            
        else:
            self.functionname , self.filename , self.type = None , None , None
        if self.filename is None:
            self._type = 'inner'
        elif self.filename == 'libpynode.so':
            self._type = 'py'
            # ����py�ڵ㣬1.0����ָ��ģ�����ƺͺ������Ƶ���ʽ
            #             2.0����ÿ����������Ϊһ���ļ�����ʽ��׼����һ���汾���죩
            #             ������Ҫ����ʶ��
            ret = xmlread( obj , 'function/input/arg' , [ 'name' , 'value' ] )
            if ret:
                ret = filter( lambda x:x[0] , ret )
                ret = dict( ret )
                if 'MODNAME' in ret and 'FUNCNAME' in ret:
                    self.py_ver = 1
                    mod = __import__( ret[ 'MODNAME' ] )
                    self.pyfunc = getattr( mod , ret[ 'FUNCNAME' ] )
                else:
                    self.py_ver = 2
                    raise RuntimeError( '�ݲ�֧�� V2.0��Py�ڵ�' )
            else:
                raise RuntimeError( 'PY�ڵ�ȱ��Ҫ��[%s]' % self._id )
            self.input_arg = ret
            
        elif self.filename.endswith( '.so' ):
            self._type = 'c'
        else:
            self._type = 'sub'
        
        ret = xmlread( obj , 'return/next' , [ 'value' , 'identifier' ] , shrink = False )
        if ret:
            self.next = dict( [ [ int( x[0] ) , [ x[1] , None ] ] for x in ret ] )
        else:
            self.next = {}
    
    def go_next( self , ret ):
        return self.next[ret][1]
    
    def __str__( self ):
        return str( self.__dict__ )

import copy
def build_flow( fn ):
    # �������̶����ļ��������̽ڵ���������start�ڵ㡣�ٹ�������У�����Ƿ��ж�����
    root = xml( open( fn , 'rb' ).read() )
    cache = {}
    for n in xmlreadobj( root , 'node' ):
        fobj = FlowNode( n )
        cache[ fobj._id ] = fobj
    # ���ݹ�ϵ���
    roots = copy.copy( cache )
    for x in cache.values():
        for k,n in x.next.items():
            if n[0] not in cache:
                raise RuntimeError( '[%s]�ķ���ֵ[%s]��Ӧ�Ľڵ�[%s]������' % ( x._id , k , n[0] ) )
            else:
                n[1] = cache[ n[0] ]
                roots.pop( n[0] , None )
    # �����Ϻ�roots�����Ԫ�ض���һ�������ʾ�����ڣ����Ǵ����
    if len( roots ) > 1:
        raise RuntimeError( '���̲����˶����ڣ�%s' % ( ','.join( roots.keys() ) ) )
    return cache[ 'start' ]
def goflow(flowfile,jyzd):
    curr = build_flow( flowfile )
    curr = curr.go_next( 0 )
    DEFAULT_RUN = { 'return':0 , 'expact': {} }
    DEFAULT_SKIP = { 'output': {} , 'return': 0 }
    jyzd = jyzd
    while curr._id != 'end':
        print '��ǰִ�е�[%s]' %( curr._id )
    #    if curr.input_arg:
    #        print curr.input_arg
    #    print curr.pyfunc
        if curr._type == 'py':
            if curr.input_arg:
                input = curr.input_arg
                FUNCNAME = input.pop('FUNCNAME')
                MODNAME = input.pop('MODNAME')
                fun_input = {}
                if len(input) > 0:
                    fun_input['input'] = input
                    jyzd.update( fun_input )
            ret = curr.pyfunc( jyzd )
        elif curr._type == 'c':
            ret = goflow('gl_qjycz.flow')
        curr = curr.go_next( ret )
    if curr._id != 'end':
        return -1
    else:
        return 0
    #act = expact.get( 'action' , 'auto' )
    #print act
#goflow('xmhht_zzzc.flow')
#jyzd = {}
#goflow('../../flow/sys_guocai.flow',jyzd)
#goflow('../../flow/subflow_sys_guocai_local2remote.flow',jyzd)
#if __name__ == '__main__':
#    if len( sys.argv ) == 1:
#        print usage
#        sys.exit( -1 )
#    main( sys.argv[1:] )