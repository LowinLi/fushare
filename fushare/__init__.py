# -*- coding:utf-8 -*- 

"""
版本改动记录:
1.1.7：
郑商所的仓单数据有些输出的格式是文本，改成int型；
郑商所有一些时间段得到的仓单是仓单变化量，修正此bug  
1.1.8:
上期所网站丢失了两个交易日20100416、20130821的数据，在调取此数据时返回None
"""




__version__ = '1.1.8'
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