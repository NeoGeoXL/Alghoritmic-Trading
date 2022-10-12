import time
import stocks as stocks 
from datetime import datetime
import pandas as pd
import strategy as strategy



stock='NVDA'
#Ratio Riesgo:Beneficio 1:2
riesgo=0.01
beneficio=0.02


#list_of_stocks=['PBR','MSFT','NVDA','NTDOY','TSLA','KHC','AMZN','GOOG','FB','TWTR','NIO','NKE','PFE','PEP','PG','PYPL','INTC','AMD','CSCO','V','VZ','WMT','XOM','JNJ','JPM','HD','MCD','KO','VVV','SONY']

#Anticrisis Stocks
list_of_stocks=['WMT','PG','MCD','HD','PFE','JNJ','KHC','CVX','PBR','COKE']

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
            stop_loss = round(stocks.stop_loss_long(precio_entrada,riesgo),2)
            take_profit=round(stocks.take_profit_long(precio_entrada,beneficio),2)
    
            stocks.enviar_mensaje_long(stock,precio_entrada,operacion,stop_loss,take_profit)
            list_of_stocks.remove(stock)
            
            print('*'*80)

        elif condicion1_short==True & condicion2_short == True & condicion3_short == True: 
            #Mensaje
            #stock='PBR'
            precio_entrada=round(senal_entrada['Close'].iat[0],2)
            operacion = 'Sell Short'
            stop_loss = round(stocks.stop_loss_short(precio_entrada,riesgo),2)
            take_profit=round(stocks.take_profit_short(precio_entrada,beneficio),2)
            
            stocks.enviar_mensaje_short(stock,precio_entrada,operacion,stop_loss,take_profit)

            list_of_stocks.remove(stock)

            print('*'*80)
        else:
            print('No hay condiciones para operar'+' '+stock)
            print('*'*80)

    time.sleep(3600)


