#!/bin/usr/env python
# coding: gbk
# 流程读取
from xmlparse import *
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

class FlowNode:
    # 流程节点定义对象
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
            # 对于py节点，1.0采用指定模块名称和函数名称的形式
            #             2.0采用每个函数独立为一个文件的形式（准备下一个版本改造）
            #             测试需要智能识别
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
                    raise RuntimeError( '暂不支持 V2.0的Py节点' )
            else:
                raise RuntimeError( 'PY节点缺少要素[%s]' % self._id )
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
    # 根据流程定义文件构造流程节点链表，返回start节点。再构造过程中，检测是否有断链。
    root = xml( open( fn , 'rb' ).read() )
    cache = {}
    for n in xmlreadobj( root , 'node' ):
        fobj = FlowNode( n )
        cache[ fobj._id ] = fobj
    # 根据关系组合
    roots = copy.copy( cache )
    for x in cache.values():
        for k,n in x.next.items():
            if n[0] not in cache:
                raise RuntimeError( '[%s]的返回值[%s]对应的节点[%s]不存在' % ( x._id , k , n[0] ) )
            else:
                n[1] = cache[ n[0] ]
                roots.pop( n[0] , None )
    # 组合完毕后，roots里面的元素多于一个，则表示多个入口，这是错误的
    if len( roots ) > 1:
        raise RuntimeError( '流程产生了多个入口：%s' % ( ','.join( roots.keys() ) ) )
    return cache[ 'start' ]
def goflow(flowfile,jyzd):
    curr = build_flow( flowfile )
    curr = curr.go_next( 0 )
    DEFAULT_RUN = { 'return':0 , 'expact': {} }
    DEFAULT_SKIP = { 'output': {} , 'return': 0 }
    jyzd = jyzd
    while curr._id != 'end':
        print '当前执行到[%s]' %( curr._id )
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