import pandas as pd
import json
import requests
import time
import numpy as np
import consumirApi

#lista empresas
df = pd.read_excel("empresas.xlsx")


ano_inicio = 2016
ano_fim = 2022


for ano in range(ano_inicio, ano_fim+1):
     dividendo = []

     
     for  linha in df.iterrows():
          ticket = linha[1].ticket
          dividendo.append(consumirApi.dividendosAnoAjustado(ticket,ano))
    
                                        
    
     df['dividendo '+str(ano)] = dividendo


print(df)
df.to_excel("empresas_dividendos.xlsx")
