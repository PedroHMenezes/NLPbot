import yfinance as yf
import re

def tickers (companies):
    tickers_list = re.findall(r'\b\w+\b', companies.upper())
    return tickers_list
    
def database (companies):
    tickers_list = re.findall(r'\b\w+\b', companies.upper())
    tickers_string = " ".join(tickers_list)
    df = yf.download(tickers = tickers_list,
                period="1y",
                interval = "1d",
                ignore_tz = True,
                prepost = False)
    return df

def last_price(company, df):
    if len(df.axes[1]) >  6:
        price = df['Close'].iloc[-2][company]
    else:
        price = df['Close'].iloc[-2]
    yf_company = yf.Ticker(company)
    currency = yf_company.info['financialCurrency']
    return 'O preço do fechamento de ontem para {0} é {1} {2:.2f}'.format(company, currency, price)

def return_1w(company, df):
    if len(df.axes[1]) >  6:
        retorno = (df['Close'].iloc[-2][company])/(df['Close'].iloc[-7][company])-1
    else:
        retorno = (df['Close'].iloc[-2])/(df['Close'].iloc[-7])-1
    return 'Retorno em 1 semana: {0:.2%}'.format(retorno)

def return_1m(company, df):
    if len(df.axes[1]) >  6:
        retorno = (df['Close'].iloc[-2][company])/(df['Close'].iloc[-24][company])-1
    else:
        retorno = (df['Close'].iloc[-2])/(df['Close'].iloc[-24])-1
    return 'Retorno em 1 mês: {0:.2%}'.format(retorno)

def return_1y(company, df):
    if len(df.axes[1]) >  6:
        retorno = (df['Close'].iloc[-2][company])/(df['Close'].iloc[0][company])-1
    else:
        retorno = (df['Close'].iloc[-2])/(df['Close'].iloc[0])-1
    return 'Retorno em 1 ano: {0:.2%}'.format(retorno)

