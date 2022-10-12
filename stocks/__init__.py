import numpy as np
import pandas as pd
from datetime import datetime
from pandas_datareader import data as pdr
import yfinance as yf
import telegram 
import telegram_token
telegram_token=telegram_token.token
yf.pdr_override()


def get_stocks_data(stock):
    data = pdr.get_data_yahoo(stock, start = '2022-06-01', end=datetime.now(), interval="1h")  
    data = data.reset_index()
    return data 

def send_message(text): 
    bot = telegram.Bot(token=telegram_token)
    bot.sendMessage(chat_id='@stock_trading_signals1', text=text)

def calcular_el_1_por_ciento(valor):
    porcentaje=valor*0.01
    return porcentaje

def stop_loss_long(precio,riesgo):
    stop_loss=precio-(precio*riesgo)
    return stop_loss
def take_profit_long(precio,beneficio):
    take_profit=precio+(precio*beneficio)
    return take_profit

def stop_loss_short(precio,riesgo):
    stop_loss=precio+(precio*riesgo)
    return stop_loss
def take_profit_short(precio,beneficio):
    take_profit=precio-(precio*beneficio)
    return take_profit

def enviar_mensaje_long(stock,precio_entrada,operacion,stop_loss,take_profit):
    text='\U0001F4CC'+' '+'Accion :' +' '+ stock + \
    '\n'+ '\n'+ \
    '\U0001F4C9'+' '+'Tipo de operacion: '+ ' '+ operacion + \
    '\n'+ '\n' + \
    '\U0001F4B0'+' '+'Precio de entrada: ' + ' ' +'$'+str(precio_entrada) + \
    '\n'+ '\n' + \
    '\U0001F534'+' '+'Stop loss: ' + ' ' +'$'+str(stop_loss) + \
    '\n'+ '\n' + \
    '\U0001F7E2'+' '+'Take profit: ' + ' ' +'$'+str(take_profit) 
    send_message(text)

def enviar_mensaje_short(stock,precio_entrada,operacion,stop_loss,take_profit):        
    text='\U0001F4CC'+' '+'Accion :' +' '+ stock + \
    '\n'+ '\n'+ \
    '\U0001F4C9'+' '+'Tipo de operacion: '+ ' '+ operacion + \
    '\n'+ '\n' + \
    '\U0001F4B0'+' '+'Precio de entrada: ' + ' ' +'$'+str(precio_entrada) + \
    '\n'+ '\n' + \
    '\U0001F534'+' '+'Stop loss: ' + ' ' +'$'+str(stop_loss) + \
    '\n'+ '\n' + \
    '\U0001F7E2'+' '+'Take profit: ' + ' ' +'$'+str(take_profit) 

    send_message(text)