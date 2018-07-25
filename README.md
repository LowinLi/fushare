# fushare
https://github.com/LowinLi/fushare

Installation
--------------
    pip install fushare

Upgrade
---------------
    pip install fushare --upgrade

**作者：金属成色**

**目录**
- [fushare库的初衷](#fushare库的初衷)
- [展期收益率](#展期收益率)
- [注册仓单](#注册仓单)
- [现货价格和基差](#现货价格和基差)
- [会员持仓排名](#会员持仓排名)

## fushare库的初衷
传统的CTA策略以趋势为主，但是自从2017年以来，无论是长线还是短线的趋势策略受制于商品波动率的降低，都面临了多多少少的回撤，市场也逐渐趋于机构化理性化。在传统CTA策略的基础上加入基本面的因素显得迫在眉睫。近几年各券商的研报陆续提出了许多依赖于趋势行情以外的有效信号，它们都表现出了与趋势策略有着很低的甚至负的相关性，这样多种不同类型的信号对冲就可以在市场上取得非常棒的夏普率和稳定的收益。
fushare库的公开就是为了向各位同仁提供一个爬虫接口，避免各个研究组、机构重复造轮子爬取相关数据的资源浪费。爬取的数据有以下几类。

## 展期收益率

通过fushare.get_rollYield_bar接口下载展期收益率，这里展期收益率列表的序列类型分为三种，分别可以通过type='date'、'symbol'、'var'获取。
其中'date'类型是由某商品品种在不同日期的主力合约次主力合约的价差组成，调用方法例子为：fushare.get_rollYield_bar(type = 'date', var = 'RB', start = '20180618', end = '20180718',plot = True)，如下图所示。

![展期收益率1](http://m.qpic.cn/psb?/V12c0Jww0zKwzz/5*I5BdC65qlzua*UdvH8RLnUqlxUPZac.zFZudbuu70!/b/dEcBAAAAAAAA&bo=6gIZAQAAAAADB9I!&rf=viewer_4)

其中'symbol'类型是由某商品品种在某天的所有交割月合约价格组成，可以很方便的观察该品种从近期到远期的展期结构，调用方法例子为：fushare.get_rollYield_bar(type = 'symbol', var = 'RB', date = '20180718',plot = True)，如下图所示。

![展期收益率2](http://m.qpic.cn/psb?/V12c0Jww0zKwzz/C4uCfCH4GmrJZIuM5bh4UxXIZVybLVQ1fg5PjxNRC4U!/b/dDEBAAAAAAAA&bo=3AIqAQAAAAADB9c!&rf=viewer_4)

其中'var'类型是由某交易日，所有品种的主力次主力合约展期收益率的组合，可以方便的找到展期收益率高的品种和低的品种，调用方法例子为：fushare.get_rollYield_bar(type = 'var', date = '20180718',plot = True)，如下图所示。

![展期收益率3](http://m.qpic.cn/psb?/V12c0Jww0zKwzz/A7sWrX8pHdkmNybpwx.qziH0pjFvl9ZDh7e1W8olQo8!/b/dDIBAAAAAAAA&bo=zAIxAQAAAAADB9w!&rf=viewer_4)

利用fushare.get_rollYield接口，可以找到特定合约特定日期的主力合约次主力合约展期收益率，或通过symbol1、symbol2变量自定义某两个合约的展期收益率。
fushare.get_rollYield(date = '20180718', var = 'IF', symbol1 = 'IF1812', symbol2 = 'IF1811')，如下图所示：
![展期收益率4](http://m.qpic.cn/psb?/V12c0Jww0zKwzz/sbBvkU.BCNWrQfDLkBL918x2*0j1QTbzXhjIP4rg5Ec!/b/dC0BAAAAAAAA&bo=VgRKAAAAAAADBzo!&rf=viewer_4)

注意：
1.以上展期计算所用的日线行情数据来自tushare库的爬取；
2.主力合约和次主力合约的定义，是由该日的各交割月合约持仓量由大到小排序得到；

## 注册仓单
注册仓单是由各交易所的公布的日级数据，在一定程度上可以反映市场的库存变化。调用例子如下：
fushare.get_reciept(start = '20180712', end = '20180719', vars = ['CU', 'NI']
![注册仓单](http://m.qpic.cn/psb?/V12c0Jww0zKwzz/cOYxMVta6Ylp87IskIjwOG6nkkMJQ1HJ7HggCSgafog!/b/dDABAAAAAAAA&bo=WARNAgAAAAADBzE!&rf=viewer_4)

注意：
1.在研究仓单的方向变化时，也需要考虑一些品种的年度周期性，如农产品的收割季、工业品的开工季等
2.需考虑到交割日的仓单变化
## 现货价格和基差


## 会员持仓排名
