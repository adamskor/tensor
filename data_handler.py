import openpyxl as xl
from pathlib import Path
import json
import datetime as dt
import pandas_datareader as web
dicts = []

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

def parse_trends(ticker_name):
    start = dt.datetime(2011,1,1)
    stop = dt.datetime(2021,5,15)
    try:
        data = web.DataReader(ticker_name, 'yahoo', start, stop)
        data = data['Close']
        data = data.tolist()
    except:
        return {}

    n = 0
    temp_down = []
    down = []
    trend = {}
    counter = 0
    while n < len(data) - 1:
        if data[n] not in temp_down:
            temp_down.append(data[n])
        if data[n + 1] < data[n]:
            temp_down.append(data[n + 1])
            n += 1
        else:
            if len(temp_down) > 1:
                trend['trend' + str(counter)] = []
                trend['trend' + str(counter)].append(temp_down)
                temp_down = []
                trend = find_up(data, trend, counter, n+1)
                counter += 1
                n += 1
            else:
                temp_down = []
                n += 1

    return trend

def find_up(data, trend, counter, n):
    temp_up = []
    while n < len(data)-1:
        if data[n] not in temp_up:
            temp_up.append(data[n])
        if data[n+1] > data[n]:
            temp_up.append(data[n + 1])
            n += 1
        else:
            break
    if len(temp_up) > 0:
        trend['trend' + str(counter)].append(temp_up)
        return trend
        temp_up = []
        n += 1
    else:
        temp_up = []
        n += 1
    return trend


def simplify_trends(ticker_name):
    trends = parse_trends(ticker_name)
    simp_trend = {}
    for i in range(len(trends.keys())):
        try:
            down = trends['trend' + str(i)][0]
            simp_trend['trend' + str(i)] = []
            simp_trend['trend' + str(i)].append(len(down))
            simp_trend['trend' + str(i)].append((down[0]/down[-1] - 1)*100)
            up = trends['trend' + str(i)][1]
            simp_trend['trend' + str(i)].append(len(up))
            simp_trend['trend' + str(i)].append((up[-1]/down[-1] - 1)*100)
        except:
            pass
    return simp_trend

def write_json(new_data, filename='data/tickeravg.json'):
    with open(filename,'r+') as file:
          # First we load existing data into a dict.
        file_data = json.load(file)
        # Join new_dat3a with file_data
        file_data.update(new_data)
        # Sets file's current position at offset.
        file.seek(0)
        # convert back to json.
        json.dump(file_data, file, indent = 4)

def get_average_trends(ticker_name):
    global dicts
    simp_trend = simplify_trends(ticker_name)
    ticker = ticker_name
    ticker_name = {'Name' : ticker}
    oneday = []
    twoday = []
    threeday = []
    fourday = []
    fiveday = []
    for i in simp_trend.values():
        if i[0] == 2:
            oneday.append(i)
        if i[0] == 3:
            twoday.append(i)
        if i[0] == 4:
            threeday.append(i)
        if i[0] == 5:
            fourday.append(i)
        if i[0] == 6:
            fiveday.append(i)
    avgdown = []
    avgup = []
    try:
        for p in oneday:
            avgdown.append(p[1])
            avgup.append(p[3])
            ticker_name['oneday'] = [len(oneday)/len(simp_trend.values()), sum(avgdown)/len(avgdown), sum(avgup)/len(avgup)]
    except:
        pass
        avgdown = []
        avgup = []
    try:
        for p in twoday:
            avgdown.append(p[1])
            avgup.append(p[3])
            ticker_name['twoday'] = [len(twoday)/len(simp_trend.values()), sum(avgdown)/len(avgdown), sum(avgup)/len(avgup)]
    except:
        pass
        avgdown = []
        avgup = []
    try:
        for p in threeday:
            avgdown.append(p[1])
            avgup.append(p[3])
            ticker_name['threeday'] = [len(threeday)/len(simp_trend.values()), sum(avgdown)/len(avgdown), sum(avgup)/len(avgup)]
    except:
        pass
        avgdown = []
        avgup = []
    try:
        for p in fourday:
            avgdown.append(p[1])
            avgup.append(p[3])
            ticker_name['fourday'] = [len(fourday)/len(simp_trend.values()), sum(avgdown)/len(avgdown), sum(avgup)/len(avgup)]
    except:
        pass
        avgdown = []
        avgup = []
    try:
        for p in fiveday:
            avgdown.append(p[1])
            avgup.append(p[3])
            ticker_name['fiveday'] = [len(fiveday)/len(simp_trend.values()), sum(avgdown)/len(avgdown), sum(avgup)/len(avgup)]
    except:
        pass
    print(ticker_name)
    dicts.append(ticker_name)




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

def parse_tickers():
    with open('data/validtickers.json', 'r') as f:
        data = json.load(f)
    for i in data['Tickers']:
        print(i)
        get_average_trends(i)

parse_tickers()
with open('data/tickeravg.json', 'w') as f:
    json.dump(dicts, f)
