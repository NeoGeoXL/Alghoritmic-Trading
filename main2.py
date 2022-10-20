from ib_insync import *
import pandas as pd
# util.startLoop()  # uncomment this line when in a notebook

ib = IB()
ib.connect('127.0.0.1', 7497, clientId=1)

contract = Stock('NVDA', 'SMART', 'USD')
'''bars = ib.reqHistoricalData(
    contract, endDateTime='', durationStr='30 D',
    barSizeSetting='1 hour', whatToShow='MIDPOINT', useRTH=True)'''


ib.qualifyContracts(contract)

order = MarketOrder('BUY', 1)
trade = ib.placeOrder(contract, order)
#ib.cancelOrder(order)
ib.sleep(1)

contract1 = Stock('AMD', 'SMART', 'USD')
ib.qualifyContracts(contract1)

order1 = MarketOrder('BUY', 1)
trade1 = ib.placeOrder(contract1, order1)

#ib.cancelOrder(order1)

df = util.df(ib.trades())
#print(df)
df_positions = util.df(ib.positions())
print(df_positions)
df_positions.to_csv('positions.csv')

df_orders = util.df(ib.orders())
print(df_orders)
df_orders.to_csv('orders.csv')

df_open_orders = util.df(ib.openOrders())
print(df_open_orders)
df_open_orders.to_csv('open_orders.csv')

#df.to_csv('AMD.csv')

ib.disconnect()
#print(trade1.log)