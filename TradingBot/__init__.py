from ast import Pass
from ib_insync import BracketOrder
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
    def __init__(self,action,quantity,limitPrice,takeProfitLimitPrice,stopLossPrice,symbol,secType):
        
        #Initializing strategy information
        self.action = action
        self.quantity = quantity
        self.limitPrice = limitPrice
        self.takeProfitLimitPrice = takeProfitLimitPrice
        self.stopLossPrice = stopLossPrice
        self.symbol = symbol
        self.secType = secType
        
        self.ib = IBApi()
        self.ib.connect('127.0.0.1',7497,1)
        self.ib_thread = threading.Thread(target=self.run_loop,daemon=True)
        self.ib_thread.start()

        #Create Order object
        #order  = BracketOrder(1,self.action,self.quantity,self.limitPrice, self.takeProfitLimitPrice,self.stopLossPrice)
        order = Order()
        #order.eTradeOnly = False
        #order.firmQuoteOnly = False
        order.orderType = 'MKT' #or LIMIT, ETC
        order.action = self.action #or Sell
        order.totalQuantity = self.quantity

        #Create Contract Object
        contract = Contract()
        contract.symbol = self.symbol
        contract.secType = self.secType
        contract.exchange = 'SMART'
        contract.primaryExchange = 'ISLAND'
        contract.currency = 'USD'
        self.ib.placeOrder(1,contract,order)
        
        '''self.order = self.createOrder()
        self.contract = self.createContract()
        self.submitOrder()'''
        
        
        #Conect to IB on init
    '''def conect(self):
        self.ib = IBApi()
        self.ib.connect('127.0.0.1',7497,1)
        ib_thread = threading.Thread(target=self.run_loop,daemon=True)
        ib_thread.start()
        time.sleep(1)
        return ib_thread'''
        
    '''def createOrder(self):
        #Create Order object
        #order  = BracketOrder(1,self.action,self.quantity,self.limitPrice, self.takeProfitLimitPrice,self.stopLossPrice)
        order = Order()
        order.orderType = 'MKT' #or LIMIT, ETC
        order.action = self.action #or Sell
        order.totalQuantity = self.quantity
        return order
    
    def createContract(self):
        #Create Contract Object
        contract = Contract()
        contract.symbol = self.symbol
        contract.secType = self.secType
        contract.exchange = 'SMART'
        contract.primaryExchange = 'ISLAND'
        contract.currency = 'USD'
        return contract
        #Place the order 
    
    def submitOrder(self):
        self.simplePlaceOid = self.nextOrderId()
        self.ib.placeOrder(self.simplePlaceOid,self.contract,self.order)
'''

    #listen to socket in separate thread
    def run_loop(self):
        self.ib.run() 


