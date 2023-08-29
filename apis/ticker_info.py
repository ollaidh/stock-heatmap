from dataclasses import dataclass
import datetime
from typing import Any


# store info for one ticker:
@dataclass(kw_only=True)
class TickerInfo:
    name: str  # ticker name
    sector: str  # sector of industry
    industry: str  # industry
    price_start: float
    price_end: float
    perc_change: float  # % difference between close-open stock price for "day" date
    market_cap: float  # market capacity for the ticker


@dataclass(kw_only=True)
class TimePoint:
    date: datetime.date
    event: str

    def __post_init__(self):
        valid_times = {'Open', 'Close', 'High', 'Low'}
        if self.event not in valid_times:
            raise ValueError(f'{self.event} is not a valid time point! Valid are: {valid_times}.')


def dict_to_ticker_info(ticker_data: dict[str, Any]) -> TickerInfo:
    return TickerInfo(
        name=ticker_data['name'],
        sector=ticker_data['sector'],
        industry=ticker_data['industry'],
        price_start=ticker_data['price_start'],
        price_end=ticker_data['price_end'],
        perc_change=ticker_data['perc_change'],
        market_cap=ticker_data['market_cap']
    )


