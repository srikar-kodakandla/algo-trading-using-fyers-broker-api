# algo-trading-using-fyers-broker-api

This program trades in stock market using fyers api . It buys when supertrend gives buy signal and sells if supertrend gives sell signal , if adx is below 30 it won't trade.
it selects supertrend values by bruteforcing all the possible combinations with past data of given stock . It selects stock day before the market opens.It selects the stocks to trade by checking list of stocks in chartink script , then it bruteforces best combination of supertrend combinations and trades with that supertrend combinations on the next day , it also messages you live alerts in telegram.

To start trading , run ipython3 fyers/strategy.py
To store live stock data in sql run ipython3 fyers/accounts_database.py

This code is kept publicly in github for educational purpose only .I am not responsible with your profit and losses.

