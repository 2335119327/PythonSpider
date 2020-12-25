import requests
import json
import csv
import pandas as pd
from pyecharts import options as opts
from pyecharts.charts import Bar

headers = {
    "User-Agent": "Mozilla/5.0 (Macintosh; Intel Mac OS X 10_13_6) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/85.0.4183.121 Safari/537.36"
}


# mode="a" 表示追加写入
file = open('data.csv', mode="a", encoding='utf-8', newline="")
# fieldnames表头数据
csvWrite = csv.DictWriter(file, fieldnames=['股票代码', '股票名称', '当前价', '涨跌额', '涨跌幅', '年初至今', '成交量', '成交额', '换手率',
                                            '市盈(TTM)', '股息率', '市值'])

# 写入表头数据
csvWrite.writeheader()

for i in range(1,10):
    print("=========正在爬取第"+str(i)+"页数据==========")
    url = "https://xueqiu.com/service/v5/stock/screener/quote/list?page="+str(i)+"&size=30&order=desc&order_by=amount&exchange=CN&market=CN&type=sha&_=1601168743543"
    response = requests.get(url=url,headers=headers).json()

    for data in response['data']['list']:
        #股票代码
        symbol = data['symbol']
        #股票名称
        name = data['name']
        #当前价
        current = data['current']
        #涨跌额
        chg = data['chg']
        if chg:
            if float(chg) > 0:
                chg = "+" + str(chg)
            else:
                chg = str(chg)
        #涨跌幅
        percent = str(data['percent']) + "%"
        #年初至今
        current_year_percent = str(data['current_year_percent']) + "%"
        #成交量
        volume = data["volume"]
        #成交额
        amount = data['amount']
        #换手率
        turnover_rate = str(data['turnover_rate']) + "%"
        #市盈(TTM)
        pe_ttm = data['pe_ttm']
        #股息率
        dividend_yield = data['dividend_yield']
        if dividend_yield:
            dividend_yield = str(dividend_yield) + "%"
        else:
            dividend_yield = None
        #市值
        market_capital = data['market_capital']
        data_dict = {'股票代码':symbol,'股票名称':name,'当前价':current,
                     '涨跌额':chg,'涨跌幅':percent,'年初至今':current_year_percent,
                     '成交量':volume,'成交额':amount,'换手率':turnover_rate,
                     '市盈(TTM)':pe_ttm,'股息率':dividend_yield,
                     '市值':market_capital}

        csvWrite.writerow(data_dict)


data_df = pd.read_csv("data.csv")
df = data_df.dropna()
df1 = df[['股票名称','成交量']]
#取前30条数据
df2 = df1.iloc[:30]


c = (
    Bar(init_opts=opts.InitOpts(width="1500px",height="660px",page_title="股票数据可视化")).add_xaxis(list(df2['股票名称'].values))
    .add_yaxis('股票成交量情况',list(df2['成交量'].values))
    .set_global_opts(
        title_opts=opts.TitleOpts(title="成交量图表"),
        datazoom_opts=opts.DataZoomOpts()
    )
    .render("data.html")
)