# all built-in libraries at the top
import os
import datetime

# all third-party libraries in the middle
import backtrader as bt
import pandas as pd
import matplotlib.pyplot as plt


datadir = './data' # data path
logdir = './log' # log path
reportdir = './report' # report path
datafile = 'BTC_USDT_1h.csv' # data file
logfile = 'BTC_USDT_1h_SMACross_10_20_2020-01-01_2020-04-01.csv'
figfile = 'BTC_USDT_1h_SMACross_10_20_2020-01-01_2020-04-01.png'
from_datetime = '2020-01-01 00:00:00' # start time
to_datetime = '2020-04-01 00:00:00' # end time


class SMACross(bt.Strategy):
    params = (
        ('pfast', 10),
        ('pslow', 20),
    )

    def __init__(self):

        pfast = bt.indicators.SMA(self.datas[0], period=self.p.pfast)
        pslow = bt.indicators.SMA(self.datas[0], period=self.p.pslow)
        self.crossover = bt.indicators.CrossOver(pfast, pslow)

    def next(self):

        if not self.position:
            if self.crossover > 0:
                self.order = self.buy()

        elif self.crossover < 0:
            self.order = self.sell()

# initiate cerebro instance
cerebro = bt.Cerebro()

# feed data
data = pd.read_csv(
    os.path.join(datadir, datafile), index_col='datetime', parse_dates=True)
data = data.loc[
    (data.index >= pd.to_datetime(from_datetime)) &
    (data.index <= pd.to_datetime(to_datetime))]
datafeed = bt.feeds.PandasData(dataname=data)
cerebro.adddata(datafeed)

# feed strategy
cerebro.addstrategy(SMACross)

# additional backtest setting
cerebro.addsizer(bt.sizers.PercentSizer, percents=99)
cerebro.broker.set_cash(10000)
cerebro.broker.setcommission(commission=0.001)

# add logger
cerebro.addwriter(
    bt.WriterFile,
    out=os.path.join(logdir, logfile),
    csv=True)

# run
cerebro.run()

# save report
plt.rcParams['figure.figsize'] = [13.8, 10]
fig = cerebro.plot(style='candlestick', barup='green', bardown='red')
fig[0][0].savefig(
	os.path.join(reportdir, figfile),
	dpi=480)