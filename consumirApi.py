import pandas as pd
import json
import requests
import time
import numpy as np
import autorizacao

 
def betaRiscoIbov(ticket, ano_inicial, ano_final):
    beta = -999
    print("Risco do Ticket ",ticket)
    while beta == -999:
        time.sleep(5)
        req = "https://api.dadosdemercado.com.br/v1/tickers/"+ticket+"/risk_measures/IBOV?period_init="+str(ano_inicial)+"-01-01&period_end="+str(ano_final)+"-12-31"
        response = requests.get(req
            , headers=autorizacao.headers())
    
        #print(response.text)
        if response.text == '{"error":"Rate limit"}' :
            #deu erro
            beta = -999
        elif response.text == '[]':
            beta = 0
        else:
            risco = pd.read_json(response.text)  
            beta = risco.beta[0]
        print(beta)

    return beta


def dividendosAnoAjustado(ticket, ano):
    print("Dividento do Ticket ",ticket)
    time.sleep(5)
    response = requests.get("https://api.dadosdemercado.com.br/v1/companies/"+ticket+"/dividends", headers=autorizacao.headers())
    #print(response.text)
    dividendos = pd.read_json(response.text)
    if dividendos.size == 0:
        return 0

    dividendos['record_date'] = pd.to_datetime(
            dividendos['record_date'])
    dividendos['year'] = dividendos.record_date.apply(lambda x: x.year)
    dividendos = dividendos.query('ticker=="'+ticket+'"')
    dividendos = dividendos.query('year == '+str(ano)+' ')
    time.sleep(5)

    response = requests.get(
        "https://api.dadosdemercado.com.br/v1/companies/"+ticket+"/splits", headers=autorizacao.headers())
    #print(response.text)
    dividendos_ajustados = np.zeros(len(dividendos.index))
    splits = pd.read_json(response.text)
    if splits.size > 0:
        splits = splits.query('ticker=="'+ticket+'"')

        for split in splits.values:
            i = 0
            for dividendo in dividendos.values:
                if(dividendos_ajustados[i] == 0):
                    dividendos_ajustados[i] = dividendo[0]

                if(split[2] > dividendo[3]):
                    print("Dividendo ",dividendo[0])
                    print("Split",split[4].split(":")[1])
                    dividendos_ajustados[i] = (
                        dividendo[0] / int(split[4].split(":")[1]))
                    print("div ajustado",  dividendos_ajustados[i])
                i += 1

        dividendos["dividendos_ajustados"] = dividendos_ajustados
    else:
        dividendos["dividendos_ajustados"] = dividendos.amount

    dividendos_ano = dividendos.groupby(by=["year"]).sum()

    try:
        total = dividendos_ano.at[ano, 'dividendos_ajustados']
    except KeyError:
        total = 0         
    
    return total

def roe(ticket, ano):
    print("Roe do Ticket ",ticket)
    time.sleep(5)
    response = requests.get(
        "https://api.dadosdemercado.com.br/v1/companies/"+ticket+"/ratios?period_type=year", headers=autorizacao.headers())
    
    #print(response.text)
    indicador = pd.read_json(response.text)
    try:
        indicador['periodo'] = pd.to_datetime(
                indicador['period_init'])
        
        indicador['year'] = indicador.periodo.apply(lambda x: x.year)
        indicador = indicador.query('year == '+str(ano)+' ')

        roe =np.double(indicador.return_on_equity)
    except:
        roe = 0

    return roe

def lucro(ticket, ano):
    print("net_income do Ticket ",ticket)
    time.sleep(5)
    response = requests.get(
        "https://api.dadosdemercado.com.br/v1/companies/"+ticket+"/incomes?period_type=year", headers=autorizacao.headers())
    
    #print(response.text)
    indicador = pd.read_json(response.text)
    try:
        indicador['periodo'] = pd.to_datetime(
                indicador['period_init'])
        
        indicador['year'] = indicador.periodo.apply(lambda x: x.year)
        indicador = indicador.query('year == '+str(ano)+' ')

        lucro =np.double(indicador.net_income)
    except:
        lucro = 0

    return lucro 

def patrimonio(ticket, ano):
    print("net_income do Ticket ",ticket)
    time.sleep(5)
    response = requests.get(
        "https://api.dadosdemercado.com.br/v1/companies/"+ticket+"/balances?statement_type=con&reference_date="+str(ano)+"-12-31", headers=autorizacao.headers())
    
    #print(response.text)
    balanco= pd.read_json(response.text)
    try:
        balanco['periodo'] = pd.to_datetime(
                balanco['reference_date'])
        
        balanco['year'] = balanco.periodo.apply(lambda x: x.year)
        balanco = balanco.query('year == '+str(ano)+' ')

        equity =np.double(balanco.equity)
    except:
        equity = 0

    return equity 

def cotacaoMedianaAno(ticket, ano):
    time.sleep(5)
    response = requests.get(
        "https://api.dadosdemercado.com.br/v1/tickers/"+ticket+"/quotes?period_init="+str(ano)+"-01-01&period_end="+str(ano)+"-12-31", headers=autorizacao.headers())
    
    #print(response.text)
    cotacao = pd.read_json(response.text)
    try:
        cotacao['date'] = pd.to_datetime(
                cotacao['date'])
        
        cotacao['year'] = cotacao.date.apply(lambda x: x.year)
        cotacao_ano = cotacao.groupby(by=["year"]).mean()

        cotacao_media =cotacao_ano.at[ano, 'adj_close']
        print("cotacao media",cotacao_media)
    except:
        cotacao_media = 0

    return cotacao_media

def indicadores(ticket, ano):
    print("indicadores ",ticket)
    time.sleep(5)
    response = requests.get(
        "https://api.dadosdemercado.com.br/v1/companies/"+ticket+"/market_ratios?statement_type=con&period_init="+str(ano)+"-01-01&period_end="+str(ano)+"-12-31", headers=autorizacao.headers())
    
    #print(response.text)
    market_ratios =[]
    try:
        market_ratios = pd.read_json(response.text)  
        market_ratios['date'] = pd.to_datetime(
                market_ratios['reference_date'])
        
        market_ratios['year'] = market_ratios.date.apply(lambda x: x.year)
        market_ratios_ano = market_ratios.groupby(by=["year"]).mean()    
       
    except:
        data = {'year':  [ano],
        'price': [0],
        'shares': [0],
        'equity_per_share': [0],
        'earnings_per_share': [0],
        'price_earnings': [0],
        'price_to_book': [0],
        'ebit_per_share': [0],
        }

        market_ratios = pd.DataFrame(data)
        market_ratios_ano = market_ratios.groupby(by=["year"]).mean()   
        
    return market_ratios_ano 