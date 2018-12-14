# -*- coding:utf-8 -*-

import re
from fushare import cons

def symbol2varietie(symbol):
    var = ''.join(re.findall('\D',symbol)).upper().strip()
    if var == 'PTA':
        var = 'TA'
    return var

def symbolMarket(symbol):
    var = symbol2varietie(symbol)
    for (market,vars) in cons.market_var.items():
        if var in vars:
            return market

def find_chinese(string):
    p = re.compile(u'[\u4e00-\u9fa5]')
    res = re.findall(p, string)
    return ''.join(res)

def chinese_to_english(var):
    """
    翻译期货品种中文和英文缩写
    """

    chineseList=['橡胶','天然橡胶','石油沥青','沥青','沥青仓库','沥青(仓库)','沥青厂库','沥青(厂库)','热轧卷板','热轧板卷','燃料油',
                 '白银','线材','螺纹钢','铅','铜','铝','锌','黄金','钯金','锡','镍','纸浆',
                 '豆一','大豆','豆二','胶合板','玉米','玉米淀粉','聚乙烯','LLDPE','LDPE','豆粕','豆油','大豆油',
                 '棕榈油','纤维板','鸡蛋','聚氯乙烯','PVC','聚丙烯','PP','焦炭','焦煤','铁矿石','乙二醇',
                 '强麦','强筋小麦',' 强筋小麦','硬冬白麦','普麦','硬白小麦','硬白小麦（）','皮棉','棉花','一号棉','白糖','PTA','菜籽油','菜油','早籼稻','早籼','甲醇','柴油','玻璃',
                 '油菜籽','菜籽','菜籽粕','菜粕','动力煤','粳稻','晚籼稻','晚籼','硅铁','锰硅','硬麦','棉纱','苹果',
                 '原油','中质含硫原油']
    englishList=['RU','RU','BU','BU','BU','BU','BU2','BU2','HC','HC','FU','AG','WR','RB','PB','CU','AL','ZN','AU','AU','SN','NI','SP',
                 'A','A','B','BB','C','CS','L','L','L','M','Y','Y',
                 'P','FB','JD','V','V','PP','PP','J','JM','I','EG',
                 'WH','WH','WH','PM','PM','PM','PM','CF','CF','CF','SR','TA','OI','OI','RI','ER','MA','MA','FG',
                 'RS','RS','RM','RM','ZC','JR','LR','LR','SF','SM','WT','CY','AP',
                 'SC','SC']
    pos=chineseList.index(var)
    return(englishList[pos])


if __name__ == '__main__':
    print(chinese_to_english('苹果'))
    symbol = 'rb1801'
    var = symbol2varietie('rb1808')
    print(var)
    market = symbolMarket('SP')
    print(market)
    chi = find_chinese('a对方水电费dc大V')
    print(chi)