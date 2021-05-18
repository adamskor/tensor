import openpyxl as xl
from pathlib import Path
import json
import datetime as dt
import pandas_datareader as web
import random as rd
dicts = []
number_of_tickers = 10
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

def parse_trends(ticker_name, start = dt.datetime(2011,1,1),stop = dt.datetime(2021,5,15)):


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
        #print(i)
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
    avgupday = []
    try:
        for p in oneday:
            print(p)
            avgdown.append(p[1])
            avgupday.append(p[2])
            avgup.append(p[3])
        ticker_name['oneday'] = [len(oneday)/len(simp_trend.values()), sum(avgdown)/len(avgdown), sum(avgup)/len(avgup), sum(avgupday)/len(avgupday)]
    except:
        pass
        avgdown = []
        avgup = []
        avgupday = []
    try:
        for p in twoday:
            avgdown.append(p[1])
            avgupday.append(p[2])
            avgup.append(p[3])
        ticker_name['twoday'] = [len(twoday)/len(simp_trend.values()), sum(avgdown)/len(avgdown), sum(avgup)/len(avgup), sum(avgupday)/len(avgupday)]
    except:
        pass
        avgdown = []
        avgup = []
        avgupday = []
    try:
        for p in threeday:
            avgdown.append(p[1])
            avgupday.append(p[2])
            avgup.append(p[3])
        ticker_name['threeday'] = [len(threeday)/len(simp_trend.values()), sum(avgdown)/len(avgdown), sum(avgup)/len(avgup), sum(avgupday)/len(avgupday)]
    except:
        pass
        avgdown = []
        avgup = []
        avgupday = []
    try:
        for p in fourday:
            avgdown.append(p[1])
            avgupday.append(p[2])
            avgup.append(p[3])
        ticker_name['fourday'] = [len(fourday)/len(simp_trend.values()), sum(avgdown)/len(avgdown), sum(avgup)/len(avgup), sum(avgupday)/len(avgupday)]
    except:
        pass
        avgdown = []
        avgup = []
        avgupday = []
    try:
        for p in fiveday:
            avgdown.append(p[1])
            avgupday.append(p[2])
            avgup.append(p[3])
        ticker_name['fiveday'] = [len(fiveday)/len(simp_trend.values()), sum(avgdown)/len(avgdown), sum(avgup)/len(avgup), sum(avgupday)/len(avgupday)]
    except:
        pass

    return ticker_name
    #dicts.append(ticker_name)




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
    print(tickers)
    start = dt.datetime(2021,5,10)
    stop = dt.datetime(2021,5,11)
    for n,i in enumerate(tickers[:10000]):
        if n % 10 == 0:
            print(n)
        try:
            data = web.DataReader(i, 'yahoo', start, stop)
            valid_t['Tickers'].append(i)
        except:
            print(i + ' is not in Yahoo database')
    with open('data/validtickers1.json', 'w') as f:
        json.dump(valid_t, f)


def parse_tickers():
    with open('data/validtickers.json', 'r') as f:
        data = json.load(f)
    for i in data['Tickers']:
        print(i)
        piss = get_average_trends(i)
        print(piss)
        with open('data/tickerdata/' + i + '.json', 'w') as f:
           json.dump(piss, f)


#parse_tickers()
#with open('data/tickeravg.json', 'w') as f:
#    json.dump(dicts, f)
def decide_buys(recommendations):
    buys = {}
    rec_with_scores = {}
    for key, value in recommendations.items():
    #    print(key, value)
        score = 0.1*value[0] +0.3*value[1] + 0.1*value[2]
    #    print(score)
        value.insert(2, score)
    #    print(value)
        rec_with_scores[key] = value
    sorted_shit = sorted(rec_with_scores.items(), reverse = True, key = lambda e: e[1][2])
    buy = sorted_shit[:3]
    for i in buy:
        buys[list(i)[0]] = list(i)[1][0]
    return buys


def test(current_date):
    days = {1 : 'oneday', 2 : 'twoday', 3 : 'threeday', 4 : 'fourday' , 5 : 'fiveday'}
    delta = dt.timedelta(6)
    start = current_date - delta
    dict = {}
    recommendations = {}
    with open('data/validtickers.json', 'r') as f:
        data = json.load(f)
    for k, i in enumerate(data['Tickers'][:number_of_tickers]):
        #print(k)
        try:
            temp = []
            data = web.DataReader(i, 'yahoo', start, current_date)['Close']
            data = data.tolist()
            #print(data)
            if data[-2] > data[-1]:
                temp.append(data[-1])
                temp.append(data[-2])
                if data[-3] > data[-2]:
                    temp.append(data[-3])
                    if data[-4] > data[-3]:
                        temp.append(data[-4])
                        if data[-5] > data[-4]:
                            temp.append(data[-5])
            if len(temp) > 1:
                down_len = len(temp)
                dict[i] = temp
                with open('data/tickerdata/' + i +'.json', 'r') as f:
                    data = json.load(f)
                #print(temp)
                interest = data[days[down_len]]
                #print(interest)
                down_size = ((temp[down_len-1] - temp[0])/temp[0])*100
                #print(down_size)
                #if down_size > interest[1] and interest[2] > 1:
                if interest[2] > 1:
                    recommendations[i] = [round(interest[3]), down_len, interest[2]] #days to keep, days of donwtrend, size of uptrend
        except:
            pass
    return decide_buys(recommendations)


def test_profit(date):
    buy = test(date)
    inc_one = dt.timedelta(1)
    profit_data = {}
    for key, days in buy.items():
        delta = dt.timedelta(days+1)
        date_sell = date + delta
        data = web.DataReader(key, 'yahoo', date, date_sell)['Close']
        while len(data.tolist()) < days + 1:
            date_sell += inc_one
            data = web.DataReader(key, 'yahoo', date, date_sell)['Close']
        #print(data)
        purchase_price = data.tolist()[0]
        sell_price = data.tolist()[days]
        profit = sell_price - purchase_price
        perc_profit = ((sell_price - purchase_price)/purchase_price)*100
        perc_profit = round(perc_profit, 4)
        #print(profit)
        profit_data[key] = perc_profit
        #print('For ticker ' + key + ': '+ str(perc_profit) + '% profit/loss')
    return profit_data

def test_profit_with_courtage(date):
    buy = test(date)
    inc_one = dt.timedelta(1)
    profit_data = {}
    for key, days in buy.items():
        try:
            delta = dt.timedelta(days+1)
            date_sell = date + delta
            while True:
                try:
                    tst2 = web.DataReader(key, 'yahoo', date_sell, date_sell)['Close']
                    break
                except:
                    date_sell = date_sell + inc_one

            data = web.DataReader(key, 'yahoo', date, date_sell)['Close']
            while len(data.tolist()) < days + 1:
                date_sell += inc_one
                data = web.DataReader(key, 'yahoo', date, date_sell)['Close']
            #print(data)
            purchase_price = data.tolist()[0]*1.0025
            sell_price = data.tolist()[days]*(1-0.0025)
            n = 2
            while purchase_price < 100:
                print(purchase_price)
                print(sell_price)
                purchase_price = purchase_price*n
                sell_price = sell_price*n
                n += 1
            profit = sell_price - purchase_price
            #perc_profit = ((sell_price - purchase_price)/purchase_price)*100
            #perc_profit = round(perc_profit, 4)
            #print(profit)
            profit_data[key] = profit
            #print('For ticker ' + key + ': '+ str(perc_profit) + '% profit/loss')
        except:
            pass
    return profit_data

def test_dates():
    date = dt.datetime(2012,1,1)
    for i in range(25):
        test_date = date + dt.timedelta(rd.randint(0, 3000))
        profit_data = test_profit(test_date)

        print('For '+ str(test_date) + ' the profits were ')
        print(profit_data.items())
            #print(i, data)

def test_a_set_period():
    date = dt.datetime(2018,8,5)
    inc_one = dt.timedelta(1)
    profit = 0
    for i in range(25):
        while True:
            try:
                tst1 = web.DataReader('AAPL', 'yahoo', date, date)['Close']
                break
            except:
                date = date + inc_one
        test_date = date + dt.timedelta(i)
        profit_data = test_profit_with_courtage(test_date)
        for p in profit_data.values():
            print(p)
            profit = profit + p
        print('For '+ str(test_date) + ' the profits were ')
        print(profit_data.items())
        print('Profit so far: ')
        print(round(profit,3))
#test_profit(dt.datetime(2020,5,17))
#test_dates()
test_a_set_period()
#parse_tickers()
#get_valid_tickers()
