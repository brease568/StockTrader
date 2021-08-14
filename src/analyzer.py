import yfinance as yf
import pandas as pd
from datetime import timedelta


class StockAnalyzer:


    def __init__(self, stock):
        self.stock = stock
        self.ticker_symbol = stock.ticker


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


    def create_stock_dataframe(self, ticker, trade_date):
        start_date = trade_date - timedelta(days=6)
        self.ticker_history_dataframe = ticker.history(start=start_date.date(), end=trade_date.date(), interval="1d")

        # Reverse the dataframe so the most recent date is at the 'top' of the output
        self.ticker_history_dataframe = self.ticker_history_dataframe[::1]


    def get_stock_highs(self, dataframe):
        high_price_series = dataframe['High']
        self.stock.todays_high = str(round(high_price_series[0], 5))
        self.stock.yesterdays_high = str(round(high_price_series[1], 5))
        self.stock.minus_two_days_high = str(round(high_price_series[2], 5))
        self.stock.minus_three_days_high = str(round(high_price_series[3], 5))


    def get_stock_lows(self, dataframe):
        low_price_series = dataframe['Low']
        self.stock.todays_low = str(round(low_price_series[0], 5))
        self.stock.yesterdays_low = str(round(low_price_series[1], 5))
        self.stock.minus_two_days_low = str(round(low_price_series[2], 5))
        self.stock.minus_three_days_low = str(round(low_price_series[3], 5))


    def get_stock_volume(self, dataframe):
        volume_series = dataframe['Volume']
        self.stock.todays_volume = volume_series[0]
        self.stock.yesterdays_volume = volume_series[1]
        self.stock.minus_two_days_volume = volume_series[2]
        self.stock.minus_three_days_volume = volume_series[3]


    def calculate_percent_change_price(self, dataframe):
        # Calculate % change today
        ticker_open = dataframe['Open'][0]
        ticker_close = dataframe['Close'][0]
        increase = ticker_close - ticker_open
        percent_gain = (increase / ticker_open) * 100
        self.stock.price_percent_change_today = str(round(percent_gain, 2))

        # Calculate % change from today and yesterday
        ticker_open = dataframe['Open'][1]
        ticker_close = dataframe['Close'][0]
        increase = ticker_close - ticker_open
        percent_gain = (increase / ticker_open) * 100
        self.stock.price_percent_change_since_yesterday = str(round(percent_gain, 2))

        # Calculate % change from today to two days ago
        ticker_open = dataframe['Open'][2]
        ticker_close = dataframe['Close'][0]
        increase = ticker_close - ticker_open
        percent_gain = (increase / ticker_open) * 100
        self.stock.price_percent_change_since_two_days = str(round(percent_gain, 2))


    def calculate_percent_change_volume(self, dataframe):
        # Calculate % change in volume from yesterday
        ticker_volume_today = dataframe['Volume'][0]
        ticker_volume_yesterday = dataframe['Volume'][1]
        increase = ticker_volume_today - ticker_volume_yesterday
        percent_change = (increase / ticker_volume_yesterday) * 100
        self.stock.volume_percent_change_since_yesterday = str(round(percent_change, 2))

        # Calculate % change in volume from two days ago
        ticker_volume_today = dataframe['Volume'][0]
        ticker_volume_minus_two = dataframe['Volume'][2]
        increase = ticker_volume_today - ticker_volume_minus_two
        percent_change = (increase / ticker_volume_minus_two) * 100
        self.stock.volume_percent_change_since_two_days = str(round(percent_change, 2))
