# -*- coding:utf-8 -*-
'''
Created on 2018年08月18日
@author: lowin
@contact: li783170560@126.com

从交易所网站获取日线行情
'''

import json
import datetime
from bs4 import BeautifulSoup
import pandas as pd
import numpy as np
from fushare import cons
import requests
import warnings


calendar = cons.get_calendar()

try:
    from urllib.request import urlopen, Request
    from urllib.parse import urlencode
    from urllib.error import HTTPError
    from http.client import IncompleteRead
except ImportError:
    from urllib import urlencode
    from urllib2 import urlopen, Request
    from urllib2 import HTTPError
    from httplib import IncompleteRead


def get_cffex_daily(date=None):
    """
        获取中金所日交易数据
    Parameters
    ------
        date: 日期 format：YYYY-MM-DD 或 YYYYMMDD 或 datetime.date对象 为空时为当天
    Return
    -------
        DataFrame
            中金所日交易数据(DataFrame):
                symbol        合约代码
                date          日期
                open          开盘价
                high          最高价
                low          最低价
                close         收盘价
                volume        成交量
                open_interest   持仓量
                turnover      成交额
                settle        结算价
                pre_settle    前结算价
                variety       合约类别
        或 None(给定日期没有交易数据)
    """
    day = cons.convert_date(date) if date is not None else datetime.date.today()
    if day.strftime('%Y%m%d') not in calendar:
        warnings.warn('%s非交易日' %day.strftime('%Y%m%d'))
        return None
    try:
        html = urlopen(Request(cons.CFFEX_DAILY_URL % (day.strftime('%Y%m'),
                                                     day.strftime('%d'), day.strftime('%Y%m%d')),
                               headers=cons.headers)).read().decode('gbk', 'ignore')
    except HTTPError as reason:
        if reason.code != 404:
            print(cons.CFFEX_DAILY_URL % (day.strftime('%Y%m'), day.strftime('%d'),
                                        day.strftime('%Y%m%d')), reason)
        return

    if html.find(u'网页错误') >= 0:
        return
    html = [i.replace(' ', '').split(',') for i in html.split('\n')[:-2] if i[0][0] != u'小']

    if html[0][0] != u'合约代码':
        return

    dict_data = list()
    day_const = day.strftime('%Y%m%d')
    for row in html[1:]:
        m = cons.FUTURE_SYMBOL_PATTERN.match(row[0])
        if not m:
            continue
        row_dict = {'date': day_const, 'symbol': row[0], 'variety': m.group(1)}

        for i, field in enumerate(cons.CFFEX_COLUMNS):
            if row[i + 1] == u"":
                row_dict[field] = 0.0
            elif field in ['volume', 'open_interest', 'oi_chg']:
                row_dict[field] = int(row[i + 1])
            else:
                try:
                    row_dict[field] = float(row[i + 1])
                except:
                    pass
        row_dict['pre_settle'] = row_dict['close'] - row_dict['change1']
        dict_data.append(row_dict)

    return pd.DataFrame(dict_data)[cons.OUTPUT_COLUMNS]


def get_czce_daily(date=None):

    """
        获取郑商所日交易数据
    Parameters
    ------
        date: 日期 format：YYYY-MM-DD 或 YYYYMMDD 或 datetime.date对象 为空时为当天
    Return
    -------
        DataFrame
            郑商所每日期货交易数据:
                symbol        合约代码
                date          日期
                open          开盘价
                high          最高价
                low           最低价
                close         收盘价
                volume        成交量
                open_interest 持仓量
                turnover      成交额
                settle        结算价
                pre_settle    前结算价
                variety       合约类别
        或 
        DataFrame
           郑商所每日期权交易数据
                symbol        合约代码
                date          日期
                open          开盘价
                high          最高价
                low           最低价
                close         收盘价
                pre_settle      前结算价
                settle         结算价
                delta          对冲值  
                volume         成交量
                open_interest     持仓量
                oi_change       持仓变化
                turnover        成交额
                implied_volatility 隐含波动率
                exercise_volume   行权量
                variety        合约类别
        None(类型错误或给定日期没有交易数据)
    """
    day = cons.convert_date(date) if date is not None else datetime.date.today()
    if day.strftime('%Y%m%d') not in calendar:
        warnings.warn('%s非交易日' %day.strftime('%Y%m%d'))
        return None
    if day > datetime.date(2010, 8, 24):
        if day > datetime.date(2015,9,19):
            u = cons.CZCE_DAILY_URL_3
            url = u % (day.strftime('%Y'), day.strftime('%Y%m%d'))
        elif day < datetime.date(2015,9,19):
            u = cons.CZCE_DAILY_URL_2
            url = u % (day.strftime('%Y'), day.strftime('%Y%m%d'))
        listed_columns = cons.CZCE_COLUMNS
        output_columns = cons.OUTPUT_COLUMNS
        try:
            r = requests.get(url)
            html = r.text
        except HTTPError as reason:
            if reason.code != 404:
                print(cons.CZCE_DAILY_URL % (day.strftime('%Y'),
                                           day.strftime('%Y%m%d')), reason)
            return
        if html.find(u'您的访问出错了') >= 0 or html.find(u'无期权每日行情交易记录') >= 0:
            return
        html = [i.replace(' ', '').split('|') for i in html.split('\n')[:-4] if i[0][0] != u'小']


        if day > datetime.date(2015, 9, 19):
            if html[1][0] not in [u'品种月份', u'品种代码']:
                return
            dict_data = list()
            day_const = int(day.strftime('%Y%m%d'))
            for row in html[2:]:
                m = cons.FUTURE_SYMBOL_PATTERN.match(row[0])
                if not m:
                    continue
                row_dict = {'date': day_const, 'symbol': row[0], 'variety': m.group(1)}
                for i, field in enumerate(listed_columns):
                    if row[i + 1] == "\r":
                        row_dict[field] = 0.0
                    elif field in ['volume', 'open_interest', 'oi_chg', 'exercise_volume']:
                        row[i + 1] = row[i + 1].replace(',', '')
                        row_dict[field] = int(row[i + 1])
                    else:
                        row[i + 1] = row[i + 1].replace(',', '')
                        row_dict[field] = float(row[i + 1])
                dict_data.append(row_dict)

            return pd.DataFrame(dict_data)[output_columns]
        elif day < datetime.date(2015, 9, 19):
            dict_data = list()
            day_const = int(day.strftime('%Y%m%d'))
            for row in html[1:]:
                row = row[0].split(',')
                m = cons.FUTURE_SYMBOL_PATTERN.match(row[0])
                if not m:
                    continue
                row_dict = {'date': day_const, 'symbol': row[0], 'variety': m.group(1)}
                for i, field in enumerate(listed_columns):
                    if row[i + 1] == "\r":
                        row_dict[field] = 0.0
                    elif field in ['volume', 'open_interest', 'oi_chg', 'exercise_volume']:
                        row_dict[field] = int(float(row[i + 1]))
                    else:
                        row_dict[field] = float(row[i + 1])
                dict_data.append(row_dict)
            return pd.DataFrame(dict_data)[output_columns]

    if day <= datetime.date(2010,8,24):
        u = cons.CZCE_DAILY_URL_1
        url = u %  day.strftime('%Y%m%d')
        listed_columns = cons.CZCE_COLUMNS_2
        output_columns = cons.OUTPUT_COLUMNS
        df = pd.read_html(url)[1].dropna(how='any')

        dict_data = list()
        day_const = int(day.strftime('%Y%m%d'))

        for row in df.to_dict(orient = 'records')[1:]:
            m = cons.FUTURE_SYMBOL_PATTERN.match(row[0])
            if not m:
                continue
            row_dict = {'date': day_const, 'symbol': row[0], 'variety': m.group(1)}
            for i, field in enumerate(listed_columns):
                if row[i + 1] == "\r":
                    row_dict[field] = 0.0
                elif field in ['volume', 'open_interest', 'oi_chg', 'exercise_volume']:

                    row_dict[field] = int(row[i + 1])
                else:

                    row_dict[field] = float(row[i + 1])
            dict_data.append(row_dict)

        return pd.DataFrame(dict_data)[output_columns]





def get_shfe_vwap(date=None):
    """
        获取上期所日成交均价数据
    Parameters
    ------
        date: 日期 format：YYYY-MM-DD 或 YYYYMMDD 或 datetime.date对象 为空时为当天
    Return
    -------
        DataFrame
            郑商所日交易数据(DataFrame):
                symbol        合约代码
                date          日期
                time_range    vwap时段，分09:00-10:15和09:00-15:00两类
                vwap          加权平均成交均价
        或 None(给定日期没有数据)
    """
    day = cons.convert_date(date) if date is not None else datetime.date.today()
    if day.strftime('%Y%m%d') not in calendar:
        warnings.warn('%s非交易日' %day.strftime('%Y%m%d'))
        return None
    try:
        json_data = json.loads(urlopen(Request(cons.SHFE_VWAP_URL % (day.strftime('%Y%m%d')),
                                               headers=cons.headers)).read().decode('utf8'))
    except HTTPError as reason:
        if reason.code not in [404,403]:
            print(cons.SHFE_DAILY_URL % (day.strftime('%Y%m%d')), reason)
        return None

    if len(json_data['o_currefprice']) == 0:
        return None
    try:
        df = pd.DataFrame(json_data['o_currefprice'])
        df['INSTRUMENTID'] = df['INSTRUMENTID'].str.strip()
        df[':B1'].astype('int16')
        return df.rename(columns=cons.SHFE_VWAP_COLUMNS)[list(cons.SHFE_VWAP_COLUMNS.values())]
    except:
        return None


def get_shfe_daily(date=None):
    """
        获取上期所日交易数据
    Parameters
    ------
        date: 日期 format：YYYY-MM-DD 或 YYYYMMDD 或 datetime.date对象 为空时为当天
    Return
    -------
        DataFrame
            上期所日交易数据(DataFrame):
                symbol        合约代码
                date          日期
                open          开盘价
                high          最高价
                low           最低价
                close         收盘价
                volume        成交量
                open_interest 持仓量
                turnover      成交额
                settle        结算价
                pre_settle     前结算价
                variety       合约类别
        或 None(给定日期没有交易数据)
    """
    day = cons.convert_date(date) if date is not None else datetime.date.today()
    if day.strftime('%Y%m%d') not in calendar:
        warnings.warn('%s非交易日' %day.strftime('%Y%m%d'))
        return None
    try:
        json_data = json.loads(urlopen(Request(cons.SHFE_DAILY_URL % (day.strftime('%Y%m%d')),
                                               headers=cons.shfe_headers)).read().decode('utf8'))
    except HTTPError as reason:
        if reason.code != 404:
            print(cons.SHFE_DAILY_URL % (day.strftime('%Y%m%d')), reason)
        return

    if len(json_data['o_curinstrument']) == 0:
        return

    df = pd.DataFrame(
        [row for row in json_data['o_curinstrument'] if row['DELIVERYMONTH'] not in [u'小计',u'合计'] and row['DELIVERYMONTH'] != ''])
    df['variety'] = df.PRODUCTID.str.slice(0, -6).str.upper()
    df['symbol'] = df['variety'] + df['DELIVERYMONTH']
    df['date'] = day.strftime('%Y%m%d')
    vwap_df = get_shfe_vwap(day)
    if vwap_df is not None:
        df = pd.merge(df, vwap_df[vwap_df.time_range == '9:00-15:00'], on=['date', 'symbol'], how='left')
        df['turnover'] = df.vwap * df.VOLUME
    else:
        df['turnover'] = df['VOLUME']*df['SETTLEMENTPRICE']
    df.rename(columns=cons.SHFE_COLUMNS, inplace=True)
    return df[cons.OUTPUT_COLUMNS]


def get_dce_daily(date=None, type="future", retries=0):
    """
        获取大连商品交易所日交易数据
    Parameters
    ------
        date: 日期 format：YYYY-MM-DD 或 YYYYMMDD 或 datetime.date对象 为空时为当天
        type: 数据类型, 为'future'期货 或 'option'期权二者之一
        retries: int, 当前重试次数，达到3次则获取数据失败
    Return
    -------
        DataFrame
            大商所日交易数据(DataFrame):
                symbol        合约代码
                date          日期
                open          开盘价
                high          最高价
                low           最低价
                close         收盘价
                volume        成交量
                open_interest   持仓量
                turnover       成交额
                settle        结算价
                pre_settle    前结算价
                variety       合约类别
        或 
        DataFrame
           郑商所每日期权交易数据
                symbol        合约代码
                date          日期
                open          开盘价
                high          最高价
                low           最低价
                close         收盘价
                pre_settle      前结算价
                settle         结算价
                delta          对冲值  
                volume         成交量
                open_interest     持仓量
                oi_change       持仓变化
                turnover        成交额
                implied_volatility 隐含波动率
                exercise_volume   行权量
                variety        合约类别
        或 None(给定日期没有交易数据)
    """
    day = cons.convert_date(date) if date is not None else datetime.date.today()
    if day.strftime('%Y%m%d') not in calendar:
        warnings.warn('%s非交易日' %day.strftime('%Y%m%d'))
        return None
    if retries > 3:
        print("maximum retires for DCE market data: ", day.strftime("%Y%m%d"))
        return

    if type == 'future':
        url = cons.DCE_DAILY_URL + '?' + urlencode({"currDate": day.strftime('%Y%m%d'),
                                                  "year": day.strftime('%Y'),
                                                  "month": str(int(day.strftime('%m')) - 1),
                                                  "day": day.strftime('%d')})
        listed_columns = cons.DCE_COLUMNS
        output_columns = cons.OUTPUT_COLUMNS
    elif type == 'option':
        url = cons.DCE_DAILY_URL + '?' + urlencode({"currDate": day.strftime('%Y%m%d'),
                                                  "year": day.strftime('%Y'),
                                                  "month": str(int(day.strftime('%m')) - 1),
                                                  "day": day.strftime('%d'),
                                                  "dayQuotes.trade_type": "1"})
        listed_columns = cons.DCE_OPTION_COLUMNS
        output_columns = cons.OPTION_OUTPUT_COLUMNS
    else:
        print('invalid type :' + type + ', should be one of "future" or "option"')
        return

    try:
        response = urlopen(Request(url, method='POST', headers=cons.headers)).read().decode('utf8')
    except IncompleteRead as reason:
        return get_dce_daily(day, retries=retries + 1)
    except HTTPError as reason:
        if reason.code == 504:
            return get_dce_daily(day, retries=retries + 1)
        elif reason.code != 404:
            print(cons.DCE_DAILY_URL, reason)
        return

    if u'错误：您所请求的网址（URL）无法获取' in response:
        return get_dce_daily(day, retries=retries + 1)
    elif u'暂无数据' in response:
        return

    data = BeautifulSoup(response, 'html.parser').find_all('tr')
    if len(data) == 0:
        return

    dict_data = list()
    implied_data = list()
    for idata in data[1:]:
        if u'小计' in idata.text or u'总计' in idata.text:
            continue
        x = idata.find_all('td')
        if type == 'future':
            row_dict = {'variety': cons.DCE_MAP[x[0].text.strip()]}
            row_dict['symbol'] = row_dict['variety'] + x[1].text.strip()
            for i, field in enumerate(listed_columns):
                field_content = x[i + 2].text.strip()
                if '-' in field_content:
                    row_dict[field] = 0
                elif field in ['volume', 'open_interest']:
                    row_dict[field] = int(field_content.replace(',', ''))
                else:
                    row_dict[field] = float(field_content.replace(',', ''))
            dict_data.append(row_dict)
        elif len(x) == 16:
            m = cons.FUTURE_SYMBOL_PATTERN.match(x[1].text.strip())
            if not m:
                continue
            row_dict = {'symbol': x[1].text.strip(), 'variety': m.group(1).upper(), 'contract_id': m.group(0)}
            for i, field in enumerate(listed_columns):
                field_content = x[i + 2].text.strip()
                if '-' in field_content:
                    row_dict[field] = 0
                elif field in ['volume', 'open_interest']:
                    row_dict[field] = int(field_content.replace(',', ''))
                else:
                    row_dict[field] = float(field_content.replace(',', ''))
            dict_data.append(row_dict)
        elif len(x) == 2:
            implied_data.append({'contract_id': x[0].text.strip(), 'implied_volatility': float(x[1].text.strip())})
    df = pd.DataFrame(dict_data)
    df['date'] = day.strftime('%Y%m%d')
    if type == 'future':
        return df[output_columns]
    else:
        return pd.merge(df, pd.DataFrame(implied_data), on='contract_id', how='left', indicator=False)[output_columns]


def get_future_daily(start=None, end=None, market='CFFEX', indexBar = False):
    """
        获取交易所日交易数据
    Parameters
    ------
        start: 开始日期 format：YYYY-MM-DD 或 YYYYMMDD 或 datetime.date对象 为空时为当天
        end: 结束数据 format：YYYY-MM-DD 或 YYYYMMDD 或 datetime.date对象 为空时为当天
        market: 'CFFEX' 中金所, 'CZCE' 郑商所,  'SHFE' 上期所, 'DCE' 大商所 之一。默认为中金所
        indexBar: bool  是否合成指数K线
    Return
    -------
        DataFrame
            中金所日交易数据(DataFrame):
                symbol      合约代码
                date       日期
                open       开盘价
                high       最高价
                low       最低价
                close      收盘价
                volume      成交量
                open_interest 持仓量
                turnover    成交额
                settle     结算价
                pre_settle   前结算价
                variety     合约类别
        或 None(给定日期没有交易数据)
    """
    if market.upper() == 'CFFEX':
        f = get_cffex_daily
    elif market.upper() == 'CZCE':
        f = get_czce_daily
    elif market.upper() == 'SHFE':
        f = get_shfe_daily
    elif market.upper() == 'DCE':
        f = get_dce_daily
    else:
        print('Invalid market.')
        return

    start = cons.convert_date(start) if start is not None else datetime.date.today()
    end = cons.convert_date(end) if end is not None else cons.convert_date(cons.get_latestDataDate(datetime.datetime.now()))

    df_list = list()
    while start <= end:
        df = f(start)
        if df is not None:
            df_list.append(df)
            if indexBar:
                df_list.append(get_futureIndex(df))
        start += datetime.timedelta(days=1)

    if len(df_list) > 0:
        return pd.concat(df_list).reset_index(drop = True)

def get_futureIndex(df):
    """
        获取指数日交易数据
    Parameters
    ------
        df: 爬到的原始合约日线行情    dataframe
    Return
    -------
        df: 持仓量加权指数日线行情
        DataFrame
            中金所日交易数据(DataFrame):
                symbol      合约代码
                date       日期
                open       开盘价
                high       最高价
                low       最低价
                close      收盘价
                volume      成交量
                open_interest 持仓量
                turnover    成交额
                settle     结算价
                pre_settle   前结算价
                variety     合约类别
    """
    index_dfs = []
    for var in set(df['variety']):
        dfCut = df[df['variety'] == var]
        dfCut = dfCut[dfCut['open_interest'] != 0]
        if len(dfCut.index)>0:
            index_df = pd.Series(index = dfCut.columns)
            index_df[['volume','open_interest','turnover']] = dfCut[['volume','open_interest','turnover']].sum()
            index_df[['open','high','low','close','settle','pre_settle']] = np.dot(np.array(dfCut[['open','high','low','close','settle','pre_settle']]).T, np.array((dfCut['open_interest'])))/np.sum(dfCut['open_interest'])
            index_df[['date','variety']] = dfCut[['date','variety']].iloc[0,:]
            index_df['symbol'] = index_df['variety'] + '99'
            index_dfs.append(index_df)
    return pd.concat(index_dfs,axis = 1).T

if __name__ == '__main__':
    d = get_future_daily(start='20180301', end='20190107', market='CZCE', indexBar = True)
    print(d)