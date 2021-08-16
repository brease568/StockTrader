# StockTrader
![GitHub code size in bytes](https://img.shields.io/github/languages/code-size/brease568/StockTrader)

The StockTrader project scans a provided username's online profit.ly account for historical stock trade information. Once the scan is complete the data is added to an excel workbook, and further stock information is pulled from Yahoo finance and analyzed. The analyzed stock information is also added to the excel workbook.

## Prerequisites

- Python 3
- An internet connection
- Ability to run programs from the command line
- Ability to create .xlxs files

## Dependencies

See the provided requirements.txt file.

## Modules Used

- BeautifulSoup
- Pandas
- openpyxl
- os
- requests
- re
- datetime
- yfinance
- argparse

## Usage

```bash
python3 main.py --help
python3 main.py --username {username}
```

## Execution Flow
### First execution (you have not scanned any user's account):
1. Look for an excel file in the current working directory of the program named 'stocks_{username}.xlsx'.
2. Create an empty excel workbook with column headers and two sheets, a winner and loser sheet.
3. The program will not find anything, so it will ask the user for input regarding a date that will be used to scan trades dating back to and NOT including that date.
4. Use BeautifulSoup to scrape trade data from a user's https://profit.ly/ account.
5. For each stock found being traded on the user's account, gather further information about the stock (high, low, volume, float, etc) from Yahoo Finance.
6. Perform analysis (% change in price, % change in volume, etc) on the information gained from Yahoo Finance on each stock for the past several days.
7. Add all of the trade information, stock information, and analysis into the user's excel workbook and categories based on which trade was a winning or losing trade.

### Nth Execution (2-n execution for a specific user):
1. Look for an excel file in the current working directory of the program named 'stocks_{username}.xlsx'.
2. Find the latest winning and losing entry in the workbook and compare the dates to find the most recent trade date.
3. Use BeautifulSoup to scrape trade data from a user's https://profit.ly/ account going back to the most recent trade date found from 'Step 2'.
4. Complete steps '5-7' from the 'First Execution' flow.

## Contributing
Pull requests are welcome. For major changes, please open an issue first to discuss what you would like to change. Currently, there are no contributors.

## License
[MIT](https://choosealicense.com/licenses/mit/)
