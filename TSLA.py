from pandas.io.data import DataReader
from datetime import datetime
import numpy
import matplotlib.pyplot as plt

#Download TSLA's adjusted close prices as historical data from Yahoo Finance
#Choose the date from 2014.04.19 to 2017.04.19
tsla_data = DataReader('TSLA',  'yahoo', datetime(2014, 4, 19), datetime(2017, 4, 19))
tsla = tsla_data['Adj Close']

#Calculate the daily returns, their mean and volatility.
def daily_return(prices):
    return numpy.log(prices[1:].values) - numpy.log(prices[:-1].values)
daily=daily_return(tsla)

tsla_mean = numpy.mean(daily)
#In more discussion
#tsla_mean = 0
tsla_vol = numpy.std(daily)


#Generate the random price assuming that obeys lognormal distribution 
#The distribution has the same mean and volatility with the daily returns above
length=len(tsla)
tsla_current = float(tsla[length-1])
n = 252

def stock_price():
    distr = numpy.random.normal(tsla_mean,tsla_vol,n)
    #Using the current price to generate prices in the coming year
    simu_return = list()
    for i in range(0,n-1):
        simu_return.append(sum(distr[:i]))
    price = tsla_current * numpy.exp(simu_return)
    return price
    
#pricing the option
barrier = tsla_current*0.7
put_strike = tsla_current

def payoffs(price):
    if min(price)<barrier:
        payoff = max(0,put_strike-price[n-2:n-1])
    else: payoff = 0
    return payoff
 
 
#Graphs of the Monte Carlo Simulation example
for i in range(0,10):
    a = stock_price()
    plt.plot(a)
    i = i + 1

plt.plot(numpy.linspace(0,252,252),numpy.ones(252)*tsla_current*0.7)
    
plt.show()


#Monte Carlo Simulation 
count = 10000
item = []
for i in xrange(count):
    item.append(payoffs(stock_price()))
option_price = (sum(item) / count)

print 'The option price is: '
print option_price




    
    
    

