#Import the libraries
import math
#import pandas_datareader as web
import numpy as np
import pandas as pd
from sklearn.preprocessing import MinMaxScaler
import matplotlib.pyplot as plt#
plt.style.use('classic')
from datetime import datetime
import matplotlib.dates as mpl_dates
from pytz import utc



def ema(cierre,m_ema):
    ema=cierre.ewm(span=m_ema, adjust=False).mean()
    return ema

def tema(cierre,m_ema):
    ema1=ema(cierre,m_ema)
    ema2=ema(ema1,m_ema)
    ema3=ema(ema2,m_ema)
    tema=(3*ema1)-(3*ema2)+ema3
    return tema

def graficar_temas(cierre,tema_short,tema_long,tema_trend):
    fig, ax = plt.subplots(figsize=(16,9))
    ax.plot(cierre, label='Cierre',color='black',linewidth=2)
    ax.plot(tema_short, label='TEMA 50',color='red')
    ax.plot(tema_long, label='TEMA 100',color='blue')
    ax.plot(tema_trend, label='TEMA 200',color='green')
    ax.set_title('TRIPLE EXPONENTIAL MOVING AVERAGE')
    ax.set_ylabel('Price in $')
    ax.set_ylabel('Date')
    plt.grid(color='grey', linestyle='dotted', linewidth=1.5)
    plt.show()


def delta_temas(tema_short, tema_long):
    delta=tema_short-tema_long
    return delta


def condicion_temas(delta):  
    condicion = 'vacio'   
    if delta > 0:
        condicion = "Bull"
    elif delta < 0:
        condicion = "Bear" 
    return condicion


def condicion_tendencia_principal(close,trend):
    if close > trend:
        return 'Bull'
    elif close < trend:
        return 'Bear'
    else:
        return 'Vacio'

def rsi(df):
    pd.options.mode.chained_assignment = None  # default='warn'
    price=df['Close']
    df['Price Diff'] = price.diff(1)
    data = df[['Close','Price Diff']]
    data['gain'] = data['Price Diff'].clip(lower=0).round(2)
    data['loss'] = data['Price Diff'].clip(upper=0).abs().round(2)
    # Get initial Averages
    window_length=14
    data['avg_gain'] = data['gain'].rolling(window=window_length, min_periods=window_length).mean()[:window_length+1]
    data['avg_loss'] = data['loss'].rolling(window=window_length, min_periods=window_length).mean()[:window_length+1]
    # Get WMS averages
    # Average Gains
    for i, row in enumerate(data['avg_gain'].iloc[window_length+1:]):
        data['avg_gain'].iloc[i + window_length + 1] =\
            (data['avg_gain'].iloc[i + window_length] *
            (window_length - 1) +
            data['gain'].iloc[i + window_length + 1])\
            / window_length
    # Average Losses
    for i, row in enumerate(data['avg_loss'].iloc[window_length+1:]):
        data['avg_loss'].iloc[i + window_length + 1] =\
            (data['avg_loss'].iloc[i + window_length] *
            (window_length - 1) +
            data['loss'].iloc[i + window_length + 1])\
            / window_length
    rs = data['avg_gain'] / data['avg_loss']
    rsi = 100 - (100 / (1.0 + rs))
    return rsi

def condicion_rsi(rsi):
    condicion = 'vacio'
    if rsi >= 50:
        condicion = "Bull"
    elif rsi < 50:
        condicion = "Bear"
    return condicion


def stop_loss(capital,ratio_riesgo):
    x = capital * ratio_riesgo
    stoploss=capital-x
    return stoploss

def df_condiciones_entrada(df):
    tema_short=tema(df['Close'],m_ema=10)   #50
    tema_long=tema(df['Close'],m_ema=20)   #100
    tema_trend=tema(df['Close'],m_ema=50)  #200
    df['Trend']=tema_trend
    condiciones_df=pd.DataFrame()
    condiciones_df['Close']=df['Close'] #primera columna del df condiciones de entrada de operacion
    
    #CONDICION 1: TEMAS 

    delta=delta_temas(tema_short,tema_long)
    df['delta_temas'] = delta
    condicion1=df['delta_temas'].apply(condicion_temas)
    condiciones_df['Condicion 1']=condicion1     

    #CONDICION 2: TENDENCIA PRINCIPAL

    condicion2=df[['Close','Trend']].apply(lambda x: condicion_tendencia_principal(*x),axis=1)
    condiciones_df['Condicion 2']=condicion2


    #CONDICION 3: RSI

    df['rsi']= rsi(df)
    condicion3=df['rsi'].apply(condicion_rsi)
    condiciones_df['Condicion 3']=condicion3

    return condiciones_df

def senal_entrada(condiciones_df):
    senal_entrada=condiciones_df.iloc[-2:,:]    #N es el numero anterior al precio que me da la senal porque esa seria primero mi columna de estudio
    return senal_entrada

def condiciones_bool_long(senal_entrada):
    senal_condiciones_bool_long=senal_entrada.apply(lambda x: x=='Bull',axis=1)
    return senal_condiciones_bool_long

def condiciones_bool_short(senal_entrada):
    senal_condiciones_bool_short=senal_entrada.apply(lambda x: x=='Bear',axis=1)
    return senal_condiciones_bool_short

def condiciones_operar_long(senal_entrada):
    condiciones_bool=condiciones_bool_long(senal_entrada)
    condicion1_long=condiciones_bool['Condicion 1'].iat[0]
    condicion2_long=condiciones_bool['Condicion 2'].iat[0]
    condicion3_long=condiciones_bool['Condicion 3'].iat[0]
    return condicion1_long, condicion2_long, condicion3_long

def condiciones_operar_short(senal_entrada):
    condiciones_bool=condiciones_bool_short(senal_entrada)
    condicion1_short=condiciones_bool['Condicion 1'].iat[0]
    condicion2_short=condiciones_bool['Condicion 2'].iat[0]
    condicion3_short=condiciones_bool['Condicion 3'].iat[0]
    return condicion1_short, condicion2_short, condicion3_short


def quantity_orders(capital_por_operacion, df):
    quantity=capital_por_operacion/df['Close'].iat[0]
    return quantity

def comprar():
    print('Comprar ahorita cabronnnn')

def vender():
    print('Vender lo que compraste ahorita cabronnnn')