from etherscan.accounts import Account
import json
import pandas as pd
with open('api_key.json', mode='r') as key_file:
    key = json.loads(key_file.read())['key']

address = '0x2a65aca4d5fc5b5c859090a6c34d164135398226'

api = Account(address=address, api_key=key)
blocks = api.get_blocks_mined_page(page=1, offset=10000, blocktype='blocks')

blockNumber = []
timeStamp = []
blockReward = []
for i in range(len(blocks)):
    blockNumber.append(blocks[i]['blockNumber'])
    timeStamp.append(blocks[i]['timeStamp'])
    blockReward.append(blocks[i]['blockReward'])

df = pd.DataFrame()
df['blockNumber'] = blockNumber
df['timeStamp'] = timeStamp
df['blockReward'] = blockReward
df['timeStamp'] = pd.to_datetime(df['timeStamp'],unit='s')
df.to_csv('get_blocks_mined_page.csv')