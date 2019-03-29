# -*- coding:utf-8 -*-

import fushare
import json
import datetime
from time import sleep
import warnings
calendar = fushare.cons.get_calendar()

settingFileName = 'setting.json'
settingfilePath = fushare.cons.getJsonPath(settingFileName, __file__)
s = json.load(open(settingfilePath,"r"))

def downLoad(date):
    date = fushare.cons.convert_date(date) if date is not None else datetime.date.today()
    if date not in calendar:
        warnings.warn('%s非交易日' % date.strftime('%Y%m%d'))
        return
    #----------------------------------------------------------------------
    print('\n' +'-'*80+'\n展期')
    df = fushare.get_rollYield_bar(type = 'var', date = date)
    df.to_csv(s['root']+'展期%s.csv'%date)

    #----------------------------------------------------------------------
    print('\n' +'-'*80+'\n基差')
    df = fushare.get_spotPrice(date)
    df.to_csv(s['root']+'基差%s.csv'%date)

    #----------------------------------------------------------------------
    print('\n' +'-'*80+'\n会员持仓排名之和')
    df = fushare.get_rank_sum_daily(start = date, end = date)
    df.to_csv(s['root']+'会员持仓排名%s.csv'%date)

    #----------------------------------------------------------------------
    print('\n' +'-'*80+'\n仓单')
    df = fushare.get_reciept(date)
    df.to_csv(s['root']+'仓单%s.csv'%date)

    #----------------------------------------------------------------------
    if s['qqEmail'] != '*':
        fushare.sendEmail('fushare',s['qqEmail'],s['secret'],s['qqEmail'],'smtp.qq.com', '465',['展期%s.csv'%date,'基差%s.csv'%date,'会员持仓排名%s.csv'%date,'仓单%s.csv'%date],s['root'],True)

def monitor(catchTime = '17:00'):
    while True:
        now = datetime.datetime.now()
        if now.strftime('%H:%M') == catchTime:
            downLoad(now.strftime('%Y%m%d'))
        sleep(40)


if __name__ == '__main__':
    monitor()