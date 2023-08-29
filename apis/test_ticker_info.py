import unittest
from ticker_info import TickerInfo
from dataclasses import asdict


class TestCase(unittest.TestCase):
    def test_todict(self):
        ticker = TickerInfo(
            name='AAPL',
            sector='IT',
            industry='42',
            price_start=10,
            price_end=15,
            perc_change=-1.5,
            market_cap=100500
        )

        d = asdict(ticker)

        self.assertEqual(d['name'], 'AAPL')


if __name__ == '__main__':
    unittest.main()
