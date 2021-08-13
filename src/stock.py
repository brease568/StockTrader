class Stock:
  
  def __init__(self, ticker, trade_type, profit, date, entry, exit, position_size, percent_profit):
    self.ticker = ticker
    self.trade_type = trade_type
    self.profit = profit
    self.date = date
    self.entry = entry
    self.exit = exit
    self.position_size = position_size
    self.percent_profit = percent_profit