"""
# -*- coding: utf-8 -*-
@author: robin.liu
"""

from Huobi import HuobiServices as hbs
from UniDax import UniDaxServices as uds, Constant as cons
import json
import random

# 获取unidax仓位
def get_unidax_position(log):
    # 返回结果是字典
    re_posi = {}
    # 读取unidax持仓
    posi = uds.account()
    if posi['msg'] != 'suc':
        log.error(posi)
    else:
        t1 = posi['data']['coin_list']  # 使用eval会报错，因次用了json方法转换str -> dict
        for c in t1:
            coin = c['coin']
            vol = c['normal']
            re_posi[coin] = vol
    return re_posi

