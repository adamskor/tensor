import datetime as dt
import pandas_datareader as web
import data_handler as dh
import json

max_follow_days = 5
def main():
    with open('data/validtickers.json', 'r') as f:
        data = json.load(f)
    valid_tickers = data['Tickers']
    start = dt.datetime(2021,5,1)
    stop = dt.datetime(2021,5,15)
    for i in valid_tickers[:1]:
        data = web.DataReader(i, 'yahoo', start, stop)
        data = data['Close']
        data = data.tolist()
        print(data)
        find_trends(start, data)

def find_trends(start, data):
    trends = []
    n = 0
    while n < len(data):
        print(n)
        current = data[n]
        i = 0
        down_trend = []
        while current >= data[i] and len(down_trend) < 5:
            down_trend.append(data[n + i])
            down_trend_len = len(down_trend)
            i += 1
            current = data[i]
        if down_trend_len > 1:
            trends.append(down_trend)
        n = n + i
        p = 1
        up_trend = []
        try:
            while p < max_follow_days + 1 and data[n + down_trend_len + p] >= data[n + down_trend_len + p - 1]:
                percentage_increase = (data[n + down_trend_len + p]/down_trend[-1] - 1)*100
                up_trend.append('After ' + str(p) + ' days we are up ' + str(round(percentage_increase, 3)) + '%')
                trends.append(up_trend)
                p += 1
        except IndexError:
            pass

        n += 1


    print(trends)

#main()





























if __name__ == '__main__':
    main()
