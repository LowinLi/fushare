import re
import datetime
import json
import os

market_var = {'cffex': ['IF','IC','IH','T','TF','TS'],
'dce':['C','CS','A','B','M','Y','P','FB','BB','JD','L','V','PP','J','JM','I','EG'],
'czce':['WH','PM','CF','SR','TA','OI','RI','MA','ME','FG','RS','RM','ZC','JR','LR','SF','SM','WT','TC','GN','RO','ER','SRX','SRY','WSX','WSY','CY','AP'],
'shfe':['CU','AL','ZN','PB','NI','SN','AU','AG','RB','WR','HC','FU','BU','RU','SC','SP']
}

vars=[]
[vars.extend(i) for i in market_var.values()]




headers = {'Host': 'www.czce.com.cn',
           'Connection': 'keep-alive',
           'Cache-Control': 'max-age=0',
           'Accept': 'text/html, */*; q=0.01',
           'X-Requested-With': 'XMLHttpRequest',
           'User-Agent': 'Mozilla/5.0 (Windows NT 6.1; WOW64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/56.0.2924.87 Safari/537.36',
           'DNT': '1',
           'Referer': 'http://www.super-ping.com/?ping=www.google.com&locale=sc',
           'Accept-Encoding': 'gzip, deflate, sdch',
           'Accept-Language': 'zh-CN,zh;q=0.8,ja;q=0.6'
           }
shfe_headers = {'User-Agent': 'Mozilla/4.0 (compatible; MSIE 5.5; Windows NT)'}

SYS_SPOTPRICE_URL = 'http://www.100ppi.com/sf/day-%s.html'
SYS_SPOTPRICE_LATEST_URL = 'http://www.100ppi.com/sf/'

SHFE_VOLRANK_URL = 'http://www.shfe.com.cn/data/dailydata/kx/pm%s.dat'
CFFEX_VOLRANK_URL = 'http://www.cffex.com.cn/fzjy/ccpm/%s/%s/%s_1.csv'
DCE_VOLRANK_URL = 'http://www.dce.com.cn/publicweb/quotesdata/exportMemberDealPosiQuotesData.html?memberDealPosiQuotes.variety=%s&memberDealPosiQuotes.trade_type=0&contract.contract_id=all&contract.variety_id=%s&year=%s&month=%s&day=%s&exportFlag=txt'
CZCE_VOLRANK_URL_1 = 'http://www.czce.com.cn/cn/exchange/jyxx/pm/pm%s.html'
CZCE_VOLRANK_URL_2 = 'http://www.czce.com.cn/cn/exchange/%s/datatradeholding/%s.htm'
CZCE_VOLRANK_URL_3 = 'http://www.czce.com.cn/cn/DFSStaticFiles/Future/%s/%s/FutureDataHolding.htm'

DCE_RECIEPT_URL = 'http://www.dce.com.cn/publicweb/quotesdata/wbillWeeklyQuotes.html?wbillWeeklyQuotes.variety=all&year=%s&month=%s&day=%s'
SHFE_RECIEPT_URL_1 = 'http://www.shfe.com.cn/data/dailydata/%sdailystock.html'
SHFE_RECIEPT_URL_2 = 'http://www.shfe.com.cn/data/dailydata/%sdailystock.dat'
CZCE_RECIEPT_URL_1 = 'http://www.czce.com.cn/cn/exchange/jyxx/sheet/sheet%s.html'
CZCE_RECIEPT_URL_2 = 'http://www.czce.com.cn/cn/exchange/%s/datawhsheet/%s.htm'
CZCE_RECIEPT_URL_3 = 'http://www.czce.com.cn/cn/DFSStaticFiles/Future/%s/%s/FutureDataWhsheet.htm'

CFFEX_DAILY_URL = 'http://www.cffex.com.cn/fzjy/mrhq/%s/%s/%s_1.csv'
SHFE_DAILY_URL = 'http://www.shfe.com.cn/data/dailydata/kx/kx%s.dat'
SHFE_VWAP_URL = 'http://www.shfe.com.cn/data/dailydata/ck/%sdailyTimePrice.dat'
DCE_DAILY_URL = 'http://www.dce.com.cn//publicweb/quotesdata/dayQuotesCh.html'
CZCE_DAILY_URL_1 = 'http://www.czce.com.cn/cn/exchange/jyxx/hq/hq%s.html'
CZCE_DAILY_URL_2 = 'http://www.czce.com.cn/cn/exchange/%s/datadaily/%s.txt'
CZCE_DAILY_URL_3 = 'http://www.czce.com.cn/cn/DFSStaticFiles/Future/%s/%s/FutureDataDaily.txt'


DATE_PATTERN = re.compile(r'^([0-9]{4})[-/]?([0-9]{2})[-/]?([0-9]{2})')
FUTURE_SYMBOL_PATTERN = re.compile(r'(^[A-Za-z]{1,2})[0-9]+')


CFFEX_COLUMNS = ['open','high','low','volume','turnover','open_interest','close','settle','change1','change2']
CZCE_COLUMNS = ['pre_settle','open','high','low','close','settle','change1','change2','volume','open_interest','oi_chg','turnover','final_settle']
CZCE_COLUMNS_2 = ['pre_settle','open','high','low','close','settle','change1','volume','open_interest','oi_chg','turnover','final_settle']
SHFE_COLUMNS =  {'CLOSEPRICE': 'close',  'HIGHESTPRICE': 'high', 'LOWESTPRICE': 'low', 'OPENINTEREST': 'open_interest', 'OPENPRICE': 'open',  'PRESETTLEMENTPRICE': 'pre_settle', 'SETTLEMENTPRICE': 'settle',  'VOLUME': 'volume'}
SHFE_VWAP_COLUMNS = {':B1': 'date', 'INSTRUMENTID': 'symbol', 'TIME': 'time_range', 'REFSETTLEMENTPRICE': 'vwap'}
DCE_COLUMNS = ['open', 'high', 'low', 'close', 'pre_settle', 'settle', 'change1','change2','volume','open_interest','oi_chg','turnover']
DCE_OPTION_COLUMNS = ['open', 'high', 'low', 'close', 'pre_settle', 'settle', 'change1', 'change2', 'delta', 'volume', 'open_interest', 'oi_chg', 'turnover', 'exercise_volume']

OUTPUT_COLUMNS = ['symbol', 'date', 'open', 'high', 'low', 'close', 'volume', 'open_interest', 'turnover', 'settle', 'pre_settle', 'variety']
OPTION_OUTPUT_COLUMNS = ['symbol', 'date', 'open', 'high', 'low', 'close', 'pre_settle', 'settle', 'delta', 'volume', 'open_interest', 'oi_chg', 'turnover', 'implied_volatility', 'exercise_volume', 'variety']

DCE_MAP =  {
    '豆一': 'A',
    '豆二': 'B',
    '豆粕': 'M',
    '豆油': 'Y',
    '棕榈油': 'P',
    '玉米': 'C',
    '玉米淀粉': 'CS',
    '鸡蛋': 'JD',
    '纤维板': 'FB',
    '胶合板': 'BB',
    '聚乙烯': 'L',
    '聚氯乙烯': 'V',
    '聚丙烯': 'PP',
    '焦炭': 'J',
    '焦煤': 'JM',
    '铁矿石': 'I',
    '乙二醇':'EG'
}


def convert_date(date):
    """
    transform a date string to datetime.date object.
    :param date, string, e.g. 2016-01-01, 20160101 or 2016/01/01
    :return: object of datetime.date(such as 2016-01-01) or None
    """
    if isinstance(date, datetime.date):
        return date
    elif isinstance(date, str):
        match = DATE_PATTERN.match(date)
        if match:
            groups = match.groups()
            if len(groups) == 3:
                return datetime.date(year=int(groups[0]), month=int(groups[1]), day=int(groups[2]))
    return None


def getJsonPath(name, moduleFile):
    """
    获取JSON配置文件的路径从模块所在目录查找： 
    """
    moduleFolder = os.path.abspath(os.path.dirname(moduleFile))
    moduleJsonPath = os.path.join(moduleFolder, '.', name)
    return moduleJsonPath

def get_calendar():
    """
    获取交易日历至2018年结束
    :return :  list
    """
    settingFileName = 'calendar.json'
    settingfilePath = getJsonPath(settingFileName, __file__)
    return json.load(open(settingfilePath,"r"))

def lastTradingDay(d):

    """
    获取前一个交易日
    :param d:           '%Y%m%d' or  datetime.date()
    :return lastday:    '%Y%m%d' or  datetime.date()
    """
    calendar = get_calendar()

    if isinstance(d,(str)):
        if d not in calendar:
            print('Today is not tradingday：' + d)
            return False
        Pos = calendar.index(d)
        lastday = calendar[Pos - 1]
        return lastday

    elif isinstance(d,(datetime.date)):
        d_str = d.strftime('%Y%m%d')
        if d_str not in calendar:
            print('Today is not workingday：' + d_str)
            return False
        Pos = calendar.index(d_str)
        lastday = calendar[Pos - 1]
        lastday = datetime.datetime.strptime(lastday,'%Y%m%d').date()
        return lastday

def get_latestDataDate(d):
    """
    获取最新的有数据的日期
    :param d:           datetime.datetime()
    :return string
    """

    calendar = get_calendar()
    if d.strftime('%Y%m%d') in calendar:
        if d.time() > datetime.time(17, 0, 0):
            return d.strftime('%Y%m%d')
        else:
            return lastTradingDay(d.strftime('%Y%m%d'))
    else:
        while d.strftime('%Y%m%d') not in calendar:
            d = d - datetime.timedelta(days = 1)
        return d.strftime('%Y%m%d')



if __name__ == '__main__':
    d = datetime.datetime(2018,10,5,17,1,0)
    print(get_latestDataDate(d))