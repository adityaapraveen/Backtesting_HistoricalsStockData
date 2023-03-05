#!/usr/bin/env python
# coding: utf-8

# In[7]:

#Importing the required libraries
import pandas as pd
import yfinance as yf


# In[8]:

#Importing the database through yfinance
ticker = ["HDFCBANK.NS"]
tickerDf = yf.download(ticker, start = '2023-03-03', end = '2023-03-04', interval='15m')



# In[4]:

#Defininf Renko chart and brick size.
brick_size = 0.5
renko_df = pd.DataFrame(index=tickerDf.index)
renko_df['close'] = tickerDf['Close']
renko_df['bar_num'] = range(1, len(renko_df)+1)
renko_df['prev_close'] = renko_df['close'].shift(1)
renko_df['brick'] = (renko_df['close'] - renko_df['prev_close']).abs() // brick_size
renko_df['bar_type'] = ['up' if renko_df['close'].iloc[i] > renko_df['prev_close'].iloc[i] else 'down' for i in range(len(renko_df))]


# In[10]:

# Renko Trading strategy 
position = 'none'
profit = 0
for i in range(1, len(renko_df)):
    if position == 'none':
        if renko_df['bar_type'].iloc[i] == 'up' and renko_df['brick'].iloc[i] >= 2:
            position = 'long'
            entry_price = renko_df['close'].iloc[i]
        elif renko_df['bar_type'].iloc[i] == 'down' and renko_df['brick'].iloc[i] >= 2:
            position = 'short'
            entry_price = renko_df['close'].iloc[i]
    elif position == 'long':
        if renko_df['bar_type'].iloc[i] == 'down' and renko_df['brick'].iloc[i] >= 2:
            position = 'none'
            exit_price = renko_df['close'].iloc[i]
            profit += exit_price - entry_price
            entry_price = 0
        elif renko_df['close'].iloc[i] < entry_price - (2 * brick_size):
            position = 'none'
            exit_price = entry_price - (2 * brick_size)
            profit += exit_price - entry_price
            entry_price = 0
    elif position == 'short':
        if renko_df['bar_type'].iloc[i] == 'up' and renko_df['brick'].iloc[i] >= 2:
            position = 'none'
            exit_price = renko_df['close'].iloc[i]
            profit += entry_price - exit_price
            entry_price = 0
        elif renko_df['close'].iloc[i] > entry_price + (2 * brick_size):
            position = 'none'
            exit_price = entry_price + (2 * brick_size)
            profit += entry_price - exit_price
            entry_price = 0


# In[ ]:


#Gives True whenever there is opportunity to enter and false whenever it exits.
for i in range(1, len(renko_df)):
    if(renko_df['bar_type'].iloc[i] == 'down' and renko_df['brick'].iloc[i] >= 2):
        print("True")
    elif(renko_df['bar_type'].iloc[i] == 'up' and renko_df['brick'].iloc[i] >= 2):
        print("False")   




def backtest_renko_strategy(renko_df, brick_size, strategy_func):

    position = 'none'
    profit = 0
    for i in range(1, len(renko_df)):
        signal = strategy_func(renko_df, brick_size, i)
        if position == 'none':
            if signal == 'long' and renko_df['brick'].iloc[i] >= 2:
                position = 'long'
                entry_price = renko_df['close'].iloc[i]
            elif signal == 'short' and renko_df['brick'].iloc[i] >= 2:
                position = 'short'
                entry_price = renko_df['close'].iloc[i]
        elif position == 'long':
            if signal == 'short' and renko_df['brick'].iloc[i] >= 2:
                position = 'none'
                exit_price = renko_df['close'].iloc[i]
                profit += exit_price - entry_price
                entry_price = 0
            elif renko_df['close'].iloc[i] < entry_price - (2 * brick_size):
                position = 'none'
                exit_price = entry_price - (2 * brick_size)
                profit += exit_price - entry_price
                entry_price = 0
        elif position == 'short':
            if signal == 'long' and renko_df['brick'].iloc[i] >= 2:
                position = 'none'
                exit_price = renko_df['close'].iloc[i]
                profit += entry_price - exit_price
                entry_price = 0
            elif renko_df['close'].iloc[i] > entry_price + (2 * brick_size):
                position = 'none'
                exit_price = entry_price + (2 * brick_size)
                profit += entry_price - exit_price
                entry_price = 0
    return profit


# In[ ]:

#Returns the Profit or Loss incurred.
if profit > 0:
    print("profitable trade with profit of: ", profit)
else:
    print("unnprofitable trade with loss of: ",profit)



# In[ ]:


#example trading strategy, you can replace the code inside the finction with your strategy to test it.
def strategy_func(renko_df, brick_size, i):
    """
    A simple renko trading strategy that goes long when the current brick is an up brick and goes short when the current
    brick is a down brick.
    """
    if renko_df['bar_type'].iloc[i] == 'up':
        return 'long'
    elif renko_df['bar_type'].iloc[i] == 'down':
        return 'short'
    else:
        return 'none'

profit = strategy_func(renko_df, brick_size,i)


