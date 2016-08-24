# coding: gbk

# ���庯������
import cStringIO , textwrap , types

try:
    from functools import partial
except ImportError:
    def partial( func , *args, **kwargs):
        # �����ṩ�����ֲ������������ܡ�
        def _curried(*moreargs, **morekwargs):
            return func(*(args+moreargs), **dict(kwargs.items() + morekwargs.items()))
        return _curried

class Stack( list ):

    def push( self , *args ):
        if len( args ) == 1:
            args = args[0]
        self.insert( 0 , args )

    def pop( self ):
        if len( self ) :
            return list.pop( self , 0 )
        else:
            raise StackEmpty()

    def top( self ):
        if len( self ) :
            return self[ 0 ]
        else:
            raise StackEmpty()

    def depth( self ):
        return len( self )
    
    def is_empty( self ):
        return self.depth() == 0

class StackEmpty( Exception ):
    def __init__( self ):
        self.args = ( 'empty stack' , )

import copy
class AttrDict( object ):
    # ��ʹ�����Է������ݵ��ֵ���
    
    def __init__( self , initd = None , nocopy = True , kword = None , strict = False ):
        """
            initd       ��ʼ�ֵ�
            nocopy      �Ƿ��Ƴ�ʼ�ֵ䣨Ĭ�ϲ����������Ч�ʣ�
            kword       �ؼ��֣��ؼ��ֱ�֤���ݵĴ��ڣ�����������
            strict      �Ƿ��ϸ�����ΪTrueʱ���������ȡ�����ڵ����ݣ����򷵻�False
        """
        self._stack = []
        if nocopy:
            self._dict = initd or {}
        else:
            self._dict = copy.deepcopy( initd or {} )
        self.Keyword = kword
        self.strict = strict
    
    def __getitem__( self , key ):
        return self.__getattr__( key )
    
    def __setitem__( self , key , value ):
        return self.__setattr__( key , value )
    
    def keys( self ):
        return self._dict.keys()
    
    def values( self ):
        return self._dict.values()
    
    def __getattr__( self , key ):
        try:
            return self.__dict__['_dict'][ key ]
        except KeyError:
            try:
                attr = getattr( self.Keyword , key )
                return attr.default
            except AttributeError:
                if self.__dict__['strict']:
                    raise KeyError( key )
                else:
                    return None
    
    def __setattr__( self , key , value ):
        if key == '_dict':
            self.__dict__[ '_dict' ] = value
            return
        if key == '_stack':
            self.__dict__[ '_stack' ] = value
            return
        if key == 'Keyword':
            self.__dict__[ 'Keyword' ] = value
            return
        if key == 'strict':
            self.__dict__[ 'strict' ] = value
            return
        try:
            attr = getattr( self.Keyword , key )
            self._dict[ key ] = attr.validate( key , value )
        except AttributeError:
            self._dict[ key ] = value

    def __delattr__( self , key ):
        if self._dict.get( key , None ):
            del self._dict[ key ]
    
    def __copy__( self , memo ):
        return self.to_dict()
    
    __deepcopy__ = __copy__
    
    def to_dict( self ):
        d = copy.deepcopy(self._dict)
        return d

    def from_dict( self , d , nocopy = False ):
        if type(d) is not dict:
            d = {}
        if nocopy:
            self._dict = d
        else:
            self._dict = copy.deepcopy( d )

    def get( self , key , *args ):
        keys = key.split('.')
        dict1 = self._dict
        li = []
        for k1 in keys:
            if type( dict1 ) == AttrDict:
                dict1 = dict1._dict
            try:
                dict1 = getattr( dict1 , k1 )
            except:
                try:
                    dict1 = dict1[k1]
                except:
                    if args:
                        return args[0]
                    else:
                        raise KeyError( '�޷��ڶ���[%s]���ҵ�[%s]��ֵ' % ( '.'.join( li ) , k1 ) )
            li.append( k1 )
        
        return dict1
        
    def push( self ):
        self._stack.append( copy.deepcopy( self._dict ) )

    def pop( self ):
        self._dict = self._stack.pop()

    def clear( self ):
        self._dict.clear()

    def update( self , dic ):
        self._dict.update( dic )

    def __str__( self ):
        s = cStringIO.StringIO()
        s.write( 'AttrDict{\n' )
        keys = self.keys()
        keys.sort()
        for key in keys:
            value = self._dict[ key ]
            r = repr( value )
            r = '\n'.join( textwrap.wrap( r ) )
            s.write( '%s:%s\n' % ( key , r ) )
        s.write( '}\n' )
        return s.getvalue()
    
    __repr__ = __str__
    
    def __getstate__( self ):
        return self.to_dict()
    
    def __setstate__( self , arg ):
        self.from_dict( arg )

import __builtin__
import inspect

class Namespace:
    # �����ṩע�ᵽϵͳ����չ���������ֿռ�
    @staticmethod
    def create( name ):
        if not name:
            __builtin__.ns_modules = {}
            return __builtin__
        
        root = __builtin__
        path = []
        for x in name.split('.'):
            path.append( x )
            if hasattr( root , x ):
                root = getattr( root , x )
            else:
                ns = Namespace( '.'.join( path ) )
                setattr( root , x , ns )
                root = ns
                
        return root
        
    def __init__( self , name ):
        self.__name = name
        self.ns_modules = {}
    
    def __str__( self ):
        return self.__name
    
    
def _register( spc , obj ):
    if inspect.isfunction( obj ):
        name = getattr( obj , 'name' , obj.func_name )
    elif inspect.isclass( obj ):
        name = obj.__name__
    else:
        raise RuntimeError( '���ֿռ���ֻ��ע�ắ������[%s]' % str( type( obj ) ) )
        
    if name in spc.ns_modules and obj.__module__ != spc.ns_modules[ name ]:
        warnings.warn( '�Ѿ���[%s]���ֿռ���ע���˺���[%s]' % ( spc , name ) , RuntimeWarning )
        #raise RuntimeError( '�Ѿ���[%s]���ֿռ���ע���˺���[%s]' % ( spc , name ) )
        return
    
    spc.ns_modules[ name ] = obj.__module__
    setattr( spc , name , obj )

def register( namespace = None ):
    if type( namespace ) in ( tuple , list ):
        ns = map( Namespace.create , namespace )
    else:
        ns = ( Namespace.create( namespace ) , )
    
    def _reg( func ):
#        # TODO �˴���ע�ͺ����, ò����Ϊ�˹��ʲô����. ����ʷ̫����Զ. ��ʱ����������, �������ٴ�
#        if func.__module__ == '__main__':
#            return func
            
        for n in ns:
            _register( n , func )
        return func
        
    return _reg
    
import warnings
def deprecation( msg = '' ):
    def _call( func ):
        def call_func( *args , **kwargs ):
            warnings.warn( '�ú���[%s]�����¸��汾�б�����[%s]' % ( func.func_name , msg ) , DeprecationWarning )
            return func( *args , **kwargs )
        call_func.get_name = func.func_name
        return call_func
    return _call

def decal2( *args ):
    # �ѿ�����ʵ��
    if len( args ) != 2:
        raise RuntimeError( 'decal2��������Ϊ�����б�����' )
        
    for x in args[0]:
        for y in args[1]:
            if isinstance( x , tuple ) or isinstance( x , list ):
                b = list( x )
            else:
                b = [x]
            b.append( y )
            yield b

def decal( *args ):
    b = args[0]
    for x in args[1:]:
        b = decal2( b , x )
    
    return list( b )

import time , datetime
def str2dt( s , fmt , default = None , null = None ):
    try:
        t = time.strptime( s , fmt )
        if ( '%Y' in fmt ):
            if ( '%H' in fmt ):
                v = datetime.datetime( t[0] , t[1] , t[2] , t[3] , t[4] , t[5] )
            else:
                v = datetime.date( t[0] , t[1] , t[2] )
        else:
            v = datetime.time( t[3] , t[4] , t[5] )
        return v
    except:
        if default:
            return default
        else:
            raise

def rq2zqdm(zqdm,rq):
    if zqdm == 'D':
        zq = 'D%04d%02d%02d' % ( rq.year , rq.month , rq.day )
    elif zqdm == 'M':
        zq = 'M%04d%02d' % ( rq.year , rq.month )
    elif zqdm == 'Q':
        zq = 'Q%04d%02d' % ( rq.year , ( rq.month - 1 ) / 3 + 1 )
    elif zqdm == 'B':
        zq = 'B%04d%02d' % ( rq.year , ( rq.month - 1 ) / 6 + 1 )
    elif zqdm == 'Y':
        zq = 'Y%04d' % rq.year
    else:
        zq = ''
    return zq

def func_loader( mpath ):
    if mpath:
        try:
            _mod = mpath.rsplit('.',1)
            smod = _mod[0]
            sfunc = _mod[-1]
            if len( _mod ) != 1:
                mod = __import__( smod )
                ms = smod.split( '.' )
                for mn in ms[1:]:
                    mod = mod.__dict__[ mn ]
            else:
                mod = __builtins__
            return getattr(mod,sfunc)
        except Exception , e:
            print e

KEY_ERROR = '__keyerror__'

class PickleReader( object ):
    """
        ��Pickle�ֶε�ֵ����ö���
        >>> p = PickleReader( { 'a':1 , 'b':2 , 'c':[ 1  , 2, 3 , 4, { 5:'aaa' , '6':'bbb' } ] } )
        >>> print d.get( 'a' )
        1
        >>> print d.get( 'b' )
        2
        >>> print d.get( 'c.0' )
        1
    """
    def __init__( self , v ):
        self.v = v
    
    def get( self , key , default = KEY_ERROR ):
        if not key:
            return self.v
            
        o = self.v
        keys = key.split( '.' )
        for i in range( len( keys ) ):
            x = keys[ i ]
            if isinstance( o , dict ):
                if x.isdigit() and x not in o:
                    o = o.get( int( x ) , default )
                else:
                    o = o.get( x , default )
                if o == KEY_ERROR:
                    raise KeyError( '.'.join( keys[:i+1] ) )
            elif isinstance( o , list ) or isinstance( o , tuple ):
                if x.isdigit():
                    try:
                        o = o[ int( x ) ]
                    except:
                        if default == KEY_ERROR:
                            raise IndexError( 'Ԥ���ʵ��±�Խ��[%s]' % '.'.join( keys[:i+1] ) )
                        else:
                            o = default
                else:
                    raise RuntimeError( '�±�[%s]���ַ�����ͬ�������Բ�ƥ��' % ( '.'.join( keys[:i+1] ) ) )
            else:
                raise RuntimeError( '�±�[%s]ֻ�������ֵ䡢�б��Ԫ������ݣ�Ŀǰ��������Ϊ��%s' % ( '.'.join( keys[:i+1] ) , type( o ) ) )
        return o
        
    def set( self , key , value ):
        keys = key.split( '.' )
        try:
            o = self.get( '.'.join( keys[:-1] ) )
        except:
            raise RuntimeError( 'set�������������Ѵ��ڵļ���[%s]������' % '.'.join( keys[:-1] ) )
            
        key = keys[-1]
        if isinstance( o , dict ):
            o[ key ] = value
        elif isinstance( o , list ):
            if key.isdigit():
                o[ int( key ) ] = value
            else:
                raise RuntimeError( '�±�[%s]��Ӧ���������б���keyֵ������[%s]' % ( '.'.join( keys[:-1] ) , key ) )
        else:
            raise RuntimeError( '�±�[%s]��Ӧ�����ݷ�����[%s]' % ( '.'.join( keys[:-1] ) , type( o ) ) )

def colno( cn ):
    """
        for i in range( 26 ):
            c = chr( ord( 'A' ) + i )
            print c , colno( c )
            
        print colno( 'AA' )
        print colno( 'Z' )
        raw_input()
    """
    n = 0
    for x in cn:
        b = ord( x ) - ord( 'A' ) + 1
        n = n * 26 + b
    return n - 1

DO_NOTHING = lambda x:x
def get_record( header , static , data , g ):
    """
    ������
        header����ͷ�������ֵ�
                key     Ϊexcel�е�����
                value   Ϊ������ʽ
                        1 ���Զ�Ӧ����У���HY_HEADER�� 'C'
                        2 ÿ���п��Զ�Ӧһ��ת����������HY_HEADER�� 'E'
        static����̬���ݡ��ֵ�
                ���ڲ���̶����ݣ��ᱻheader��ȡ�Ľ������
                
        data  ��csv��ȡ����б��ǵ�Ҫstrip����split(',')
        g     ��������ȡת���������ֵ䣬ͨ�����Դ���globals()
    ������
        sex = lambda x: '1' if x == '��' else '2'

        HY_HEADER = { 'C':'hydm,mm' , 'D':'xm' , 'E':'xb:sex' , 'Q':'sr' , 'AW':'sj' , 'AX':'gh' }
        HY_STATIC = { 'jsdm': '9997' , 'glqx':'3' }

        JG_HEADER = { 'F': 'jgmc' }
        JG_STATIC = { 'zt': '0' }
        
    """
    d = copy.copy( static )
    for coln , conf in header.items():
        col = colno( coln )
        try:
            v = data[col]
        except:
            v = None
        # ���conf
        conf = conf.split( ',' )
        for c in conf:
            if ':' in c:
                c , f = c.split( ':' )
                f = g.get( f , DO_NOTHING )
            else:
                c , f = c , DO_NOTHING
            d[ c ] = f( v ) # ��������
    return d
