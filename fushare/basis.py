# -*- coding:utf-8 -*-
'''
Created on 2018年07月12日
@author: lowin
@contact: li783170560@126.com

从生意社网站爬取大宗商品现货价格，及相应基差
网站数据含有20110104至今
'''



import requests

import pandas as pd
import datetime
import time
import warnings
from fushare.symbolVar import *
calendar = cons.get_calendar()

def get_spotPrice_daily(start = None, end = None, vars = cons.vars):
    """
        获取大宗商品现货价格，及相应基差
    Parameters
    ------
        start: 开始日期 format：YYYY-MM-DD 或 YYYYMMDD 或 datetime.date对象 为空时为当天
        end: 结束数据 format：YYYY-MM-DD 或 YYYYMMDD 或 datetime.date对象 为空时为当天
        vars: 合约品种如RB、AL等列表 为空时为所有商品
    Return
    -------
        DataFrame
            展期收益率数据(DataFrame):
                var             商品品种                     string
                SP              现货价格                     float
                nearSymbol      临近交割合约                  string
                nearPrice       临近交割合约结算价             float
                domSymbol       主力合约                     string
                domPrice        主力合约结算价                float
                nearBasis       临近交割合约相对现货的基差       float
                domBasis        主力合约相对现货的基差          float
                nearBasisRate   临近交割合约相对现货的基差率     float
                domBasisRate    主力合约相对现货的基差率        float
                date            日期                        string YYYYMMDD
    """

    start = cons.convert_date(start) if start is not None else datetime.date.today()
    end = cons.convert_date(end) if end is not None else cons.convert_date(cons.get_latestDataDate(datetime.datetime.now()))
    df_list=[]
    while start <= end:
        print(start)
        df = get_spotPrice(start,vars)
        if df is False:
            return pd.concat(df_list).reset_index(drop=True)
        elif df is not None:
            df_list.append(df)
        start += datetime.timedelta(days = 1)

    if len(df_list) > 0:
        return pd.concat(df_list).reset_index(drop=True)


def get_spotPrice(date = None,vars = cons.vars):
    """
        获取某一天大宗商品现货价格，及相应基差
    Parameters
    ------
        date: 开始日期 format：YYYY-MM-DD 或 YYYYMMDD 或 datetime.date对象 为空时为当天
        vars: 合约品种如RB、AL等列表 为空时为所有商品
    Return
    -------
        DataFrame
            展期收益率数据(DataFrame):
                var             商品品种                     string
                SP              现货价格                     float
                nearSymbol      临近交割合约                  string
                nearPrice       临近交割合约结算价             float
                domSymbol       主力合约                     string
                domPrice        主力合约结算价                float
                nearBasis       临近交割合约相对现货的基差      float
                domBasis        主力合约相对现货的基差         float
                nearBasisRate   临近交割合约相对现货的基差率    float
                domBasisRate    主力合约相对现货的基差率       float
                date            日期                       string YYYYMMDD
    """
    date = cons.convert_date(date) if date is not None else datetime.date.today()
    if date < datetime.date(2011,1,4):
        raise Exception("数据源开始日期为20110104，请修改获取数据时段检查")
    if date.strftime('%Y%m%d') not in calendar:
        warnings.warn('%s非交易日' % date.strftime('%Y%m%d'))
        return None
    u1 = cons.SYS_SPOTPRICE_LATEST_URL
    u2 = cons.SYS_SPOTPRICE_URL %date.strftime('%Y-%m-%d')
    i = 1
    while True:
        for url in [u2,u1]:
            try:
                r=requests.get(url,timeout=2)
                string = pd.read_html(r.text)[0].loc[1,1]

                news = ''.join(re.findall(r'[0-9]',string))
                if news[3:11] == date.strftime('%Y%m%d'):

                    records = _check_information(pd.read_html(r.text)[1],date)
                    records.index = records['var']
                    vars_inMarket = [i for i in vars if i in records.index]
                    return records.loc[vars_inMarket,:].reset_index(drop=True)
                else:
                    time.sleep(3)
            except Exception as e:
                print('%s日生意社数据连接失败，第%s次尝试，最多5次' % (date.strftime('%Y-%m-%d'), str(i)))
                i+=1
                if i > 5:
                    print('%s日生意社数据连接失败，已超过5次，您的地址被网站墙了，请保存好返回数据，稍后从该日期起重试' % date.strftime('%Y-%m-%d'))
                    return False


def _check_information(df, date):
    df = df.loc[:, [0, 1, 2, 3, 7, 8]]
    df.columns = ['var', 'SP', 'nearSymbol', 'nearPrice', 'domSymbol', 'domPrice']
    records=pd.DataFrame()
    for string in df['var'].tolist():
        if string == 'PTA':
            news = 'PTA'
        else:
            news = ''.join(re.findall(r'[\u4e00-\u9fa5]', string))
        if news != '' and news not in ['商品', '价格', '上海期货交易所', '郑州商品交易所', '大连商品交易所']:
            var = chinese_to_english(news)
            record = pd.DataFrame(df[df['var'] == string])
            record.loc[:,'var'] = var
            record.loc[:,'SP'] = record.loc[:,'SP'].astype(float)
            if var == 'JD':
                record.loc[:,'SP'] = float(record['SP']) * 500
            if var == 'FG':
                record.loc[:,'SP'] = record['SP'] * 80
            records = records.append(record)


    records.loc[:, ['nearPrice', 'domPrice', 'SP']] = records.loc[:, ['nearPrice', 'domPrice', 'SP']].astype(
        'float')

    records.loc[:, 'nearSymbol'] = records['nearSymbol'].replace('[^0-9]*(\d*)$', '\g<1>', regex=True)
    records.loc[:, 'domSymbol'] = records['domSymbol'].replace('[^0-9]*(\d*)$', '\g<1>', regex=True)

    records.loc[:, 'nearSymbol'] = records['var'] + records.loc[:, 'nearSymbol'].astype('int').astype('str')
    records.loc[:, 'domSymbol'] = records['var'] + records.loc[:, 'domSymbol'].astype('int').astype('str')

    records['nearSymbol'] = records['nearSymbol'].apply(lambda x: x.lower() if x[:-4] in cons.market_var['shfe']+cons.market_var['dce'] else x)
    records.loc[:,'domSymbol'] = records.loc[:,'domSymbol'].apply(lambda x: x.lower() if x[:-4] in cons.market_var['shfe']+cons.market_var['dce'] else x)
    records.loc[:,'nearSymbol'] = records.loc[:,'nearSymbol'].apply(lambda x: x[:-4]+x[-3:] if x[:-4] in cons.market_var['czce'] else x)
    records.loc[:,'domSymbol'] = records.loc[:,'domSymbol'].apply(lambda x: x[:-4]+x[-3:] if x[:-4] in cons.market_var['czce'] else x)

    records['nearBasis'] = records['nearPrice'] - records['SP']
    records['domBasis'] = records['domPrice'] - records['SP']
    records['nearBasisRate'] = records['nearPrice']/records['SP']-1
    records['domBasisRate'] = records['domPrice']/records['SP']-1
    records.loc[:, 'date'] = date.strftime('%Y%m%d')
    return records




if __name__ == '__main__':
    df = get_spotPrice_daily(start ='20181108', end ='20181110')
    print(df)

