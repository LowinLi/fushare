# -*- coding:utf-8 -*-

"""
Created on 2018年07月18日
@author: lowin
@contact: li783170560@126.com

从大连商品交易所、上海商品交易所、郑州商品交易所、中金交易所爬取前20会员持仓数据
建议下午16点30以后爬取当天数据，避免交易所数据更新不稳定
郑州交易所格式分为三类
"""


import json
from bs4 import BeautifulSoup
from io import StringIO
import datetime
import warnings
from fushare.requests_fun import *
from fushare.symbolVar import *
calendar = cons.get_calendar()

rank_columns = ['vol_party_name', 'vol', 'vol_chg','long_party_name', 'long_openIntr',
   'long_openIntr_chg', 'short_party_name', 'short_openIntr', 'short_openIntr_chg']
intColumns = ['vol', 'vol_chg', 'long_openIntr', 'long_openIntr_chg', 'short_openIntr', 'short_openIntr_chg']


def get_rank_sum_daily(start=None, end=None, vars=cons.vars):
    """
        抓取四个期货交易所前5、前10、前15、前20会员持仓排名数据
        注1：由于上期所和中金所只公布每个品种内部的标的排名，没有公布品种的总排名；
            所以函数输出的品种排名是由品种中的每个标的加总获得，并不是真实的品种排名列表
        注2：大商所只公布了品种排名，未公布标的排名
        Parameters
        ------
            start: 开始日期 format：YYYY-MM-DD 或 YYYYMMDD 或 datetime.date对象 为空时为当天
            end: 结束数据 format：YYYY-MM-DD 或 YYYYMMDD 或 datetime.date对象 为空时为当天
            vars: 合约品种如RB、AL等列表 为空时为所有商品
        Return
        -------
            DataFrame:
                展期收益率数据(DataFrame):
                    symbol                      标的合约                     string
                    var                         商品品种                     string
                    vol_top5                    成交量前5会员成交量总和         int
                    vol_chg_top5                成交量前5会员成交量变化总和      int
                    long_openIntr_top5          持多单前5会员持多单总和         int
                    long_openIntr_chg_top5      持多单前5会员持多单变化总和      int
                    short_openIntr_top5         持空单前5会员持空单总和         int
                    short_openIntr_chg_top5     持空单前5会员持空单变化总和      int 
                    vol_top10                   成交量前10会员成交量总和        int                   
                    ...
                    
                    date                        日期                         string YYYYMMDD
    """
    start = cons.convert_date(start) if start is not None else datetime.date.today()
    end = cons.convert_date(end) if end is not None else cons.convert_date(cons.get_latestDataDate(datetime.datetime.now()))
    records = pd.DataFrame()
    while start <= end:
        print(start)
        if start.strftime('%Y%m%d') in calendar:
            data = get_rank_sum(start, vars)
            if data is False:
                print('%s日交易所数据连接失败，已超过20次，您的地址被网站墙了，请保存好返回数据，稍后从该日期起重试' % start.strftime('%Y-%m-%d'))
                return records.reset_index(drop=True)
            records = records.append(data)
        else:
            warnings.warn('%s非交易日' % start.strftime('%Y%m%d'))
        start += datetime.timedelta(days=1)

    return records.reset_index(drop=True)




def get_rank_sum(date = None,vars=cons.vars):
    """
        抓取四个期货交易所前5、前10、前15、前20会员持仓排名数据
        注1：由于上期所和中金所只公布每个品种内部的标的排名，没有公布品种的总排名；
            所以函数输出的品种排名是由品种中的每个标的加总获得，并不是真实的品种排名列表
        注2：大商所只公布了品种排名，未公布标的排名
        Parameters
        ------
            date: 日期 format：YYYY-MM-DD 或 YYYYMMDD 或 datetime.date对象 为空时为当天
            vars: 合约品种如RB、AL等列表 为空时为所有商品
        Return
        -------
            DataFrame:
                展期收益率数据(DataFrame):
                    symbol                      标的合约                     string
                    var                         商品品种                     string
                    vol_top5                    成交量前5会员成交量总和         int
                    vol_chg_top5                成交量前5会员成交量变化总和      int
                    long_openIntr_top5          持多单前5会员持多单总和         int
                    long_openIntr_chg_top5      持多单前5会员持多单变化总和      int
                    short_openIntr_top5         持空单前5会员持空单总和         int
                    short_openIntr_chg_top5     持空单前5会员持空单变化总和      int 
                    vol_top10                   成交量前10会员成交量总和        int                   
                    ...

                    date                        日期                         string YYYYMMDD
    """
    date = cons.convert_date(date) if date is not None else datetime.date.today()
    if date.strftime('%Y%m%d') not in calendar:
        warnings.warn('%s非交易日' % date.strftime('%Y%m%d'))
        return None
    dce_var = [i for i in vars if i in cons.market_var['dce']]
    shfe_var = [i for i in vars if i in cons.market_var['shfe']]
    czce_var = [i for i in vars if i in cons.market_var['czce']]
    cffex_var = [i for i in vars if i in cons.market_var['cffex']]
    D={}
    if len(dce_var)>0:
        data = get_dce_rank_table(date, dce_var)
        if data is False:
            return False
        D.update(data)
    if len(shfe_var)>0:
        data = get_shfe_rank_table(date, shfe_var)
        if data is False:
            return False
        D.update(data)
    if len(czce_var)>0:
        data = get_czce_rank_table(date, czce_var)
        if data is False:
            return False
        D.update(data)
    if len(cffex_var)>0:
        data = get_cffex_rank_table(date, cffex_var)
        if data is False:
            return False
        D.update(data)
    records=pd.DataFrame()


    for symbol, table in D.items():
        table = table.applymap(lambda x: 0 if x == '' else x)
        for symbol in set(table['symbol']):

            var = symbol2varietie(symbol)
            if var in vars:
                tableCut = table[table['symbol'] == symbol]
                tableCut['rank'] = tableCut['rank'].astype('float')
                tableCut_top5 = tableCut[tableCut['rank'] <= 5]
                tableCut_top10 = tableCut[tableCut['rank'] <= 10]
                tableCut_top15 = tableCut[tableCut['rank'] <= 15]
                tableCut_top20 = tableCut[tableCut['rank'] <= 20]

                D = {'symbol': symbol, 'variety': var,

                     'vol_top5': tableCut_top5['vol'].sum(), 'vol_chg_top5': tableCut_top5['vol_chg'].sum(),
                     'long_openIntr_top5': tableCut_top5['long_openIntr'].sum(),
                     'long_openIntr_chg_top5': tableCut_top5['long_openIntr_chg'].sum(),
                     'short_openIntr_top5': tableCut_top5['short_openIntr'].sum(),
                     'short_openIntr_chg_top5': tableCut_top5['short_openIntr_chg'].sum(),

                     'vol_top10': tableCut_top10['vol'].sum(), 'vol_chg_top10': tableCut_top10['vol_chg'].sum(),
                     'long_openIntr_top10': tableCut_top10['long_openIntr'].sum(),
                     'long_openIntr_chg_top10': tableCut_top10['long_openIntr_chg'].sum(),
                     'short_openIntr_top10': tableCut_top10['short_openIntr'].sum(),
                     'short_openIntr_chg_top10': tableCut_top10['short_openIntr_chg'].sum(),

                     'vol_top15': tableCut_top15['vol'].sum(), 'vol_chg_top15': tableCut_top15['vol_chg'].sum(),
                     'long_openIntr_top15': tableCut_top15['long_openIntr'].sum(),
                     'long_openIntr_chg_top15': tableCut_top15['long_openIntr_chg'].sum(),
                     'short_openIntr_top15': tableCut_top15['short_openIntr'].sum(),
                     'short_openIntr_chg_top15': tableCut_top15['short_openIntr_chg'].sum(),

                     'vol_top20': tableCut_top20['vol'].sum(), 'vol_chg_top20': tableCut_top20['vol_chg'].sum(),
                     'long_openIntr_top20': tableCut_top20['long_openIntr'].sum(),
                     'long_openIntr_chg_top20': tableCut_top20['long_openIntr_chg'].sum(),
                     'short_openIntr_top20': tableCut_top20['short_openIntr'].sum(),
                     'short_openIntr_chg_top20': tableCut_top20['short_openIntr_chg'].sum(),

                     'date': date.strftime('%Y%m%d')
                     }
                records = records.append(pd.DataFrame(D, index=[0]))

    if len(D.items())>0:
        add_vars = [i for i in cons.market_var['shfe']+cons.market_var['cffex'] if i in records['variety'].tolist()]
        for var in add_vars:
            recordsCut = records[records['variety'] == var]
            var_record = pd.DataFrame(recordsCut.sum()).T
            var_record['date'] = date.strftime('%Y%m%d')
            var_record.loc[:,['variety','symbol']] = var
            records = records.append(var_record)

    return records.reset_index(drop=True)

def get_shfe_rank_table(date = None,vars = cons.vars):
    """
        抓取上海商品期货交易所前20会员持仓排名数据明细
        注：该交易所只公布每个品种内部的标的排名，没有公布品种的总排名
        Parameters
        ------
            date: 日期 format：YYYY-MM-DD 或 YYYYMMDD 或 datetime.date对象 为空时为当天
            vars: 合约品种如RB、AL等列表 为空时为所有商品
            数据从20020107开始，每交易日16:30左右更新数据
        Return
        -------
            DataFrame:
                rank                        排名                        int
                vol_party_name              成交量排序的当前名次会员        string(中文)
                vol                         该会员成交量                  int
                vol_chg                     该会员成交量变化量             int
                long_party_name             持多单排序的当前名次会员        string(中文)
                long_openIntr               该会员持多单                  int
                long_openIntr_chg           该会员持多单变化量             int
                short_party_name            持空单排序的当前名次会员        string(中文)
                short_openIntr              该会员持空单                  int
                short_openIntr_chg          该会员持空单变化量             int
                symbol                      标的合约                     string
                var                         品种                        string
                date                        日期                        string YYYYMMDD
    """
    date = cons.convert_date(date) if date is not None else datetime.date.today()
    if date < datetime.date(2002,1,7):
        print("shfe数据源开始日期为20020107，跳过")
        return {}
    if date.strftime('%Y%m%d') not in calendar:
        warnings.warn('%s非交易日' % date.strftime('%Y%m%d'))
        return {}
    url = cons.SHFE_VOLRANK_URL %(date.strftime('%Y%m%d'))
    r = requests_link(url,'utf-8')
    try:
        context = json.loads(r.text)
    except:
        return {}
    df = pd.DataFrame(context['o_cursor'])

    df = df.rename(columns={'CJ1': 'vol', 'CJ1_CHG': 'vol_chg', 'CJ2': 'long_openIntr', 'CJ2_CHG': 'long_openIntr_chg',
                            'CJ3': 'short_openIntr',
                            'CJ3_CHG': 'short_openIntr_chg', 'PARTICIPANTABBR1': 'vol_party_name',
                            'PARTICIPANTABBR2': 'long_party_name',
                            'PARTICIPANTABBR3': 'short_party_name', 'PRODUCTNAME': 'product1', 'RANK': 'rank',
                            'INSTRUMENTID': 'symbol','PRODUCTSORTNO':'product2'})

    if len(df.columns)<3:
        return {}
    df = df.applymap(lambda x: x.strip() if type(x) == type('') else x)
    df = df.applymap(lambda x: None if x == '' else x)
    df['variety'] = df['symbol'].apply(lambda x: symbol2varietie(x))

    df = df[df['rank'] > 0]
    for col in ['PARTICIPANTID1','PARTICIPANTID2','PARTICIPANTID3','product1','product2']:
        try:
            del df[col]
        except:
            pass
    get_vars = [var for var in vars if var in df['variety'].tolist()]
    D={}
    for var in get_vars:
        df_var = df[df['variety'] == var]
        for symbol in set(df_var['symbol']):
            df_symbol = df_var[df_var['symbol'] == symbol]
            D[symbol] = df_symbol.reset_index(drop=True)
    return D



def _czce_df_read(url,skiprow,encode='utf-8'):
    """
        抓取郑州商品期货交易所的网页数据
        Parameters
        ------
            url:        网站         string
            skiprow:    去掉前几行    int
        Return
        -------
            DataFrame
                
    """
    r = requests_link(url,encode)
    data = pd.read_html(r.text, match='.+', flavor=None, header=0, index_col=0, skiprows=skiprow, attrs=None,
                        parse_dates=False,  thousands=', ', encoding="gbk", decimal='.',
                        converters=None, na_values=None, keep_default_na=True)
    return data

def get_czce_rank_table(date = None,vars = cons.vars):
    """
        抓取郑州商品期货交易所前20会员持仓排名数据明细
        注：该交易所即公布了品种排名，也公布了标的排名
        Parameters
        ------
            date: 日期 format：YYYY-MM-DD 或 YYYYMMDD 或 datetime.date对象 为空时为当天
            vars: 合约品种如RB、AL等列表 为空时为所有商品
            数据从20050509开始，每交易日16:30左右更新数据
        Return
        -------
            DataFrame:
                rank                        排名                        int
                vol_party_name              成交量排序的当前名次会员        string(中文)
                vol                         该会员成交量                  int
                vol_chg                     该会员成交量变化量             int
                long_party_name             持多单排序的当前名次会员        string(中文)
                long_openIntr               该会员持多单                  int
                long_openIntr_chg           该会员持多单变化量             int
                short_party_name            持空单排序的当前名次会员        string(中文)
                short_openIntr              该会员持空单                  int
                short_openIntr_chg          该会员持空单变化量             int
                symbol                      标的合约                     string
                var                         品种                        string
                date                        日期                        string YYYYMMDD
    """
    date = cons.convert_date(date) if date is not None else datetime.date.today()
    if date < datetime.date(2005,5,9):
        print("czce数据源开始日期为20050509，跳过")
        return {}
    if date.strftime('%Y%m%d') not in calendar:
        warnings.warn('%s非交易日' % date.strftime('%Y%m%d'))
        return {}
    if date <= datetime.date(2010, 8, 25):
        url = cons.CZCE_VOLRANK_URL_1 % (date.strftime('%Y%m%d'))
        data = _czce_df_read(url,skiprow=0)
        r = requests_link(url,'utf-8')
        r.encoding = 'utf-8'
        soup = BeautifulSoup(r.text, 'lxml', from_encoding="gb2312")
        symbols=[]
        for link in soup.find_all('b'):
            strings = (str(link).split(' '))
            if len(strings)>5:
                try:
                    symbol = chinese_to_english(strings[4])
                except:
                    symbol = strings[4]
                symbols.append(symbol)
        D={}
        for i in range(len(symbols)):
            symbol = symbols[i]
            tableCut = data[i+2]
            tableCut.columns = rank_columns
            tableCut = tableCut.iloc[:-1,:]
            tableCut.loc[:,'rank'] = tableCut.index
            tableCut.loc['合计','rank'] = 999
            tableCut.loc['合计',['vol_party_name','long_party_name','short_party_name']] = None
            tableCut.loc[:,'symbol'] = symbol
            tableCut.loc[:,'variety'] = symbol2varietie(symbol)
            tableCut[intColumns] = tableCut[intColumns].fillna(0)
            tableCut[intColumns] = tableCut[intColumns].astype(str)
            tableCut[intColumns] = tableCut[intColumns].applymap(lambda x: x.replace(',', ''))
            tableCut = tableCut.applymap(lambda x: 0 if x == '-' else x)

            tableCut[intColumns] = tableCut[intColumns].astype(float)
            tableCut[intColumns] = tableCut[intColumns].astype(int)
            D[symbol] = tableCut.reset_index(drop=True)
        return D

    elif date <= datetime.date(2015, 11, 11):
        url = cons.CZCE_VOLRANK_URL_2 % (date.year, date.strftime('%Y%m%d'))
        data = _czce_df_read(url,skiprow=1)[1]
    elif date < datetime.date(2017, 12, 28):
        url = cons.CZCE_VOLRANK_URL_3 % (date.year, date.strftime('%Y%m%d'))
        data = _czce_df_read(url,skiprow=1)[0]
    else:
        url = cons.CZCE_VOLRANK_URL_3 % (date.year, date.strftime('%Y%m%d'))
        data = _czce_df_read(url, skiprow=0)[0]

    if len(data.columns) <6:
        return {}

    table = pd.DataFrame(data.iloc[:, :9])
    table.columns = rank_columns
    table.loc[:,'rank'] = table.index
    table[intColumns] = table[intColumns].astype(str)
    table[intColumns] = table[intColumns].applymap(lambda x: x.replace(',', ''))
    table = table.applymap(lambda x: 0 if x == '-' else x)
    indexs = [i for i in table.index if '合约' in i or '品种' in i]
    indexs.insert(0,0)
    D = {}

    for i in range(len(indexs)):

        if indexs[i] == 0:
            tableCut = table.loc[:indexs[i + 1], :]
            string = tableCut.index.name

        elif i < len(indexs) - 1:
            tableCut = table.loc[indexs[i]:indexs[i + 1], :]
            string = tableCut.index[0]

        else:
            tableCut = table.loc[indexs[i]:, :]
            string = tableCut.index[0]

        if 'PTA' in string:
            symbol ='TA'
        else:
            try:
                symbol = chinese_to_english(find_chinese(re.compile('：(.*) ').findall(string)[0]))
            except:
                symbol = re.compile('：(.*) ').findall(string)[0]

        var = symbol2varietie(symbol)

        if var in vars:

            tableCut = tableCut.dropna(how='any').iloc[1:, :]
            tableCut = tableCut.loc[[x for x in tableCut.index if x in [str(i) for i in range(21)]], :]

            tableCut = _tableCut_cal(tableCut, symbol)
            D[symbol] = tableCut.reset_index(drop=True)

    return D


def get_dce_rank_table(date = None,vars = cons.vars):
    """
        抓取大连商品期货交易所前20会员持仓排名数据明细
        注：该交易所即公布了品种排名，也公布了标的排名
        Parameters
        ------
            date: 日期 format：YYYY-MM-DD 或 YYYYMMDD 或 datetime.date对象 为空时为当天
            vars: 合约品种如RB、AL等列表 为空时为所有商品
            数据从20060104开始，每交易日16:30左右更新数据
        Return
        -------
            DataFrame:
                rank                        排名                        int
                vol_party_name              成交量排序的当前名次会员        string(中文)
                vol                         该会员成交量                  int
                vol_chg                     该会员成交量变化量             int
                long_party_name             持多单排序的当前名次会员        string(中文)
                long_openIntr               该会员持多单                  int
                long_openIntr_chg           该会员持多单变化量             int
                short_party_name            持空单排序的当前名次会员        string(中文)
                short_openIntr              该会员持空单                  int
                short_openIntr_chg          该会员持空单变化量             int
                symbol                      标的合约                     string
                var                         品种                        string
                date                        日期                        string YYYYMMDD
    """
    date = cons.convert_date(date) if date is not None else datetime.date.today()
    if date < datetime.date(2006, 1, 4):
        print(Exception("dce数据源开始日期为20060104，跳过"))
        return {}
    if date.strftime('%Y%m%d') not in calendar:
        warnings.warn('%s非交易日' % date.strftime('%Y%m%d'))
        return {}
    vars = [i for i in vars if i in cons.market_var['dce']]
    D={}
    for var in vars:
        url = cons.DCE_VOLRANK_URL % (var.lower(), var.lower(), date.year, date.month - 1, date.day)

        list_60_name = []
        list_60 = []
        list_60_chg = []
        rank = []

        texts = urllib_request_link(url)
        if texts == None:
            return False
        if len(texts)>30:
            for text in texts:
                line = text.decode('utf8')
                stringlist = line.split()
                try:
                    if int(stringlist[0]) <= 20:
                        list_60_name.append(stringlist[1])
                        list_60.append(stringlist[2])
                        list_60_chg.append(stringlist[3])
                        rank.append(stringlist[0])
                except:
                    pass
            tableCut = pd.DataFrame({'rank': rank[0:20],
                               'vol_party_name': list_60_name[0:20],
                               'vol': list_60[0:20],
                               'vol_chg': list_60_chg[0:20],
                               'long_party_name': list_60_name[20:40],
                               'long_openIntr': list_60[20:40],
                               'long_openIntr_chg': list_60_chg[20:40],
                               'short_party_name': list_60_name[40:60],
                               'short_openIntr': list_60[40:60],
                               'short_openIntr_chg': list_60_chg[40:60]
                               })
            tableCut = tableCut.applymap(lambda x: x.replace(',', ''))
            tableCut = _tableCut_cal(tableCut, var)
            D[var] = tableCut.reset_index(drop=True)
    return D

def get_cffex_rank_table(date = None,vars = cons.vars):
    """
        抓取郑州商品期货交易所前20会员持仓排名数据明细
        注：该交易所即公布了品种排名，也公布了标的排名
        Parameters
        ------
            date: 日期 format：YYYY-MM-DD 或 YYYYMMDD 或 datetime.date对象 为空时为当天
            vars: 合约品种如RB、AL等列表 为空时为所有商品
            数据从20100416开始，每交易日16:30左右更新数据
        Return
        -------
            DataFrame:
                rank                        排名                        int
                vol_party_name              成交量排序的当前名次会员        string(中文)
                vol                         该会员成交量                  int
                vol_chg                     该会员成交量变化量             int
                long_party_name             持多单排序的当前名次会员        string(中文)
                long_openIntr               该会员持多单                  int
                long_openIntr_chg           该会员持多单变化量             int
                short_party_name            持空单排序的当前名次会员        string(中文)
                short_openIntr              该会员持空单                  int
                short_openIntr_chg          该会员持空单变化量             int
                symbol                      标的合约                     string
                var                         品种                        string
                date                        日期                        string YYYYMMDD
    """
    vars = [i for i in vars if i in cons.market_var['cffex']]
    date = cons.convert_date(date) if date is not None else datetime.date.today()
    if date < datetime.date(2010,4,16):
        print(Exception("cffex数据源开始日期为20100416，跳过"))
        return {}
    if date.strftime('%Y%m%d') not in calendar:
        warnings.warn('%s非交易日' % date.strftime('%Y%m%d'))
        return {}
    D={}
    for var in vars:
        url = cons.CFFEX_VOLRANK_URL % (date.strftime('%Y%m'), date.strftime('%d'), var)
        r = requests_link(url,encoding='gbk')
        if r == None:
            return False
        if '网页错误' not in r.text:
            table = pd.read_csv(StringIO(r.text.split('\n交易日,')[1]))
            table = table.dropna(how='any')
            table = table.applymap(lambda x: x.strip() if type(x)==type('') else x)
            for symbol in set(table['合约']):
                tableCut =table[table['合约'] == symbol]
                tableCut.columns = ['symbol','rank']+rank_columns
                tableCut = _tableCut_cal(pd.DataFrame(tableCut),symbol)
                D[symbol] = tableCut.reset_index(drop=True)
    return D

def _tableCut_cal(tableCut, symbol):
    var = symbol2varietie(symbol)
    tableCut[intColumns+['rank']] = tableCut[intColumns+['rank']].astype(int)
    tableCut_sum = tableCut.sum()
    tableCut_sum['rank'] = 999
    for col in ['vol_party_name', 'long_party_name', 'short_party_name']:
        tableCut_sum[col] = None
    tableCut = tableCut.append(pd.DataFrame(tableCut_sum).T,sort = True)
    tableCut['symbol'] = symbol
    tableCut['variety'] = var

    return tableCut


if __name__ == '__main__':
    df = get_rank_sum('20181105')
    print(df)
    #df = get_czce_rank_table(date = '20181105')
    #print(df)
    #df = get_dce_rank_table(date = '20181105')
    #print(df)
    df = get_shfe_rank_table(date = '20181105')
    print(df)
    df = get_cffex_rank_table(date = '20181105')
    print(df)
