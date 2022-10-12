import time
import stocks as stocks 
from datetime import datetime
import pandas as pd
import strategy as strategy
import TradingBot 
from ibapi.client import EClient
from ibapi.wrapper import EWrapper
from ibapi.contract import Contract
from ibapi.order import Order
import threading
import time


class IBapi(EWrapper, EClient):
	def __init__(self):
		EClient.__init__(self, self)

	def nextValidId(self, orderId: int):
		super().nextValidId(orderId)
		self.nextorderId = orderId
		print('The next valid order id is: ', self.nextorderId)

	def orderStatus(self, orderId, status, filled, remaining, avgFullPrice, permId, parentId, lastFillPrice, clientId, whyHeld, mktCapPrice):
		print('orderStatus - orderid:', orderId, 'status:', status, 'filled', filled, 'remaining', remaining, 'lastFillPrice', lastFillPrice)
	
	def openOrder(self, orderId, contract, order, orderState):
		print('openOrder id:', orderId, contract.symbol, contract.secType, '@', contract.exchange, ':', order.action, order.orderType, order.totalQuantity, orderState.status)

	def execDetails(self, reqId, contract, execution):
		print('Order Executed: ', reqId, contract.symbol, contract.secType, contract.currency, execution.execId, execution.orderId, execution.shares, execution.lastLiquidity)

app = IBapi()
app.connect('127.0.0.1', 7497, 0)
app.nextorderId = None

def run_loop():
	app.run()
    
api_thread = threading.Thread(target=run_loop, daemon=True)
api_thread.start()

while True:
	if isinstance(app.nextorderId, int):
		print('connected')
		break
	else:
		print('waiting for connection')
		time.sleep(1)

def defineContract(symbol,secType,exchange,currency='USD'):
    contract = Contract()
    contract.symbol = symbol
    contract.secType = secType
    contract.exchange = exchange
    contract.currency = currency
    return contract

# Definimos el par GBP/USD
def createOrder(action,totalQuantity,orderType):
    order = Order()
    order.eTradeOnly = False
    order.firmQuoteOnly = False
    order.action = action
    order.totalQuantity = totalQuantity
    order.orderType = orderType
    return order

stock='NVDA'
#Ratio Riesgo:Beneficio 1:2
riesgo=0.01
beneficio=0.02


list_of_stocks=['PCG','F','VALE','PBR','MSFT','NVDA','NTDOY','TSLA','KHC','AMZN','GOOG','TWTR','NIO','NKE','PFE','PEP','PG','PYPL','INTC','AMD','CSCO','V','VZ','WMT','XOM','JNJ','JPM','HD','MCD','KO','VVV','SONY']

#Anticrisis Stocks
#list_of_stocks=['WMT','PG','MCD','HD','PFE','JNJ','KHC','CVX','PBR','COKE']

while 1:
    for stock in list_of_stocks:
        #Lo primero que tengo que hacer es ver si las condiciones del precio me dicen que compre o no.
        df = stocks.get_stocks_data(stock)
        #print(df)
        condiciones=strategy.df_condiciones_entrada(df)
        #print(condiciones)
        senal_entrada=strategy.senal_entrada(condiciones) #Me ubico en la fila que voy a analizar las condiciones
        print('-'*20+' '+stock+' '+'-'*20)
        print(senal_entrada)
        condicion1_long,condicion2_long,condicion3_long=strategy.condiciones_operar_long(senal_entrada)
        condicion1_short,condicion2_short,condicion3_short=strategy.condiciones_operar_short(senal_entrada)

        if condicion1_long==True & condicion2_long == True & condicion3_long == True:
            #Mensaje
            #stock='PBR'
            precio_entrada=round(senal_entrada['Close'].iat[0],2)
            operacion = 'Buy Long'
            stop_loss_price = round(stocks.stop_loss_long(precio_entrada,riesgo),2)
            take_profit_price = round(stocks.take_profit_long(precio_entrada,beneficio),2)
            action ='BUY'
            quantity = 1
            limitPrice = precio_entrada
            takeProfitPrice = take_profit_price
            stopLossPrice = stop_loss_price
            symbol = stock
            secType = 'STK'
            exchange = 'SMART'
            contract = defineContract(symbol=stock,secType=secType,exchange=exchange)
            order = createOrder(action='BUY',totalQuantity=quantity,orderType='MKT')
            #bot = TradingBot.Bot(action,quantity,limitPrice,takeProfitPrice,stopLossPrice,symbol,secType)

            app.placeOrder(app.nextorderId, contract, order)
            time.sleep(3)

            print('cancelling order')
            app.cancelOrder(app.nextorderId)

            time.sleep(3)
            app.disconnect()

            stocks.enviar_mensaje_long(stock,precio_entrada,operacion,stop_loss_price,take_profit_price)
            list_of_stocks.remove(stock)
            
            print('*'*80)

        elif condicion1_short==True & condicion2_short == True & condicion3_short == True: 
            #Mensaje
            #stock='PBR'
            precio_entrada_short=round(senal_entrada['Close'].iat[0],2)
            operacion = 'Sell Short'
            stop_loss_short_price = round(stocks.stop_loss_short(precio_entrada_short,riesgo),2)
            take_profit_short_price = round(stocks.take_profit_short(precio_entrada_short,beneficio),2)
            action ='SELL'
            quantity = 1
            limitPrice = precio_entrada_short
            takeProfitPrice = take_profit_short_price
            stopLossPrice = stop_loss_short_price
            symbol = stock
            secType = 'STK'
            exchange = 'SMART'
            contract = defineContract(symbol=stock,secType=secType,exchange=exchange)
            order = createOrder(action='SELL',totalQuantity=quantity,orderType='MKT')
            #bot = TradingBot.Bot(action,quantity,limitPrice,takeProfitPrice,stopLossPrice,symbol,secType)

            app.placeOrder(app.nextorderId, contract, order)
            time.sleep(3)

            print('cancelling order')
            app.cancelOrder(app.nextorderId)

            time.sleep(3)
            app.disconnect()
            
            # bot = TradingBot.Bot(action,quantity,limitPrice,takeProfitPrice,stopLossPrice,symbol,secType)

            stocks.enviar_mensaje_short(stock,precio_entrada_short,operacion,stop_loss_short_price,take_profit_short_price)

            list_of_stocks.remove(stock)

            print('*'*80)
        else:
            print('No hay condiciones para operar'+' '+stock)
            print('*'*80)

    time.sleep(10)


