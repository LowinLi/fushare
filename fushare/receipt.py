# -*- coding:utf-8 -*-

"""
Created on 2018年07月12日
@author: lowin
@contact: li783170560@126.com

从大连商品交易所、上海商品交易所、郑州商品交易所爬取每日仓单数据
建议下午16点30以后爬取当天数据，避免交易所数据更新不稳定

"""


import json
import datetime
import warnings
from fushare.symbolVar import *
calendar = cons.get_calendar()
from fushare.requests_fun import *
shfe_20100126 = pd.DataFrame({'var':['CU','AL','ZN','RU','FU','AU','RB','WR'],'reciept':[29783,285396,187713,116435,376200,12,145648,0]})
shfe_20101029 = pd.DataFrame({'var':['CU','AL','ZN','RU','FU','AU','RB','WR'],'reciept':[39214,359729,182562,25990,313600,27,36789,0]})
# ----------------------------------------------------------------------
def get_dce_reciept(date = None,vars=cons.vars):
    """
        抓取大连商品交易所注册仓单数据
        Parameters
        ------
            date: 开始日期 format：YYYY-MM-DD 或 YYYYMMDD 或 datetime.date对象 为空时为当天
            vars: 合约品种如RB、AL等列表 为空时为所有商品
            数据从20060106开始，每周五更新仓单数据。直到20090407起，每交易日都更新仓单数据
        Return
        -------
            DataFrame:
                展期收益率数据(DataFrame):
                    var             商品品种                     string
                    reciept         仓单数                       int
                    date            日期                         string YYYYMMDD
    """
    date = cons.convert_date(date) if date is not None else datetime.date.today()
    if date.strftime('%Y%m%d') not in calendar:
        warnings.warn('%s非交易日' % date.strftime('%Y%m%d'))
        return None
    url = cons.DCE_RECIEPT_URL % (date.year, date.month - 1, date.day)
    data = pandas_readHtml_link(url, encoding='utf-8')[0]
    records=pd.DataFrame()
    for x in data.to_dict(orient='records'):
        if type(x[0]) == type('a'):
            if x[0][-2:] == '小计':
                var = x[0][:-2]
                D = {'var':chinese_to_english(var),'reciept':int(x[3]),'reciept_chg':int(x[4]),'date':date.strftime('%Y%m%d')}
                records = records.append(pd.DataFrame(D,index=[0]))
    if len(records.index) != 0:
        records.index = records['var']
        vars_inMarket = [i for i in vars if i in records.index]
        records = records.loc[vars_inMarket, :]
    return records.reset_index(drop=True)

# ----------------------------------------------------------------------
def get_shfe_reciept_1(date = None,vars = cons.vars):
    """
        抓取上海商品交易所注册仓单数据
        适用20081006至20140518(包括)
        20100126、20101029日期交易所格式混乱，直接回复脚本中DataFrame
        20100416、20130821日期交易所数据丢失
        Parameters
        ------
            date: 开始日期 format：YYYY-MM-DD 或 YYYYMMDD 或 datetime.date对象 为空时为当天
            vars: 合约品种如RB、AL等列表 为空时为所有商品
        Return
        -------
            DataFrame:
                展期收益率数据(DataFrame):
                    var             商品品种                     string
                    reciept         仓单数                       int
                    date            日期                         string YYYYMMDD
    """
    date = cons.convert_date(date).strftime('%Y%m%d') if date is not None else datetime.date.today()
    if date not in calendar:
        warnings.warn('%s非交易日' % date.strftime('%Y%m%d'))
        return None
    if date == '20100126':
        shfe_20100126['date']=date
        return shfe_20100126
    elif date == '20101029':
        shfe_20101029['date'] = date
        return shfe_20101029
    elif date in ['20100416','20130821']:
        print(u'20100416、20130821日期交易所数据丢失')
        return None
    else:
        varList = ['天然橡胶', '沥青仓库', '沥青厂库', '热轧卷板', '燃料油', '白银', '线材', '螺纹钢', '铅', '铜', '铝', '锌', '黄金', '锡', '镍']
        url = cons.SHFE_RECIEPT_URL_1 % date

        data = pandas_readHtml_link(url)[0]

        indexs = [x for x in data.index if (data[0].tolist()[x] in varList)]
        lastIndex = [x for x in data.index if '注' in str(data[0].tolist()[x])][0]-1
        records = pd.DataFrame()
        for i in list(range(len(indexs))):
            if i !=len(indexs)-1:
                dataCut = data.loc[indexs[i]:indexs[i+1]-1,:]
            else:
                dataCut = data.loc[indexs[i]:lastIndex,:]
                dataCut = dataCut.fillna(method='pad')
            D={}
            D['var'] = chinese_to_english(dataCut[0].tolist()[0])
            D['reciept'] = int(dataCut[1].tolist()[-1])
            D['reciept_chg'] = int(dataCut[2].tolist()[-1])
            D['date'] = date
            records = records.append(pd.DataFrame(D,index=[0]))
    if len(records.index) != 0:
        records.index = records['var']
        vars_inMarket = [i for i in vars if i in records.index]
        records = records.loc[vars_inMarket, :]
    return records.reset_index(drop=True)



# ----------------------------------------------------------------------
def get_shfe_reciept_2(date = None,vars=None):
    """
        抓取上海商品交易所注册仓单数据
        适用20140519(包括)至今
        Parameters
        ------
            date: 开始日期 format：YYYY-MM-DD 或 YYYYMMDD 或 datetime.date对象 为空时为当天
            vars: 合约品种如RB、AL等列表 为空时为所有商品
        Return
        -------
            DataFrame:
                展期收益率数据(DataFrame):
                    var             商品品种                     string
                    reciept         仓单数                       int
                    date            日期                         string YYYYMMDD
    """
    date = cons.convert_date(date).strftime('%Y%m%d') if date is not None else datetime.date.today()
    if date not in calendar:
        warnings.warn('%s非交易日' % date.strftime('%Y%m%d'))
        return None
    url = cons.SHFE_RECIEPT_URL_2 % date
    r = requests_link(url,encoding='utf-8')
    r.encoding = 'utf-8'
    try:
        context = json.loads(r.text)
    except:
        return pd.DataFrame()
    data = pd.DataFrame(context['o_cursor'])
    if len(data.columns) <1:
        return pd.DataFrame()
    records = pd.DataFrame()
    for var in set(data['VARNAME'].tolist()):
        dataCut = data[data['VARNAME'] == var]
        D = {'var':chinese_to_english(re.sub("\W|[a-zA-Z]", "", var)),'reciept':int(dataCut['WRTWGHTS'].tolist()[-1]),'reciept_chg':int(dataCut['WRTCHANGE'].tolist()[-1]),'date':date}
        records = records.append(pd.DataFrame(D,index=[0]))
    if len(records.index) != 0:
        records.index = records['var']
        vars_inMarket = [i for i in vars if i in records.index]
        records = records.loc[vars_inMarket, :]
    return records.reset_index(drop=True)

# ----------------------------------------------------------------------
def get_czce_reciept_1(date = None, vars=cons.vars):
    """
        抓取郑州商品交易所注册仓单数据
        适用20080222至20100824(包括)
        Parameters
        ------
            date: 开始日期 format：YYYY-MM-DD 或 YYYYMMDD 或 datetime.date对象 为空时为当天
            vars: 合约品种如CF、TA等列表 为空时为所有商品
        Return
        -------
            DataFrame:
                展期收益率数据(DataFrame):
                    var             商品品种                     string
                    reciept         仓单数                       int
                    date            日期                         string YYYYMMDD
    """
    date = cons.convert_date(date).strftime('%Y%m%d') if date is not None else datetime.date.today()
    if date not in calendar:
        warnings.warn('%s非交易日' % date.strftime('%Y%m%d'))
        return None
    if date == '20090820':
        return pd.DataFrame()
    url = cons.CZCE_RECIEPT_URL_1 % date
    r = requests_link(url,encoding='utf-8')
    r.encoding = 'utf-8'
    context = r.text
    data = pd.read_html(context)[1]
    records=pd.DataFrame()
    indexs= [x for x in data.index if '品种：' in str(data[0].tolist()[x])]
    for i in list(range(len(indexs))):
        if i != len(indexs) - 1:
            dataCut = data.loc[indexs[i]:indexs[i + 1] - 1, :]
            dataCut = dataCut.fillna(method='pad')
        else:
            dataCut = data.loc[indexs[i]:, :]
            dataCut = dataCut.fillna(method='pad')
        if 'PTA' in dataCut[0].tolist()[0]:
            var = 'TA'
        else:
            var = chinese_to_english(re.sub('[A-Z]+', '', dataCut[0].tolist()[0][3:]))
        if var == 'CF':
            reciept = dataCut[6].tolist()[-1]
            reciept_chg = dataCut[7].tolist()[-1]
        else:
            reciept =dataCut[5].tolist()[-1]
            reciept_chg = dataCut[6].tolist()[-1]
        D = {'var':var, 'reciept':int(reciept),'reciept_chg':int(reciept_chg), 'date':date}
        records = records.append(pd.DataFrame(D,index=[0]))
    if len(records.index) != 0:
        records.index = records['var']
        vars_inMarket = [i for i in vars if i in records.index]
        records = records.loc[vars_inMarket, :]
    return records.reset_index(drop=True)
# ----------------------------------------------------------------------
def get_czce_reciept_2(date = None,vars = cons.vars):
    """
        抓取郑州商品交易所注册仓单数据
        适用20100825(包括)至20151111(包括)
        Parameters
        ------
            date: 开始日期 format：YYYY-MM-DD 或 YYYYMMDD 或 datetime.date对象 为空时为当天
            vars: 合约品种如CF、TA等列表 为空时为所有商品
        Return
        -------
            DataFrame:
                展期收益率数据(DataFrame):
                    var             商品品种                     string
                    reciept         仓单数                       int
                    date            日期                         string YYYYMMDD
    """
    date = cons.convert_date(date).strftime('%Y%m%d') if date is not None else datetime.date.today()
    if date not in calendar:
        warnings.warn('%s非交易日' % date.strftime('%Y%m%d'))
        return None
    url = cons.CZCE_RECIEPT_URL_2 % (date[:4], date)
    r = requests.get(url)
    r.encoding = 'utf-8'
    data = pd.read_html(r.text)[3:]
    records=pd.DataFrame()
    for dataCut in data:
        if len(dataCut.columns)>3:
            lastIndexs = [x for x in dataCut.index if '注：' in str(dataCut[0].tolist()[x])]
            if len(lastIndexs)>0:
                lastIndex = lastIndexs[0] - 1
                dataCut = dataCut.loc[:lastIndex,:]
            if 'PTA' in dataCut[0].tolist()[0]:
                var = 'TA'
            else:
                strings = dataCut[0].tolist()[0]
                string = strings.split(' ')[0][3:]
                var = chinese_to_english(re.sub('[A-Z]+', '', string))
            dataCut.columns = dataCut.T[1].tolist()
            reciept = dataCut['仓单数量'].tolist()[-1]
            reciept_chg = dataCut['当日增减'].tolist()[-1]
            D = {'var':var, 'reciept':int(reciept),'reciept_chg':int(reciept_chg), 'date':date}
            records = records.append(pd.DataFrame(D,index=[0]))
    if len(records.index) != 0:
        records.index = records['var']
        vars_inMarket = [i for i in vars if i in records.index]
        records = records.loc[vars_inMarket, :]
    return records.reset_index(drop=True)
# ----------------------------------------------------------------------
def get_czce_reciept_3(date = None, vars = cons.vars):
    """
        抓取郑州商品交易所注册仓单数据
        适用20151112(包括)至今
        Parameters
        ------
            date: 开始日期 format：YYYY-MM-DD 或 YYYYMMDD 或 datetime.date对象 为空时为当天
            vars: 合约品种如CF、TA等列表 为空时为所有商品
        Return
        -------
            DataFrame:
                展期收益率数据(DataFrame):`1
                    var             商品品种                     string
                    reciept         仓单数                       int
                    date            日期                         string YYYYMMDD
    """

    date = cons.convert_date(date).strftime('%Y%m%d') if date is not None else datetime.date.today()
    if date not in calendar:
        warnings.warn('%s非交易日' % date.strftime('%Y%m%d'))
        return None
    url = cons.CZCE_RECIEPT_URL_3 % (date[:4], date)
    r = requests_link(url,encoding='utf-8')
    r.encoding = 'utf-8'
    data = pd.read_html(r.text, encoding='gb2312')
    records=pd.DataFrame()
    if len(data) < 4:
        return records
    if int(date) <= 20171227:
        data = data[1:]
    for dataCut in data:
        if len(dataCut.columns) > 3:
            lastIndexs = [x for x in dataCut.index if '注：' in str(dataCut[0].tolist()[x])]
            if len(lastIndexs) > 0:
                lastIndex = lastIndexs[0] - 1
                dataCut = dataCut.loc[:lastIndex, :]
            if 'PTA' in dataCut[0].tolist()[0]:
                var = 'TA'
            else:
                strings = dataCut[0].tolist()[0]
                string = strings.split(' ')[0][3:]
                var = chinese_to_english(re.sub('[A-Z]+', '', string))
            dataCut.columns = dataCut.loc[1,:]
            dataCut = dataCut.fillna(method='pad')
            try:
                reciept = dataCut.loc[:, '仓单数量'].tolist()[-1]
            except:
                reciept = dataCut.loc[:, '仓单数量(保税)'].tolist()[-1]
            reciept_chg = dataCut.loc[:, '当日增减'].tolist()[-1]
            D = {'var': var, 'reciept': int(reciept),'reciept_chg':int(reciept_chg), 'date': date}
            records = records.append(pd.DataFrame(D, index=[0]))
    if len(records.index) != 0:
        records.index = records['var']
        vars_inMarket = [i for i in vars if i in records.index]
        records = records.loc[vars_inMarket, :]
    return records.reset_index(drop=True)

# ----------------------------------------------------------------------
def get_reciept(start=None, end=None, vars=cons.vars):
    """
        获取大宗商品注册仓单数量
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
                    reciept         仓单数量                     int
                    date            日期                        string YYYYMMDD
    """
    start = cons.convert_date(start) if start is not None else datetime.date.today()
    end = cons.convert_date(end) if end is not None else cons.convert_date(cons.get_latestDataDate(datetime.datetime.now()))
    records=pd.DataFrame()
    while start <= end:
        if start.strftime('%Y%m%d') not in calendar:
            warnings.warn('%s非交易日' % start.strftime('%Y%m%d'))
        else:
            print(start)
            for market,marketVars in cons.market_var.items():

                if market == 'dce':
                    if start >= datetime.date(2009,4,7):
                        f = get_dce_reciept
                    else:
                        print(u'20090407起，dce每交易日更新仓单数据')
                        f = None
                elif market == 'shfe':
                    if start <= datetime.date(2014,5,16) and start >= datetime.date(2008,10,6):
                        f = get_shfe_reciept_1
                    elif start > datetime.date(2014,5,16):
                        f = get_shfe_reciept_2
                    else:
                        f=None
                        print(u'20081006起，shfe每交易日更新仓单数据')

                elif market == 'czce':
                    if start <= datetime.date(2010,8,24) and start >= datetime.date(2008,3,3):
                        f = get_czce_reciept_1
                    elif start <= datetime.date(2015,11,11) and start > datetime.date(2010,8,24):
                        f = get_czce_reciept_2
                    elif start > datetime.date(2015,11,11):
                        f = get_czce_reciept_3
                    else:
                        f=None
                        print(u'20080303起，czce每交易日更新仓单数据')


                get_vars = [var for var in vars if var in marketVars]

                if market != 'cffex' and get_vars != []:
                    if f is not None:
                        records = records.append(f(start,get_vars))

        start += datetime.timedelta(days=1)
    return records.reset_index(drop=True)

if __name__ == '__main__':
    d = get_reciept('20181128')
    print(d)
