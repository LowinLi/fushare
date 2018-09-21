# fushare(python3)
https://github.com/LowinLi/fushare

Installation
--------------
    pip install fushare

Upgrade
---------------
    pip install fushare --upgrade
    
Latest Version
---------------
    1.1.9


**作者：金属成色**

**目录**
- [fushare库的初衷](#fushare库的初衷)
- [展期收益率](#展期收益率)
- [注册仓单](#注册仓单)
- [现货价格和基差](#现货价格和基差)
- [会员持仓排名](#会员持仓排名)



## fushare库的初衷

传统的CTA策略以趋势为主，但是自从2017年以来，无论是长线还是短线的趋势策略都受制于商品波动率的降低，面临了多多少少的回撤，同时市场也逐渐趋于机构化理性化，因此在传统CTA策略的基础上加入基本面的因素显得迫在眉睫。近几年各券商的研报陆续提出了许多依赖于趋势行情以外的有效信号，它们的表现都与趋势策略有着很低的甚至负的相关性，这样通过多种不同类型的信号对冲得到的策略，就有机会在市场上取得非常棒的夏普率和稳定的收益。

fushare库的公开就是为了向各位同仁提供一个爬虫接口，避免各个研究组、机构重复造轮子爬取相关数据的资源浪费。


## 展期收益率
展期收益率是由不同交割月的价差除以相隔月份数计算得来，它反映了市场对该品种在近期交割和远期交割的价差预判。

通过fushare.get_rollYield_bar接口下载展期收益率，这里展期收益率列表的序列类型分为三种，分别可以通过type='date'、'symbol'、'var'获取。
其中'date'类型是由某商品品种在不同日期的主力合约次主力合约的价差组成，调用方法例子为：

fushare.get_rollYield_bar(type = 'date', var = 'RB', start = '20180618', end = '20180718',plot = True)，如下图所示。

![展期收益率1](http://m.qpic.cn/psb?/V12c0Jww0zKwzz/5*I5BdC65qlzua*UdvH8RLnUqlxUPZac.zFZudbuu70!/b/dEcBAAAAAAAA&bo=6gIZAQAAAAADB9I!&rf=viewer_4)


其中'symbol'类型是由某商品品种在某天的所有交割月合约价格组成，可以很方便的观察该品种从近期到远期的展期结构，调用方法例子为：

fushare.get_rollYield_bar(type = 'symbol', var = 'RB', date = '20180718',plot = True)，如下图所示。

![展期收益率2](http://m.qpic.cn/psb?/V12c0Jww0zKwzz/C4uCfCH4GmrJZIuM5bh4UxXIZVybLVQ1fg5PjxNRC4U!/b/dDEBAAAAAAAA&bo=3AIqAQAAAAADB9c!&rf=viewer_4)


其中'var'类型是由某交易日，所有品种的主力次主力合约展期收益率的组合，可以方便的找到展期收益率高的品种和低的品种，调用方法例子为：

fushare.get_rollYield_bar(type = 'var', date = '20180718',plot = True)，如下图所示。

![展期收益率3](http://m.qpic.cn/psb?/V12c0Jww0zKwzz/A7sWrX8pHdkmNybpwx.qziH0pjFvl9ZDh7e1W8olQo8!/b/dDIBAAAAAAAA&bo=zAIxAQAAAAADB9w!&rf=viewer_4)


利用fushare.get_rollYield接口，可以找到特定合约特定日期的主力合约次主力合约展期收益率，或通过symbol1、symbol2变量自定义某两个合约的展期收益率。


fushare.get_rollYield(date = '20180718', var = 'IF', symbol1 = 'IF1812', symbol2 = 'IF1811')，如下图所示：

![展期收益率4](http://m.qpic.cn/psb?/V12c0Jww0zKwzz/sbBvkU.BCNWrQfDLkBL918x2*0j1QTbzXhjIP4rg5Ec!/b/dC0BAAAAAAAA&bo=VgRKAAAAAAADBzo!&rf=viewer_4)


注意：

1.以上展期计算所用的日线行情数据来自tushare库的爬取；

2.主力合约和次主力合约的定义，是由该日的各交割月合约持仓量由大到小排序得到。


## 注册仓单
注册仓单是由各交易所的公布的日级数据，在一定程度上可以反映市场的库存变化。调用例子如下：

fushare.get_reciept(start = '20180712', end = '20180719', vars = ['CU', 'NI'])

![注册仓单](http://m.qpic.cn/psb?/V12c0Jww0zKwzz/cOYxMVta6Ylp87IskIjwOG6nkkMJQ1HJ7HggCSgafog!/b/dDABAAAAAAAA&bo=WARNAgAAAAADBzE!&rf=viewer_4)

注意：

1.vars变量接上需要爬取的品种列表，即使是一个品种，也需要以列表形式输入；

2.在研究仓单的方向变化时，需要考虑一些品种的年度周期性，如农产品的收割季、工业品的开工季等；

3.需考虑到交割日的仓单变化。


## 现货价格和基差
基差是商品期货非常重要的基本面因素。这里提供两种获取基差的方法：
获取当天的基差数据

fushare.get_spotPrice()

返回值分别为品种、现货价格、最近交割合约、最近交割合约价格、主力合约、主力合约价格、最近合约基差值、主力合约基差值、最近合约基差率、主力合约基差率。


![现货价格和基差1](http://m.qpic.cn/psb?/V12c0Jww0zKwzz/1yzlLTNuEb9MlS7Hf5aCd4SnzyyuJ7yMsrN8SVM3o.o!/b/dEUBAAAAAAAA&bo=9QIeAgAAAAADJ.k!&rf=viewer_4)


获取历史某段时间的基差值

fushare.get_spotPrice_daily(start = '20180710', end = '20180719', vars = ['CU', 'RB'])

![现货价格和基差2](http://m.qpic.cn/psb?/V12c0Jww0zKwzz/4MI.i0EOyN7EfQP2saeb0NAOmrIldZbSrEMCaf4b2.0!/b/dDABAAAAAAAA&bo=nwLbAQAAAAADB2U!&rf=viewer_4)


注意：

现货价格是从生意社网站爬取获得，仅支持从2011年至今每个交易日数据。


## 会员持仓排名
自从“蜘蛛网策略”问世以来，会员持仓数据受到日益关注。数据的爬取方式如下所示：
获取某段时间的会员持仓排名前5、前10等总和

fushare.get_rank_sum_daily(start = '20180718', end = '20180719', vars = ['IF', 'C'])
![会员持仓1](http://m.qpic.cn/psb?/V12c0Jww0zKwzz/10ILkxJYpz7G7WGpnWI1yLlk0jGDzgjoNOsttgwcWd0!/b/dFUAAAAAAAAA&bo=dQPAAQAAAAADB5U!&rf=viewer_4)

获取某交易日的会员持仓排名前5、前10等总和

fushare.get_rank_sum(date = '20180719', vars = ['CF'])
![会员持仓2](http://m.qpic.cn/psb?/V12c0Jww0zKwzz/bqwB8l7lgM9bIVEak7zYL7NjO8oOmFIvAMI9x*lBIGY!/b/dEYBAAAAAAAA&bo=vwMYAQAAAAADB4c!&rf=viewer_4)

获取某交易日某品种的持仓排名榜

fushare.get_dce_rank_table()、fushare.get_cffex_rank_table()、fushare.get_czce_rank_table()、fushare.get_shfe_rank_table()。
![会员持仓3](http://m.qpic.cn/psb?/V12c0Jww0zKwzz/O905N6vk7SFlQlnPfaFJEZi2qTFUOl.7OKXIGmBeWm8!/b/dFoAAAAAAAAA&bo=pgM8AQAAAAADB7o!&rf=viewer_4)

注意：

因为个交易所公布的持仓排名不同：大连所只公布品种的总持仓排名，没有按不同交割月划分；上海、中金交易所公布了每个交割月的持仓排名，没有公布品种所有合约总排名，因此这里的品种排名和是各合约加总计算得来；郑州交易所公布了各合约排名和品种排名，因此这里都是交易所原始数据。

致谢：
感谢tushare项目提供借鉴学习的机会；感谢生意社网站的商品基差数据的公开。

交流：
欢迎加QQ群交流809290570

数据仅供参考，不构成投资建议，投资者请自行研究，风险自担。

