from analyzer import StockAnalyzer
from stock import Stock
from bs4 import BeautifulSoup
import pandas as panda
import yfinance as yf
import requests
import re
import datetime
import os
import openpyxl
import argparse


class StockScanner:
  
    def __init__(self):
        self.winner_stock_list = list()
        self.loser_stock_list = list()
  
  
    def generate_data(self, scan_back_to_date, username):
    
        print("Starting a new scan to generate stock data...")

        # The first page will be '1', but need to start it at '0' for the loop
        page_number = 0

        while True:

            # Used to compare to the scan_back_to_date to determine how far back to scan
            most_recent_scan_date = ''

            # Scrape the profit.ly page for the user and store it
            web_page = "https://profit.ly/user/" + username + "/trades?page=" + str(page_number + 1) + "&size=10"
            page = requests.get(web_page)

            # Create the main soup
            soup = BeautifulSoup(page.content, "html.parser")
        
            # This grabs the center feed of the page that contains every 'card'
            card_feed = soup.find("div", class_="col-md-8 col-lg-7 no-gutters")
        
            has_scanned_winners = False
        
            # Loop through each user's page twice. Once to grab the profit cards and 
            # once to grab all the loss cards
            for _ in range(2):

                # Grab either the profit cards or the loss cards
                if has_scanned_winners == False:
                    all_card_headers = card_feed.find_all("div", class_=re.compile("card-header bg-profitGreen"))
                    print("==== Scanning all profit cards... ====")
                else:
                    all_card_headers = card_feed.find_all("div", class_=re.compile("card-header bg-danger"))
                    print("==== Scanning all loss cards.. ====")
        
                # Grab specific info from individual cards
                for card_header in all_card_headers:
                    card_feed_info = card_header.find_next("div", class_="feed-info")
                    trade_date = card_feed_info.find_next('a', href=True, class_="text-muted").get_text()
                    trade_formatted_date = self.create_datetime(trade_date)

                    most_recent_scan_date = trade_formatted_date
            
                    # If the trade date of the card is before the scan_back_to_date, break
                    # because we should already have this info
                    if trade_formatted_date < scan_back_to_date:
                        break
            
                    stock_ticker = card_header.find_next('a', class_="trade-ticker").get_text()
                    trade_type = card_header.find_next('span', class_="trade-type").get_text()
            
                    if has_scanned_winners == False:
                        trade_profit = card_header.find_next('a', class_="text-white trade-up mr-1").get_text().strip()
                    else:
                        trade_profit = card_header.find_next('a', class_="text-white trade-down mr-1").get_text().strip()
                            
                    # Follow the link for even more specific trade info such as entry, exit, and position size
                    trade_url = card_feed_info.find_next('a', href=True, class_="text-muted").get('href')                
                    trade_page = requests.get("https://profit.ly" + trade_url)
                
                    specific_soup = BeautifulSoup(trade_page.content, "html.parser")
                    specific_trade_feed = specific_soup.find("div", class_="container feeds mb-0 border-bottom-0 pb-0")
                
                    trade_entry_and_exit = specific_trade_feed.find_all("td", align="right")
                    trade_entry = trade_entry_and_exit[0].get_text()
                    trade_exit = trade_entry_and_exit[1].get_text()
            
                    trade_position_size_table = specific_trade_feed.find_all("li", class_="list-group-item d-flex justify-content-between align-items-center")
                    trade_position_size = trade_position_size_table[1].span.get_text()
                    
                    trade_percentage_profit = trade_position_size_table[2].span.get_text().strip()
                
                    stock = Stock(stock_ticker, trade_type, trade_profit, trade_formatted_date, trade_entry, trade_exit, trade_position_size, trade_percentage_profit)
                
                    if has_scanned_winners == False:
                        self.winner_stock_list.append(stock)
                    else:
                        self.loser_stock_list.append(stock)

                has_scanned_winners = True

            if most_recent_scan_date < scan_back_to_date:
                break


    def create_datetime(self, date_string):

        # Split the date_string by whitespace and get the month and day
        # Strip the right side comma from the day
        month = date_string.split()[0]
        day = date_string.split()[1].rstrip(',')

        # Get the hour AND minute based on splitting on whitespace
        time = date_string.split()[2]

        # The hour will be in a twelve hour format to start
        # Split the hour and minute on the colon
        twelve_hour = time.split(':')[0]
        minute = time.split(':')[1]

        # Clock period refers to AM or PM
        clock_period = date_string.split()[3]

        twenty_four_hour = ''

        # Convert the hour from twelve hour format to a twenty four hour format
        if (clock_period == 'AM') and (twelve_hour == '12'):
            twenty_four_hour = '00'
        elif (clock_period == 'AM') and (twelve_hour == '10' or twelve_hour == '11'):
            twenty_four_hour = twelve_hour
        elif (clock_period == 'AM'):
            twenty_four_hour = '0' + twelve_hour
        elif (clock_period == 'PM') and (twelve_hour == '12'):
            twenty_four_hour = twelve_hour
        else:
            twenty_four_hour = str(int(twelve_hour) + 12)

        # Create a dictionary to switch the 3 letter month abbreviation to a number
        month_switcher = {
            'Jan': '01',
            'Feb': '02',
            'Mar': '03',
            'Apr': '04',
            'May': '05',
            'Jun': '06',
            'Jul': '07',
            'Aug': '08',
            'Sep': '09',
            'Oct': '10',
            'Nov': '11',
            'Dec': '12'
        }

        # Change the month format by calling the dictionary above
        formatted_month = month_switcher.get(month, "Invalid Month")

        # The year is not reported in the scraped time, so will assume the year is the current year
        current_year = datetime.datetime.now().year

        formatted_datetime = datetime.datetime(int(current_year), int(formatted_month), int(day), int(twenty_four_hour), int(minute))
        print(f"\n*** FORMATTED DATE: {formatted_datetime} ***\n")
        return formatted_datetime


    # Use pandas to create an excel workbook with two sheets, winners and losers, and create
    # all the column headers
    def create_stock_workbook(self, username):
        stock_dataframe = panda.DataFrame(columns=['Date', 'Ticker', 'Trade Type', 'Profit', 'Entry', 'Exit', 'Position Size', 'Percent Profit',
                                                    'SPACE', 'L:H', 'Volume', 'SPACE', 'L:H (-) 1 Day', 'L:H (-) 2 Days', 'Volume (-) 1 Day', 
                                                    'Volume (-) 2 Days', '% Change From Open', '% Change (-) 1 Day', '% Change (-) 2 Days',
                                                    '% Change Volume (-) 1 Day', '% Change Volume (-) 2 Days', 'SPACE',
                                                    'Float Shares', 'Shares Outstanding', 'Implied Shares Outstanding'])
        writer = panda.ExcelWriter('stocks_' + username + '.xlsx', engine='xlsxwriter')
        stock_dataframe.to_excel(writer, sheet_name='winners', index=False)
        stock_dataframe.to_excel(writer, sheet_name='losers', index=False)
        writer.save()
        print("Empty stock workbook with headers created...")


    # Add the trade data and the stock analysis data to the excel workbook
    def populate_stock_workbook(self, winner_stock_list, loser_stock_list, username):
        print("Attempting to populate data...")
        stock_workbook = openpyxl.load_workbook('./stocks_' + username + '.xlsx')
        winner_sheet = stock_workbook.get_sheet_by_name('winners')
        loser_sheet = stock_workbook.get_sheet_by_name('losers')
        
        stock_workbook.active = winner_sheet

        for stock in winner_stock_list:
            print(f"Adding data for winning ticker: {stock.ticker}")
            winner_sheet.append([stock.date, stock.ticker, stock.trade_type, stock.profit, stock.entry, stock.exit, stock.position_size, stock.percent_profit,\
                                "N/A", str(stock.todays_low) + ':' + str(stock.todays_high), stock.todays_volume, "N/A", str(stock.yesterdays_low) + ':' + str(stock.yesterdays_high),\
                                str(stock.minus_two_days_low) + ':' + str(stock.minus_two_days_high), stock.yesterdays_volume, stock.minus_two_days_volume,\
                                stock.price_percent_change_today, stock.price_percent_change_since_yesterday, stock.price_percent_change_since_two_days,\
                                stock.volume_percent_change_since_yesterday, stock.volume_percent_change_since_two_days, "N/A",\
                                stock.float, stock.shares_outstanding, stock.implied_shares_outstanding])
            
        stock_workbook.active = loser_sheet
    
        for stock in loser_stock_list:
            print(f"Adding data for losing ticker: {stock.ticker}")
            loser_sheet.append([stock.date, stock.ticker, stock.trade_type, stock.profit, stock.entry, stock.exit, stock.position_size, stock.percent_profit,\
                                "N/A", str(stock.todays_low) + ':' + str(stock.todays_high), stock.todays_volume, "N/A", str(stock.yesterdays_low) + ':' + str(stock.yesterdays_high),\
                                str(stock.minus_two_days_low) + ':' + str(stock.minus_two_days_high), stock.yesterdays_volume, stock.minus_two_days_volume,\
                                stock.price_percent_change_today, stock.price_percent_change_since_yesterday, stock.price_percent_change_since_two_days,\
                                stock.volume_percent_change_since_yesterday, stock.volume_percent_change_since_two_days, "N/A",\
                                stock.float, stock.shares_outstanding, stock.implied_shares_outstanding])

        stock_workbook.save('stocks_' + username + '.xlsx')
    

    # Analyze each trades stock data from Yahoo Finance
    def perform_stock_analysis(self, stock_list):
        for stock in stock_list:
            stock_analyzer = StockAnalyzer(stock)
            stock_analyzer.analyze()
        

# Called when an excel workbook does not already exist for a user.
# Calls the main functions throughout the program to create the excel workbook, scrape and generate
# the data, perform analysis, and populate the data into the excel workbook
def create_new_stock_data(stock_scan, username):
    print("A workbook does not exist.. Creating a new stock workbook")
    stock_scan.create_stock_workbook(username)
    
    date = request_scan_back_date()

    stock_scan.generate_data(date, username)
    stock_scan.perform_stock_analysis(stock_scan.winner_stock_list)
    stock_scan.perform_stock_analysis(stock_scan.loser_stock_list)
    stock_scan.populate_stock_workbook(stock_scan.winner_stock_list, stock_scan.loser_stock_list, username)


# Called when an excel workbook already exists and contains users data.
# Pulls the latest data entry's date and will then perform the main functions of the program
# such as scraping, analysis, and data population 
def update_existing_stock_data(stock_scan, username):
    print("A workbook already exists... Reading the latest entry date")
    
    most_recent_stock_date = ''
    
    data_frame = panda.read_excel('./stocks_' + username + '.xlsx', sheet_name='winners')
    try:
        recent_winner_date = data_frame['Date'][0]
    except IndexError:
        print("Scanning the winner sheet produced an IndexError, most likely there are no entries")
        recent_winner_date = datetime.datetime(1970, 1, 1)
    data_frame = panda.read_excel('./stocks_' + username + '.xlsx', sheet_name='losers')
    try:
        recent_loser_date = data_frame['Date'][0]
    except IndexError:
        print("Scanning the loser sheet produced an IndexError, most likely there are no entries")
        recent_loser_date = datetime.datetime(1970, 1, 1)
    
    if recent_winner_date > recent_loser_date:
        most_recent_stock_date = recent_winner_date
    else:
        most_recent_stock_date = recent_loser_date

    print(f"Most recent stock entry date: {most_recent_stock_date}")

    stock_scan.generate_data(most_recent_stock_date, username)
    stock_scan.perform_stock_analysis(stock_scan.winner_stock_list)
    stock_scan.perform_stock_analysis(stock_scan.loser_stock_list)
    stock_scan.populate_stock_workbook(stock_scan.winner_stock_list, stock_scan.loser_stock_list, username)


# Used to ask to user for a date to scan trades back to
def request_scan_back_date():
    print("*** Requesting a date to scan stocks back to.. ***")
    month = input("Enter the numerical value for a month: ")
    day = input("Enter a numerical value for a day: ")
    year = input("Enter a numerical value for a year: ")
    hour = input("Enter a 24-hour clock hour: ")
    minute = input("Enter a minute: ")

    date = datetime.datetime(int(year), int(month), int(day), int(hour), int(minute))
    return date


def _arg_parse():
    parser = argparse.ArgumentParser(description="Scan the provided username's profit.ly trades, add the data to an excel workbook, and analyze the stock's data and history.")
    parser.add_argument("--username",
            help="The username of the profit.ly account you want to scan")
    return parser.parse_args()


def main(args):
  
    username = args.username
    stock_scan = StockScanner()

    print("Checking if a stock workbook already exists for " + username + "...")
    
    if not os.path.exists("./stocks_" + username + ".xlsx"):
        create_new_stock_data(stock_scan, username)
    else:
        update_existing_stock_data(stock_scan, username)

if __name__ == "__main__":
    args = _arg_parse()
    main(args)
