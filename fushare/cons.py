import re
import datetime

market_var = {'cffex': ['IF','IC','IH','T','TF'],
'dce':['C','CS','A','B','M','Y','P','FB','BB','JD','L','V','PP','J','JM','I'],
'czce':['WH','PM','CF','SR','TA','OI','RI','MA','ME','FG','RS','RM','ZC','JR','LR','SF','SM','WT','TC','GN','RO','ER','SRX','SRY','WSX','WSY','CY','AP'],
'shfe':['CU','AL','ZN','PB','NI','SN','AU','AG','RB','WR','HC','FU','BU','RU']
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

SYS_SPOTPRICE_URL = 'http://www.100ppi.com/sf/day-%s.html'
SYS_SPOTPRICE_LATEST_URL = 'http://www.100ppi.com/sf/'

SHFE_VOLRANK_URL = 'http://www.shfe.com.cn/data/dailydata/kx/pm%s.dat'
CFFEX_VOLRANK_URL = 'http://www.cffex.com.cn/fzjy/ccpm/%s/%s/%s_1.csv'
DCE_VOLRANK_URL = 'http://www.dce.com.cn/publicweb/quotesdata/exportMemberDealPosiQuotesData.html?memberDealPosiQuotes.variety=%s&memberDealPosiQuotes.trade_type=0&contract.contract_id=all&contract.variety_id=%s&year=%s&month=%s&day=%s&exportFlag=txt'
CZCE_VOLRANK_URL_1 = 'http://www.czce.com.cn/portal/exchange/jyxx/pm/pm%s.html'
CZCE_VOLRANK_URL_2 = 'http://www.czce.com.cn/portal/exchange/%s/datatradeholding/%s.htm'
CZCE_VOLRANK_URL_3 = 'http://www.czce.com.cn/portal/DFSStaticFiles/Future/%s/%s/FutureDataHolding.htm'

DCE_RECIEPT_URL = 'http://www.dce.com.cn/publicweb/quotesdata/wbillWeeklyQuotes.html?wbillWeeklyQuotes.variety=all&year=%s&month=%s&day=%s'
SHFE_RECIEPT_URL_1 = 'http://www.shfe.com.cn/data/dailydata/%sdailystock.html'
SHFE_RECIEPT_URL_2 = 'http://www.shfe.com.cn/data/dailydata/%sdailystock.dat'
CZCE_RECIEPT_URL_1 = 'http://www.czce.com.cn/portal/exchange/jyxx/sheet/sheet%s.html'
CZCE_RECIEPT_URL_2 = 'http://www.czce.com.cn/portal/exchange/%s/datawhsheet/%s.htm'
CZCE_RECIEPT_URL_3 = 'http://www.czce.com.cn/portal/DFSStaticFiles/Future/%s/%s/FutureDataWhsheet.htm'

DATE_PATTERN = re.compile(r'^([0-9]{4})[-/]?([0-9]{2})[-/]?([0-9]{2})')

def convert_date(date):
    """
    transform a date string to datetime.date object.
    :param day, string, e.g. 2016-01-01, 20160101 or 2016/01/01
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

