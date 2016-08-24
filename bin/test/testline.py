#coding:gbk
import os
import sys
fn = sys._getframe().f_code.co_filename.split(os.sep)[-1]
def funcname():
    frame = None
    try:
        raise ZeroDivisionError
    except ZeroDivisionError:
        frame = sys.exc_info()[2].tb_frame.f_back
    return frame.f_code.co_name
def get_cur_info():
    print fn  #当前文件名，可以通过__file__获得
    print funcname()  #当前函数名
get_cur_info()
