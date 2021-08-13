import yfinance as yf
import pandas as pd
from datetime import timedelta

class StockAnalyzer:
  
  def __init__(self, stock):
    self.stock = stock
    self.ticker_symbol = stock.ticker
  #def __init__(self, ticker_symbol):
  #  self.ticker_symbol = ticker_symbol

  def analyze(self):
    print(f"Starting analysis on {self.ticker_symbol}")
    self.pull_stock_info()
    self.get_share_info(self.ticker)
    self.create_stock_dataframe(self.ticker, self.stock.date)
    self.get_stock_highs(self.ticker_history_dataframe)
    self.get_stock_lows(self.ticker_history_dataframe)
    self.get_stock_volume(self.ticker_history_dataframe)
    self.calculate_percent_change_price(self.ticker_history_dataframe)
    self.calculate_percent_change_volume(self.ticker_history_dataframe)


  def pull_stock_info(self):
    self.ticker = yf.Ticker(self.ticker_symbol)
  
  def get_share_info(self, ticker):
    self.stock.float = ticker.info['floatShares']
    self.stock.shares_outstanding = ticker.info['sharesOutstanding']
    self.stock.implied_shares_outstanding = ticker.info['impliedSharesOutstanding']
    #self.float = ticker.info['floatShares']
    #self.shares_outstanding = ticker.info['sharesOutstanding']
    #self.implied_shares_outstanding = ticker.info['impliedSharesOutstanding']

  def create_stock_dataframe(self, ticker, trade_date):
    start_date = trade_date - timedelta(days=6)
    self.ticker_history_dataframe = ticker.history(start=start_date.date(), end=trade_date.date(), interval="1d")
    #self.ticker_history_dataframe = ticker.history(period="5d")
    self.ticker_history_dataframe = self.ticker_history_dataframe[::1]

  def get_stock_highs(self, dataframe):
    high_price_series = dataframe['High']
    self.stock.todays_high = str(round(high_price_series[0], 5))
    self.stock.yesterdays_high = str(round(high_price_series[1], 5))
    self.stock.minus_two_days_high = str(round(high_price_series[2], 5))
    self.stock.minus_three_days_high = str(round(high_price_series[3], 5))
    #self.todays_high = str(round(high_price_series[0], 5))
    #self.yesterdays_high = str(round(high_price_series[1]))
    #self.minus_two_days_high = str(round(high_price_series[2]))
    #self.minus_three_days_high = str(round(high_price_series[3]))

  def get_stock_lows(self, dataframe):
    low_price_series = dataframe['Low']
    self.stock.todays_low = str(round(low_price_series[0], 5))
    self.stock.yesterdays_low = str(round(low_price_series[1], 5))
    self.stock.minus_two_days_low = str(round(low_price_series[2], 5))
    self.stock.minus_three_days_low = str(round(low_price_series[3], 5))
    #self.todays_low = str(round(low_price_series[0]))
    #self.yesterdays_low = str(round(low_price_series[1]))
    #self.minus_two_days_low = str(round(low_price_series[2]))
    #self.minus_three_days_low = str(round(low_price_series[3]))

  def get_stock_volume(self, dataframe):
    volume_series = dataframe['Volume']
    self.stock.todays_volume = volume_series[0]
    self.stock.yesterdays_volume = volume_series[1]
    self.stock.minus_two_days_volume = volume_series[2]
    self.stock.minus_three_days_volume = volume_series[3]
    #self.todays_volume = volume_series[0]
    #self.yesterdays_volume = volume_series[1]
    #self.minus_two_days_volume = volume_series[2]
    #self.minus_three_days_volume = volume_series[3]

  def calculate_percent_change_price(self, dataframe):
    # Calculate % change today
    ticker_open = dataframe['Open'][0]
    ticker_close = dataframe['Close'][0]
    increase = ticker_close - ticker_open
    percent_gain = (increase / ticker_open) * 100
    self.stock.price_percent_change_today = str(round(percent_gain, 2))
    #self.price_percent_change_today = str(round(percent_gain, 2))

    # Calculate % change from today and yesterday
    ticker_open = dataframe['Open'][1]
    ticker_close = dataframe['Close'][0]
    increase = ticker_close - ticker_open
    percent_gain = (increase / ticker_open) * 100
    self.stock.price_percent_change_since_yesterday = str(round(percent_gain, 2))
    #self.price_percent_change_since_yesterday = str(round(percent_gain, 2))

    # Calculate % change from today to two days ago
    ticker_open = dataframe['Open'][2]
    ticker_close = dataframe['Close'][0]
    increase = ticker_close - ticker_open
    percent_gain = (increase / ticker_open) * 100
    self.stock.price_percent_change_since_two_days = str(round(percent_gain, 2))
    #self.price_percent_change_since_two_days = str(round(percent_gain, 2))

  def calculate_percent_change_volume(self, dataframe):
    # Calculate % change in volume from yesterday
    ticker_volume_today = dataframe['Volume'][0]
    ticker_volume_yesterday = dataframe['Volume'][1]
    increase = ticker_volume_today - ticker_volume_yesterday
    percent_change = (increase / ticker_volume_yesterday) * 100
    self.stock.volume_percent_change_since_yesterday = str(round(percent_change, 2))
    #self.volume_percent_change_since_yesterday = str(round(percent_change, 2))

    # Calculate % change in volume from two days ago
    ticker_volume_today = dataframe['Volume'][0]
    ticker_volume_minus_two = dataframe['Volume'][2]
    increase = ticker_volume_today - ticker_volume_minus_two
    percent_change = (increase / ticker_volume_minus_two) * 100
    self.stock.volume_percent_change_since_two_days = str(round(percent_change, 2))
    #self.volume_percent_change_since_two_days = str(round(percent_change, 2))

"""
# Get all available info for a specific ticker
ticker = yf.Ticker('HALB')

# Access  specific data in the ticker's information
#shares_outstanding = ticker.info['sharesOutstanding']
#implied_shares_outstanding = ticker.info['impliedSharesOutstanding']
#float_shares = ticker.info['floatShares']

#print(f"Shares Outstanding: {shares_outstanding}")
#print(f"Implied Shares Outstanding: {implied_shares_outstanding}")
#print(f"Float Shares: {float_shares}")

# Create a pandas dataframe from the tickers history of price info over the period of the last 5 days - inclusive of today
#ticker_history_dataframe = ticker.history(period="5d")
ticker_history_data = {'Open': [0.0372, 0.0450, 0.0400, 0.0501, 0.0262], 'High': [0.0372, 0.0450, 0.0420, 0.501, 0.0519], 
'Low': [0.0301, 0.0351, 0.0350, 0.0360, 0.0261], 'Close': [0.0314, 0.0362, 0.0397, 0.0370, 0.0511], 'Volume': [8652700, 8416400, 11127900, 44183100, 195024400]}
ticker_history_dataframe = pd.DataFrame(data=ticker_history_data)

print(f"ticker_history_dataframe type: {type(ticker_history_dataframe)}\n")
print("Printing the dataframe:")
print(ticker_history_dataframe)

# Reverse the dataframe to have today's date at the 'top' of the dataframe
#ticker_history_dataframe = ticker_history_dataframe[::-1]

# Create a pandas 'Series' from the ticker dataframe pulling the 'High' Column
high_price_series = ticker_history_dataframe['High']
print(f"\nhigh_price_series type: {type(high_price_series)}\n")
print("Printing the high_price_series:")
print(high_price_series)
print("\n")

# Get the highs
todays_high = high_price_series[0]
yesterdays_high = high_price_series[1]
minus_two_days_high = high_price_series[2]
minus_three_days_high = high_price_series[3]
#todays_high = str(round(todays_high, 5))
print(f"Today's High: {str(round(todays_high, 5))}")

# Get the lows
low_price_series = ticker_history_dataframe['Low']
todays_low = low_price_series[0]
yesterdays_low = low_price_series[1]
minus_two_days_low = low_price_series[2]
minus_three_days_low = low_price_series[3]
#todays_low = str(round(todays_low, 5))
print(f"Today's Low: {str(round(todays_low, 5))}")

# Get the volume
volume_series = ticker_history_dataframe['Volume']
todays_volume = volume_series[0]
yesterdays_volume = volume_series[1]
minus_two_days_volume = volume_series[2]
minus_three_days_volume = volume_series[3]
print(f"Today's Volume: {todays_volume}")

# Calculate % change today
ticker_open = ticker_history_dataframe['Open'][0]
ticker_close = ticker_history_dataframe['Close'][0]
#print(str(round(ticker_open, 5)))
#print(str(round(ticker_close, 5)))
increase = ticker_close - ticker_open
#print(increase)
percent_gain = (increase / ticker_open) * 100
percent_gain = str(round(percent_gain, 2))
print(f"Percent change from open: {percent_gain}%")

# Calculate % change from today and yesterday
ticker_open = ticker_history_dataframe['Open'][1]
ticker_close = ticker_history_dataframe['Close'][0]
increase = ticker_close - ticker_open
percent_gain = (increase / ticker_open) * 100
percent_gain = str(round(percent_gain, 2))
print(f"Percent change from yesterday's open: {percent_gain}%")

# Calculate % change from today to two days ago
ticker_open = ticker_history_dataframe['Open'][2]
ticker_close = ticker_history_dataframe['Close'][0]
increase = ticker_close - ticker_open
percent_gain = (increase / ticker_open) * 100
percent_gain = str(round(percent_gain, 2))
print(f"Percent change from two days ago open: {percent_gain}%")

# Calculate % change in volume from yesterday
ticker_volume_today = ticker_history_dataframe['Volume'][0]
ticker_volume_yesterday = ticker_history_dataframe['Volume'][1]
increase = ticker_volume_today - ticker_volume_yesterday
percent_change = (increase / ticker_volume_yesterday) * 100
percent_change = str(round(percent_change, 2))
print(f"Percent change in volume from yesterday: {percent_change}%")

# Calculate % change in volume from two days ago
ticker_volume_today = ticker_history_dataframe['Volume'][0]
ticker_volume_minus_two = ticker_history_dataframe['Volume'][2]
increase = ticker_volume_today - ticker_volume_minus_two
percent_change = (increase / ticker_volume_minus_two) * 100
percent_change = str(round(percent_change, 2))
print(f"Percent change in volume from two days ago: {percent_change}%")

"""