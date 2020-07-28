import os
import pandas as pd
from binance.client import Client


dir = './data'
pd.set_option('display.max_columns',None)
if not os.path.isdir(dir):
    os.mkdir(dir)

client = Client("","")

# get historical klines data
raw_klines = client.get_historical_klines("BTCUSDT","1h","2019-1-1")
df = pd.DataFrame(raw_klines,
                  columns=['Open_Time', 'Open', 'High', 'Low', 'Close', 'Volume', 'Close_Time',
                           'Quote_Asset_Volume',
                           'Num_Trades', 'Tb_Base_Asset_Volume', 'Tb_Quote_Asset_Volume', 'Ignored'])
df['Open_Time'] = pd.to_datetime(df['Open_Time'], unit='ms')
df['Close_Time'] = pd.to_datetime(df['Close_Time'], unit='ms')
df.to_csv(dir + '/historical_klines.csv')

# get order book
raw = client.get_order_book(symbol = "BTCUSDT",limit = 500)
df = pd.DataFrame(raw['bids'], columns=['bids_price', 'bids_qty'])
df1 = pd.DataFrame(raw['asks'], columns=['asks_price', 'asks_qty'])
mergeddf = df.merge(df1, left_index=True, right_index=True)
mergeddf.to_csv(dir + '/orderbook.csv')

# get recent trades
raw_trades = client.get_recent_trades(symbol = "BTCUSDT")
df1 = pd.DataFrame(raw_trades, columns=['id', 'price', 'qty', 'quoteQty', 'time', 'isBuyerMaker', 'isBestMatch'])
df1['time'] = pd.to_datetime(df1['time'], unit='ms')
df1.to_csv(dir + '/recent_trades.csv')