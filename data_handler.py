import openpyxl as xl
from pathlib import Path
import json
import datetime as dt
import pandas_datareader as web

def extract_tickers():
    data = {}
    data['Data'] = []
    path_to_tickerdata = Path('data', 'ticker.xlsx')
    wb = xl.load_workbook(path_to_tickerdata)
    stocks_sheet = wb['Stock']
    for i in range(106328):
    #'Add progress bar
        if i % 10 == 0:
            print(i)
        dict = {'Ticker' : None, 'Name' : None, 'Exchange' : None, 'Category' : None, 'Country' : None}
        dict['Ticker'] = stocks_sheet['A' + str(i+5)].value
        dict['Name'] = stocks_sheet['B' + str(i+5)].value
        dict['Exchange'] = stocks_sheet['C' + str(i+5)].value
        dict['Category'] = stocks_sheet['D' + str(i+5)].value
        dict['Country'] = stocks_sheet['E' + str(i+5)].value
        data['Data'].append(dict)
    print(data)
    with open('data/data.json', 'w') as f:
        json.dump(data, f)



def get_all_tickers():
    tickers = []
    with open('data/data.json', 'r') as f:
        data = json.load(f)
        for i in data['Data']:
            tickers.append(i['Ticker'])
    return tickers

def get_valid_tickers():
    valid_t = {}
    valid_t['Tickers'] = []
    tickers = get_all_tickers()
    tickers = tickers[:1000]
    start = dt.datetime(2021,5,10)
    stop = dt.datetime(2021,5,11)
    for n,i in enumerate(tickers):
        if n % 10 == 0:
            print(n)
        try:
            data = web.DataReader(i, 'yahoo', start, stop)
            valid_t['Tickers'].append(i)
        except:
            print(i + ' is not in Yahoo database')
    with open('data/validtickers.json', 'w') as f:
        json.dump(valid_t, f)
