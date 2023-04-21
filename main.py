import pandas as pd
import json
import requests
import time
import numpy as np
import consumirApi

#lista empresas
df = pd.read_excel("empresas.xlsx")


ano = 2016
ano_fim = 2022

beta = []
dividendo_ano = []
dividendo_ano_fim = []
roes = []
cotacao_medias_inicio = []
cotacao_medias_fim = []
for  linha in df.iterrows():
     ticket = linha[1].ticket
     beta.append(consumirApi.betaRiscoIbov(ticket,ano-2,ano))
     dividendo_ano.append(consumirApi.dividendosAnoAjustado(ticket,ano))
     roes.append(consumirApi.roe(ticket,ano))
     cotacao_medias_inicio.append(consumirApi.cotacaoMedianaAno(ticket,ano))
     cotacao_medias_fim.append(consumirApi.cotacaoMedianaAno(ticket,ano_fim))
     dividendo_ano_fim.append(consumirApi.dividendosAnoAjustado(ticket,ano_fim))

df['cotacao_media'] = cotacao_medias_inicio
df['beta'] = beta
df['dividendo_ano'] = dividendo_ano
df['roe'] = roes
df['cotacao_medias_fim'] = cotacao_medias_fim
df['dividendo_ano_fim'] = dividendo_ano_fim
print(df)
df.to_excel("empresasB.xlsx")
