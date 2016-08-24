# coding: gbk

from sqlalchemy.orm import *
from sqlalchemy.ext.declarative import *

class Settings(object):
    """
    用户使用register方法将配置项增加到系统中
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
            raise EnvironmentError, "无法导入配置模块[%s]: %s" % ( module, e )
        
        for setting in dir(mod):
            if setting == setting.upper():
                setting_value = getattr(mod, setting)
                if setting not in self:
                    setattr(self, setting , setting_value)
                
        # 更新默认值
        default_dict( self._dict , self.default )
        
        # 处理完所有参数后，才应该处理数据库连接，避免由于顺序问题导致错误
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
            msg = '，' + msg
        for x in args:
            if isinstance( x , str ):
                if x.upper() not in self:
                    raise RuntimeError( '参数[%s]还未定义' % x.upper() + msg )
    
    def __str__( self ):
        return repr( self.__dict__ )
    
    def contract( self , name ):
        # 约束查找方式为：
        #   从Level大的约束开始找起
        if self._contract[-1].level != 0:
            # 必须有一个0级的约束，用于定义全部的，最低等级的level
            raise RuntimeError( '约束定义不完善，未定义默认0级约束' )
            
        for x in self._contract:
            v = x.items.get( name )
            if v is not None:
                return v
        raise RuntimeError( '约束[%s]查找失败，请确认定义了该约束条件' % name )
    
    def enable_c( self , pkg_name ):
        # 指定包的名字，自动载入_contract下的约束条件
        # 要求：_contract包下的__init__.py 中定义0级约束对象，并给出ver_list列表，列表是该
        #       包下所有需要引入的定义了约束的模块名称列表
        try:
            mod = __import__( pkg_name + '._contract'  , {} , {} , [''] )
        except:
            raise RuntimeError( '找不到约束定义，系统无法启动' )
        
        versions = getattr( mod , 'ver_list' , [] )
        for v in versions:
            try:
                __import__( pkg_name + '._contract.' + v , {} , {} , [''] )
            except:
                pass

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

class Contract( object ):
    # 约束用一个字典存放。
    # 约束的内容为：名称 值，使用字典存放
    # 约束的值不可为None
    
    def __init__( self , level ):
        self.level = level
        self.items = {}
        
        settings._contract.append( self )
        settings._contract.sort( key = lambda x:x.level , reverse = True )
    
    def update( self , di , **kwargs ):
        if type( di ) != dict:
            raise RuntimeError( '请使用字典来定义约束' )
        
        self.items.update( di )
        if kwargs:
            self.items.update( kwargs )
            
        if None in self.items.values():
            i = [ str(x[0]) for x in self.items.items() if x[1] is None ]
            raise RuntimeError( '约束[%s]不可以为None' % ','.join( i ) )
    
    def set( self , name , value ):
        if value is None:
            raise RuntimeError( '约束[%s]不可为None' % name )
        self.items[ name ] = value

settings = Settings()
