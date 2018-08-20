# -*- coding:utf-8 -*- 

__version__ = '1.1.1'
__author__ = 'Lowin'


"""
大宗商品现货价格及基差
"""
from fushare.basis import (get_spotPrice_daily,
                           get_spotPrice)


"""
期货持仓成交排名数据
"""
from fushare.cot import (get_rank_sum_daily,
                         get_rank_sum,
                         get_shfe_rank_table,
                         get_czce_rank_table,
                         get_dce_rank_table,
                         get_cffex_rank_table)


"""
大宗商品仓单数据
"""
from fushare.receipt import (get_reciept)


"""
大宗商品仓单数据
"""
from fushare.rollYield import (get_rollYield_bar, get_rollYield)


"""
交易所行情数据日线
"""
from fushare.dailyBar import (get_cffex_daily,
                              get_czce_daily,
                              get_shfe_vwap,
                              get_shfe_daily,
                              get_dce_daily,
                              get_future_daily)