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
    #Listen for realtime bars
    def realTime(self, reqId, time, open, high, low, close,volume, wap, count):
        bot.on_bar_update(reqId, time, open, high, low, close,volume, wap, count)
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
        #Request market data
        self.ib.reqRealTimeBars(0,contract,5,'TRADES',1,[])



    
    #listen to socket in separate thread
    def run_loop(self):
        self.ib.run()
    #pass realtime bar data back to our bot object
    def on_bar_update(reqId, time, open, high, low, close,volume, wap, count):
        print(reqId)

bot = Bot()