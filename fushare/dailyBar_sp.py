# !/usr/bin/env python3
# -*- coding:utf-8 -*-
'''
created by Fangyang on Time:2018/10/26
'''

__author__ = 'Fangyang'

import requests
from fushare import cons
from fushare.symbolVar import symbol2varietie
import pandas as pd
import datetime


def gen_url_str(bar_type, symbol, exchange):

    if len(symbol) <= 3:   # 判断是否为连续合约, 连续合约url要加 0
        symbol = symbol + '0'

    if bar_type == '':
        url_str = cons.COMMODITY_DAILY_URL.format(bar_type, symbol)
        if exchange is 'cffex':
            url_str = cons.FINANCIAL_DAILY_URL.format(bar_type, symbol)
        return url_str

    else:
        url_str = cons.COMMODITY_MIN_URL.format(bar_type, symbol)
        if exchange is 'cffex':
            url_str = cons.FINANCIAL_MIN_URL.format(bar_type, symbol)
        return url_str


def get_json_daily_data_to_df(url_str, start, end, symbol, exchange):

    try:
        r = requests.get(url_str, timeout=5)
        r_json = r.json()
        r_lists = list(r_json)
        df = pd.DataFrame(r_lists, columns=['date', 'open', 'high', 'low', 'close', 'vol'])
        df['date'] = pd.to_datetime(df['date'])

        if start <= end:
            start = pd.Timestamp(start)
            end = pd.Timestamp(end)
            df = df[(df['date'] >= start) & (df['date'] <= end)]

        df['exchange'] = exchange
        df['symbol'] = symbol
        print('成功获取{}的{}'.format(exchange, symbol))
        return df
    except:
        print('Error : API 接口获取数据有问题')


def get_future_daily_sp(start=None, end=None, bar_type='1D', symbol=None):
    '''

    :param start: k线起始日期, format：YYYY-MM-DD 或 YYYYMMDD 或 datetime.date对象 为空时为当天
    :param end: k线结束日期, format：YYYY-MM-DD 或 YYYYMMDD 或 datetime.date对象 为空时为当天
    :param bar_type: k线类型, 分钟包括[5m, 15m, 30m, 60m], 日k为 [1D]
    :param symbol: 合约代码, 举例螺纹钢 RB 表示连续合约, RB1801 表示具体合约
    :return: df
    '''

    start = cons.convert_date(start) if start is not None else datetime.date.today()
    end = cons.convert_date(end) if end is not None else cons.convert_date(
        cons.get_latestDataDate(datetime.datetime.now()))

    if bar_type == '1D':
        bar_type = ''
        exchange_symbols_dict = cons.market_var

        if symbol is None:   # 如果symbol为 None, 返回所有连续合约, 这里再测试下,如果总失败, drop
            all_symbols_daily_bar_df = pd.DataFrame()
            for exchange, symbols in exchange_symbols_dict.items():
                for symbol in symbols:
                    url_str = gen_url_str(bar_type, symbol, exchange)
                    df = get_json_daily_data_to_df(url_str, start, end, symbol, exchange)
                    all_symbols_daily_bar_df = all_symbols_daily_bar_df.append(df, ignore_index=True)  # 这里要赋值,要不empty
            return all_symbols_daily_bar_df

        else:
            for exchange, symbols in exchange_symbols_dict.items():
                if symbol2varietie(symbol) in symbols:
                    print("合约代码 {} 属于 {} 交易所".format(symbol, exchange))
                    url_str = gen_url_str(bar_type, symbol, exchange)
                    return get_json_daily_data_to_df(url_str, start, end, symbol, exchange)
                else:
                    print("合约代码 {} 不属于 {} 交易所".format(symbol, exchange))

    else:
        exchange_symbols_dict = cons.market_var
        for exchange, symbols in exchange_symbols_dict.items():
            if symbol2varietie(symbol) in symbols:
                print("合约代码 {} 属于 {} 交易所".format(symbol, exchange))
                url_str = gen_url_str(bar_type, symbol, exchange)
                return get_json_daily_data_to_df(url_str, start, end, symbol, exchange)
            else:
                print("合约代码 {} 不属于 {} 交易所".format(symbol, exchange))


if __name__ == '__main__':
    all_df = get_future_daily_sp(start='2018/10/18', end='2018/10/20', bar_type='5m', symbol='RB1811')
    all_df.to_csv(r'E:\Python_project_in_E\Web_Spider\Commdity_spiders\data\all_df.csv')

