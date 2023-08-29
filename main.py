import json
import pandas as pd
import pathlib
from datetime import date
from apis.yf_api import *
import plotly.express as px
import os
from dataclasses import asdict


# TODO classes interface for different stock info systems
def load_tickers_list(file_name: pathlib.Path) -> list[str]:
    tickers = []

    with open(file_name) as f:
        for line in f:
            tickers.append(line.strip())

    return tickers


def create_heatmap(tickers: list[TickerInfo]):
    df = pd.DataFrame({'ticker': [ticker.name for ticker in tickers],
                       'sector': [
                           '' if ticker.sector is None else ticker.sector for ticker in tickers
                       ],
                       'industry': [
                           '' if ticker.industry is None else ticker.industry for ticker in tickers
                       ],
                       'perc_delta': [ticker.perc_change for ticker in tickers],
                       'market_cap': [ticker.market_cap for ticker in tickers]
                       })

    color_scale = [
        [0, 'rgb(255, 0, 0)'],
        [0.5, 'rgb(66, 69, 83)'],
        [1, 'rgb(0, 154, 23)']
    ]

    fig = px.treemap(df, path=['sector', 'industry', 'ticker'], values='market_cap', color='perc_delta',
                     color_continuous_scale=color_scale,
                     color_continuous_midpoint=0,
                     hover_data={'perc_delta': ':.2p', 'market_cap': ':'})

    fig.update_layout(margin=dict(t=50, l=25, r=25, b=25))
    fig.show()


def get_ticker_from_cache(ticker: str, start_date: TimePoint, end_date: TimePoint) -> TickerInfo | None:
    cache_path = pathlib.Path(__file__).parent.resolve() / '__cache' / f'{ticker}.json'
    if cache_path.is_file():
        with open(cache_path) as f:
            data = json.load(f)
            key = f'{start_date.date} {start_date.event} {end_date.date} {end_date.event}'
            if key in data:
                return dict_to_ticker_info(data[key])
    return None


def save_tickers_to_cache(tickers: list[TickerInfo], start_date: TimePoint, end_date: TimePoint) -> None:
    cache_path = pathlib.Path(__file__).parent.resolve() / '__cache'
    if not os.path.isdir(cache_path):
        os.makedirs(cache_path)

    for ticker in tickers:
        filename = f'{ticker.name}.json'
        ticker_to_dict = {f'{start_date.date} {start_date.event} {end_date.date} {end_date.event}': asdict(ticker)}
        with open(cache_path / filename, 'w') as f:
            json.dump(ticker_to_dict, f, indent=4)


def main():
    # TODO: get companies from json for example
    # companies = ['AAPL', 'NVDA', 'AMD', 'HPQ', 'INTC', 'MSFT', 'META', 'GOOGL', 'NFLX', 'ORCL', 'IBM', 'CSCO', 'TRMB']
    # companies = ['AAPL']

    file_path = pathlib.Path(__file__).parent.resolve() / 'snp500_tickers.txt'
    companies = load_tickers_list(file_path)
    # print(companies)

    companies_to_load = []
    data = []
    start_date = TimePoint(date=date.today() + timedelta(days=-2), event='Open')
    end_date = TimePoint(date=date.today() + timedelta(days=-1), event='Open')

    for c in companies:
        ticker = get_ticker_from_cache(c, start_date, end_date)
        if ticker is None:
            companies_to_load.append(c)
        else:
            data.append(ticker)

    # TODO: not all days have data (like weekends or holidays) - handle it

    yf = YfinanceApi()
    loaded_data = yf.get_stock_data(companies_to_load, start_date, end_date)
    save_tickers_to_cache(loaded_data, start_date, end_date)

    create_heatmap(data)


if __name__ == "__main__":
    main()
