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
        t1 = posi['data']['coin_list']
        for c in t1:
            coin = c['coin']
            vol = float(c['normal'])
            re_posi[coin] = vol
    return re_posi

# 获取huobi仓位
def get_huobi_position(log):
    # 返回结果是字典
    re_posi = {}
    # 读取持仓
    posi = hbs.get_balance()
    if posi['status'] != 'ok':
        log.error(posi)
    else:
        t1 = posi['data']['list']
        for c in t1:
            coin = c['currency']
            vol = float(c['balance'])
            # 货币资产把冻结资产和可交易资产分开，所以需要加起来才是总仓位
            if re_posi.__contains__(coin):
                re_posi[coin] += vol
            else:
                re_posi[coin] = vol

    return re_posi


def do_hedge(p_u, p_h, b_p, log):
    for base in b_p:
        coin = base['coin']
        base_vol = float(base['base_vol'])

        # 实际总持仓量
        total = p_u[coin] + p_h[coin]

        # 相关交易数据
        hedge_vol = 0.0
        hedge_direct = ''
        if total > base_vol:
            # 做空
            hedge_vol = total - base_vol
            hedge_direct = 'SELL'

        if total < base_vol:
            # 做多
            hedge_vol = base_vol- total
            hedge_direct = 'BUY'

        # 如果对冲数量大于0，则执行对冲交易
        if hedge_vol > 0:
            do_trade_huobi(coin, hedge_vol, hedge_direct, log)
    return

# 在火币下单, 因为对冲，所以直接下市价单
def do_trade_huobi(coin, he_v, he_d,log):
    sym = coin + 'usdt'
    if he_d == 'BUY':
        t = 'buy-market'
    else:
        t = 'sell-market'

    # 下单交易
    hbs.send_order(
        amount=he_v,
        source='api',
        symbol=sym,
        _type=t)
    return
