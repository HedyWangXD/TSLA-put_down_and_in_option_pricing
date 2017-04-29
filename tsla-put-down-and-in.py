#Download the historical data from Yahoo Finance, and take the adjusted close prices
#Choose the date from 2014.01.01 to 2017.04.19
from pandas.io.data import DataReader
from datetime import datetime
import numpy
import matplotlib.pyplot as plt


tsla_data = DataReader('TSLA',  'yahoo', datetime(2014, 4, 19), datetime(2017, 4, 19))

tsla = tsla_data['Adj Close']

#Calculate the daily returns, their mean and variance.
def daily_return(prices):
    return prices[1:] / prices[:-1].values-1
daily_return(tsla)

tsla_mean = numpy.mean(daily_return(tsla))
tsla_var = numpy.std(daily_return(tsla))


#Generate the random date that obeys normal distribution 
#The distribution has the same mean and variance with the daily returns above
length=len(tsla)
tsla_current = float(tsla[length-1])
n = 252

def stock_price():
    distr = numpy.random.normal(tsla_mean,tsla_var,n)
    parameter = distr+1
#Using the current price to generate prices in the coming year
    price = list()
    for i in range(0,n):
        top_i = parameter[:i]
        p = 1  
        for x in top_i:
            p *= x
        price.insert(i,tsla_current * p)
    return price
    
#pricing the option
barrier = tsla_current*0.7
put_strike = tsla_current

def payoffs(price):
    if min(price)<barrier:
        payoff = max(0,put_strike-price[n-1])
    else: payoff = 0
    return payoff

#Monte Carlo Simulation 
count = 200
item = []
for i in xrange(count):
    item.append(payoffs(stock_price()))

option_price = (sum(item) / count)
print option_price




    
    
    

