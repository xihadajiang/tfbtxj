# coding: gbk

from sqlalchemy.orm import *
from sqlalchemy.ext.declarative import *

class Settings(object):
    """
    �û�ʹ��register���������������ӵ�ϵͳ��
    """
    def __init__( self ):
        self.modules = []
        self._contract = []
        self._dict = {}
        self.default = { 'USE_DB' : True }
        #self.USE_DB = True
        
    def register( self , module ):
        if module in self.modules:
            return
        try:
            mod = __import__( module  , {} , {} , [''] )
            self.modules.append( module )
        except ImportError, e:
            from shangjie.utils import traceback2
            traceback2.print_exc( show_locals = True )
            raise EnvironmentError, "�޷���������ģ��[%s]: %s" % ( module, e )
        
        for setting in dir(mod):
            if setting == setting.upper():
                setting_value = getattr(mod, setting)
                if setting not in self:
                    setattr(self, setting , setting_value)
                
        # ����Ĭ��ֵ
        default_dict( self._dict , self.default )
        
        # ���������в����󣬲�Ӧ�ô������ݿ����ӣ���������˳�����⵼�´���
        if self.DB_ENGINE and ( 'DB_SESSION' not in self ) and self.USE_DB:
            self.DB_SESSION = scoped_session( sessionmaker( autocommit = True , autoflush = False , bind = self.DB_ENGINE ) ) # 0.5
            #self.DB_SESSION = scoped_session( sessionmaker( transactional = False , autoflush = False , bind = self.DB_ENGINE ) ) # 0.4
            self.BaseModel = declarative_base( self.DB_ENGINE )
            self.BASEMODEL = self.BaseModel
    
    def __getattr__( self , name ):
        if name in self._dict:
            return self._dict[ name ]
        else:
            return None
    
    def __setattr__( self , name , val ):
        if name in ( 'modules' , '_contract' , '_dict' , 'default' ):
            self.__dict__[ name ] = val
        else:
            self._dict[ name ] = val
    
    def __contains__( self , name ):
        return name in self._dict
    
    def unpack( self , d ):
        for k,v in self._dict.items():
            if k == k.upper():
                d[k] = v
    
    def check( self , *args , **kwargs ):
        msg = kwargs.get( 'msg' , '' )
        if msg:
            msg = '��' + msg
        for x in args:
            if isinstance( x , str ):
                if x.upper() not in self:
                    raise RuntimeError( '����[%s]��δ����' % x.upper() + msg )
    
    def __str__( self ):
        return repr( self.__dict__ )
    
    def contract( self , name ):
        # Լ�����ҷ�ʽΪ��
        #   ��Level���Լ����ʼ����
        if self._contract[-1].level != 0:
            # ������һ��0����Լ�������ڶ���ȫ���ģ���͵ȼ���level
            raise RuntimeError( 'Լ�����岻���ƣ�δ����Ĭ��0��Լ��' )
            
        for x in self._contract:
            v = x.items.get( name )
            if v is not None:
                return v
        raise RuntimeError( 'Լ��[%s]����ʧ�ܣ���ȷ�϶����˸�Լ������' % name )
    
    def enable_c( self , pkg_name ):
        # ָ���������֣��Զ�����_contract�µ�Լ������
        # Ҫ��_contract���µ�__init__.py �ж���0��Լ�����󣬲�����ver_list�б��б��Ǹ�
        #       ����������Ҫ����Ķ�����Լ����ģ�������б�
        try:
            mod = __import__( pkg_name + '._contract'  , {} , {} , [''] )
        except:
            raise RuntimeError( '�Ҳ���Լ�����壬ϵͳ�޷�����' )
        
        versions = getattr( mod , 'ver_list' , [] )
        for v in versions:
            try:
                __import__( pkg_name + '._contract.' + v , {} , {} , [''] )
            except:
                pass

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

class Contract( object ):
    # Լ����һ���ֵ��š�
    # Լ��������Ϊ������ ֵ��ʹ���ֵ���
    # Լ����ֵ����ΪNone
    
    def __init__( self , level ):
        self.level = level
        self.items = {}
        
        settings._contract.append( self )
        settings._contract.sort( key = lambda x:x.level , reverse = True )
    
    def update( self , di , **kwargs ):
        if type( di ) != dict:
            raise RuntimeError( '��ʹ���ֵ�������Լ��' )
        
        self.items.update( di )
        if kwargs:
            self.items.update( kwargs )
            
        if None in self.items.values():
            i = [ str(x[0]) for x in self.items.items() if x[1] is None ]
            raise RuntimeError( 'Լ��[%s]������ΪNone' % ','.join( i ) )
    
    def set( self , name , value ):
        if value is None:
            raise RuntimeError( 'Լ��[%s]����ΪNone' % name )
        self.items[ name ] = value

settings = Settings()
