"""
# -*- coding: utf-8 -*-
@author: robin.liu

用来对冲成交单
"""

from Huobi import HuobiServices as hbs
from UniDax import UniDaxServices as uds, Constant as cons
import json
import random

# 获取全部成交单

a = uds.all_trade('ethusdt')

print(a)