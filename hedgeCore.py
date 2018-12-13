"""
# -*- coding: utf-8 -*-
@author: robin.liu
@github: qqqlyx
"""


'''
对齐持仓量的方式，来进行对冲
UniDAX + Huobi
'''

import hedge_action_position as hed
from UniDax import UniDaxServices as uds, Constant as cons
import threading
import logging
import datetime
import json
from pprint import pprint

# 用于记录基准仓位
base_position = []


# 定期调用做市程序
def core_timer():
    # log
    global run_count
    log.warning('Start Hedge, ' + str(run_count))

    # 查询unidax持仓
    posi_unidax = hed.get_unidax_position(log)

    # 查询huobi持仓
    posi_huobi = hed.get_huobi_position(log)

    # uni+huobi总仓位，与起始仓位进行对比
    hed.do_hedge(posi_unidax, posi_huobi, base_position, log)

    # 定时循环
    global timer
    timer = threading.Timer(10, core_timer)
    timer.start()
    # log
    log.warning('End Hedge, ' + str(run_count))
    run_count += 1


def set_log():
    # 创建一个logger
    # log等级 info < warning < error
    logger = logging.getLogger()
    logger.setLevel(logging.DEBUG)
    # 创建一个handler，用于写入日志文件
    date = datetime.datetime.now().strftime('%Y%m%d')
    logname = date
    fh = logging.FileHandler('log//' + logname)
    fh.setLevel(logging.DEBUG)
    # 再创建一个handler，用于输出到控制台
    ch = logging.StreamHandler()
    ch.setLevel(logging.WARNING)
    # 定义handler的输出格式
    formatter = logging.Formatter('%(asctime)s - %(levelname)s - %(message)s')
    fh.setFormatter(formatter)
    ch.setFormatter(formatter)
    # 给logger添加handler
    logger.addHandler(fh)
    logger.addHandler(ch)
    # 记录一条日志
    logger.info('robin hedge')
    return logger


run_count = 1
log = set_log()


# 获取coin基准持仓
f = open('log//base_position.txt')
try:
    for l in f:
        line = l
        line = line.rstrip('\n') # 默认读取末尾会有换行符，这儿给删掉
        sa = line.split(',')
        dict = {'coin': sa[0], 'base_vol': sa[1]}
        base_position.append(dict)
finally:
     f.close()

# 开始定时器
timer = threading.Timer(1, core_timer)
timer.start()
