#!/bin/usr/env python
# coding: gbk
import flow_utils
from utils.ftools import AttrDict
def GUOCAI_ENTRY(jyzd):
    print ''
    flow_utils.goflow('mainflow_guocai.flow',jyzd)
def locale2remote(jyzd):
    req_msg = jyzd.get('req_msg','')
    flow_utils.goflow('guocai_locale2remote.flow',jyzd)
def remote2locale(jyzd):
    req_msg = jyzd.get('req_msg','')
    flow_utils.goflow('guocai_remote2locale.flow',jyzd)
jyzd = {'pub':{'subsysname':'tttttttt'}}
jyzd['req_msg'] = """88888<?xml version='1.0' encoding="GB2312"?><root><ver>1.0</ver><spid>11111</spid><spbillno>222222</spbillno><business_type>14900</business_type><business_no>444444</business_no><tran_amt>10000</tran_amt><cur_type></cur_type><true_name>11111</true_name><mobile></mobile><cre_id></cre_id><cre_type></cre_type><card_id>622384609891538799</card_id><card_type></card_type><bank_name>10000</bank_name><bank_ins_code>26520300</bank_ins_code><card_prov></card_prov><purpose></purpose><postscript></postscript><md5_sign></md5_sign><TransCode>api_acp_single.cgi</TransCode></root>"""
GUOCAI_ENTRY(jyzd)
#remote2locale(jyzd)
#remote2locale(jyzd)
#if __name__ == '__main__':
#    if len( sys.argv ) == 1:
#        print usage
#        sys.exit( -1 )
#    main( sys.argv[1:] )