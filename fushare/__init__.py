# -*- coding:utf-8 -*- 

"""
版本改动记录:
1.1.7：
郑商所的仓单数据有些输出的格式是文本，改成int型；
郑商所有一些时间段得到的仓单是仓单变化量，修正此bug  
1.1.8:
上期所网站丢失了两个交易日20100416、20130821的数据，在调取此数据时返回None
1.1.9:
基差数据、会员持仓数据、仓单数据，在爬取过早日期时，出现交易所/生意社网还未发布源数据时，跳过并提示用户数据起始日期；
修正了基差数据第二次爬取时，由于用LATEST网址格式，出现日期不匹配跳过的问题；
修改了郑商所会员持仓数据在2010年8月25日前爬取失败的问题
在爬取基差数据和会员持仓数据时，如果出现连续爬取失败超过限制，直接返回已爬过的数据

"""




__version__ = '1.1.9'
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