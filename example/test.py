import fushare

def test():
    print('测试及功能展示：')

    #----------------------------------------------------------------------
    print('\n' +'-'*80+'\n一个品种在时间轴上的展期收益率')
    df = fushare.get_rollYield_bar(type='date', var='RB', start='20180608', end='20180718', plot=False)
    print(df)

    #----------------------------------------------------------------------
    print('\n' +'-'*80+'\n一个品种在不同交割标的上的价格比较')
    df = fushare.get_rollYield_bar(type = 'symbol', var = 'RB', date = '20180718',plot = False)
    print(df)

    #----------------------------------------------------------------------
    print('\n' +'-'*80+'\n多个品种在某天的展期收益率横截面比较')
    df = fushare.get_rollYield_bar(type = 'var', date = '20180718',plot = False)
    print(df)

    #----------------------------------------------------------------------
    print('\n' +'-'*80+'\n特定两个标的的展期收益率')
    df = fushare.get_rollYield(date = '20180718', var = 'IF', symbol1 = 'IF1812', symbol2 = 'IF1811')
    print(df)

    #----------------------------------------------------------------------
    print('\n' +'-'*80+'\n特定品种、特定时段的交易所注册仓单')
    df = fushare.get_reciept(start='20180712', end='20180719', vars=['CU', 'NI'])
    print(df)

    #----------------------------------------------------------------------
    print('\n' +'-'*80+'\n特定日期的现货价格及基差')
    df = fushare.get_spotPrice('20180719')
    print(df)

    #----------------------------------------------------------------------
    print('\n' +'-'*80+'\n特定品种、特定时段的现货价格及基差')
    df = fushare.get_spotPrice_daily(start='20180710', end='20180719', vars=['CU', 'RB'])
    print(df)

    #----------------------------------------------------------------------
    print('\n' +'-'*80+'\n特定品种、特定时段的会员持仓排名求和')
    df = fushare.get_rank_sum_daily(start = '20180718', end = '20180719', vars = ['IF', 'C'])
    print(df)

    #----------------------------------------------------------------------
    print('\n' +'-'*80+'\n大商所会员持仓排名细节；郑商所、上期所、中金所分别改成get_czce_rank_table、get_shfe_rank_table、get_cffex_rank_table')
    df = fushare.get_dce_rank_table('20180718')
    print(df)

    #----------------------------------------------------------------------
    print('\n' +'-'*80+'\n日线行情获取')
    df = fushare.get_future_daily(start='20180818', end='20180821', market='CFFEX')
    print(df)


if __name__ == '__main__':
    test()