from ast import Pass
import ibapi
from ibapi.client import EClient
from ibapi.wrapper import EWrapper

from ibapi.contract import Contract
from ibapi.order import *
import threading
import time

#Class for the Interactive Brokers Connection

class IBApi(EWrapper,EClient):
    def __init__(self):
        EClient.__init__(self,self)

#Bot logic

class Bot:
    ib = None
    def __init__(self):
        #Conect to IB on init
        self.ib = IBApi()
        self.ib.connect('127.0.0.1',7497,1)
        ib_thread = threading.Thread(target=self.run_loop,daemon=True)
        ib_thread.start()
        time.sleep(1)
        #Get the symbol info
        symbol = input('Enter the symbol you want to trade: ')
        #Create our IB contract object
        contract = Contract()
        contract.symbol = symbol.upper()
        contract.secType = 'STK'
        contract.exchange = 'SMART'
        contract.currency = 'USD'
        #Create Order object
        order  = Order()
        order.orderType = 'MKT' #or LIMIT, ETC
        order.action = 'BUY' #or Sell
        quantity = 1
        order.totalQuantity = quantity
        #Create Contract Object
        contract = Contract()
        contract.symbol = symbol
        contract.secType = 'STK' #or FUT, etc
        contract.exchange = 'SMART'
        contract.primaryExchange = 'ISLAND'
        contract.currency = 'USD'
        #Place the order 
        self.ib.placeOrder(1,contract, order)


    #listen to socket in separate thread
    def run_loop(self):
        self.ib.run()


bot = Bot()


