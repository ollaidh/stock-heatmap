import sys

import yfinance
from datetime import timedelta
from apis.ticker_info import *
import time


class YfinanceApi:
    # browse stock data and ticker data for all tickers from polygon.io, save as TickerInfo object for each ticker
    def get_stock_data(self, companies: list[str], start_date: TimePoint, end_date: TimePoint) -> list[TickerInfo]:
        result = []
        # print(start_date, end_date)
        all_tickers = yfinance.Tickers(' '.join(companies))
        for company in companies:
            ticker = all_tickers.tickers[company]
            ticker_history = ticker.history(start=start_date.date, end=end_date.date + timedelta(days=1))
            # print(ticker_history.to_string())
            if ticker_history[start_date.event].empty or ticker_history[end_date.event].empty:
                print(f'No data for ticker {company}', file=sys.stderr)
                continue
            price_start = ticker_history[start_date.event][0]
            price_end = ticker_history[end_date.event][-1]
            percentage_change = (price_end - price_start) / price_start
            result.append(TickerInfo(
                name=company,
                sector=ticker.info.get('sector'),
                industry=ticker.info.get('industry'),
                price_start=price_start,
                price_end=price_end,
                perc_change=percentage_change,
                market_cap=ticker.info['marketCap']
            ))
            print(f'{company} OK')
            time.sleep(0.5)
        # print(result)
        return result
