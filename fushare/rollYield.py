# -*- coding:utf-8 -*-

"""
Created on 2018年07月11日
@author: lowin
@contact: li783170560@126.com

获取各合约展期收益率，日线数据从dailyBar脚本获取
"""

import numpy as np
import matplotlib.pyplot as plt
from fushare.symbolVar import *
from fushare.dailyBar import *
calendar = cons.get_calendar()

def _plot_bar(values,xtick):
    fig = plt.figure(1)
    ax = fig.add_subplot(111)
    ax.bar(range(len(values)), values, color="green")
    ax.set_xticks(range(len(xtick)))
    ax.set_xticklabels(xtick, fontsize=6)
    plt.show()


def _plot(values, xtick):
    plt.plot(values,xtick)
    plt.show()


def get_rollYield_bar(type = 'symbol',  var = 'RB',date= None, start = None, end = None, plot = False):
    """
        获取展期收益率
    Parameters
    ------
        type = 'symbol'：获取某天某品种所有交割月合约的收盘价
        type = 'var'：获取某天所有品种两个主力合约的展期收益率（展期收益率横截面）
        type = ‘date’：获取某品种每天的两个主力合约的展期收益率（展期收益率时间序列）
        start: 开始日期 format：YYYYMMDD
        end: 结束数据 format：YYYYMMDD
        date: 某一天日期 format： YYYYMMDD
        var: 合约品种如RB、AL等
    Return
    -------
        DataFrame
            展期收益率数据(DataFrame):
                ry      展期收益率
                index   日期或品种
    """

    date = cons.convert_date(date) if date is not None else datetime.date.today()
    start = cons.convert_date(start) if start is not None else datetime.date.today()
    end = cons.convert_date(end) if end is not None else cons.convert_date(cons.get_latestDataDate(datetime.datetime.now()))
    if type == 'symbol':
        df = get_future_daily(start=date, end=date, market=symbolMarket(var))
        df = df[df['variety'] == var]
        if plot:
            _plot_bar(df['close'].tolist(), df['symbol'].tolist())
        return df

    if type == 'var':
        df = pd.DataFrame()
        for market in ['dce','cffex','shfe','czce']:
            df = df.append(get_future_daily(start=date, end=date, market=market))
        varList = list(set(df['variety']))
        dfL=pd.DataFrame()
        for var in varList:
            ry = get_rollYield(date, var, df = df)
            if ry:
                dfL = dfL.append(pd.DataFrame([ry], index=[var], columns=['rollYield','nearBy','deferred']))
        dfL['date'] = date
        dfL = dfL.sort_values('rollYield')
        if plot:
            _plot_bar(dfL['rollYield'].tolist(), dfL.index)
        return dfL

    if type == 'date':
        dfL=pd.DataFrame()
        while start <= end:
            try:
                ry = get_rollYield(start, var)
                if ry:
                    dfL = dfL.append(pd.DataFrame([ry], index=[start], columns=['rollYield','nearBy','deferred']))
            except:
                pass
            start += datetime.timedelta(days=1)
        if plot:
            _plot(pd.to_datetime(dfL.index), dfL['rollYield'].tolist())
        return dfL



def get_rollYield(date = None, var = 'IF',symbol1 = None, symbol2 = None, df = None):
    """
            获取某一天某一品种（主力和次主力）、或固定两个合约的展期收益率
        Parameters
        ------
            date: string 某一天日期 format： YYYYMMDD
            var: string 合约品种如RB、AL等            
            symbol1: string 合约1如rb1810
            symbol2: string 合约2如rb1812
            df: DataFrame或None 从dailyBar得到合约价格，如果为空就在函数内部抓dailyBar，直接喂给数据可以让计算加快
        Return
        -------
            tuple
            rollYield
            nearBy
            deferred
    """
    date = cons.convert_date(date) if date is not None else datetime.date.today()
    if date.strftime('%Y%m%d') not in calendar:
        warnings.warn('%s非交易日' % date.strftime('%Y%m%d'))
        return None
    if symbol1:
        var = symbol2varietie(symbol1)
    if type(df) != type(pd.DataFrame()):
        market = symbolMarket(var)
        df = get_future_daily(start=date, end=date, market=market)
    if var:
        df = df[df['variety'] == var].sort_values('open_interest',ascending=False)
        df['close']=df['close'].astype('float')
        symbol1 = df['symbol'].tolist()[0]
        symbol2 = df['symbol'].tolist()[1]

    close1 = df['close'][df['symbol'] == symbol1.upper()].tolist()[0]
    close2 = df['close'][df['symbol'] == symbol2.upper()].tolist()[0]

    A = re.sub(r'\D', '', symbol1)
    A1 = int(A[:-2])
    A2 = int(A[-2:])
    B = re.sub(r'\D', '', symbol2)
    B1 = int(B[:-2])
    B2 = int(B[-2:])
    c = (A1 - B1) * 12 + (A2 - B2)
    if close1 == 0 or close2 == 0:
        return False

    if c > 0:
        return np.log(close2/close1)/c*12, symbol2,symbol1
    else:
        return np.log(close2/close1)/c*12, symbol1,symbol2



if __name__ == '__main__':

    d = get_rollYield_bar(type = 'var', date = '20181214',plot = True)
    print(d)
