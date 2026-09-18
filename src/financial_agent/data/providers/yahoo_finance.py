import logging

import pandas as pd
import yfinance as yf

from .base import MarketDataProvider

logger = logging.getLogger(__name__)


class YahooFinanceMarketDataProvider(MarketDataProvider):

    def __init__(self, periods: int = 252):
        super().__init__()

        logger.info(
            "Initializing YahooFinanceMarketDataProvider periods=%s",
            periods,
        )

        if periods <= 0:
            raise ValueError("periods must be greater than zero")

        self.periods = periods

    def get_history(self, ticker: str) -> pd.DataFrame:
        logger.info(
            "Fetching Yahoo Finance historical data ticker=%s",
            ticker,
        )

        if not ticker:
            raise ValueError("ticker cannot be empty")

        try:
            data = yf.download(
                ticker,
                period="1y",
                interval="1d",
                auto_adjust=False,
                progress=False,
            )

            if data.empty:
                raise ValueError(
                    f"No market data returned for ticker={ticker}"
                )

            if isinstance(data.columns, pd.MultiIndex):
                data.columns = data.columns.get_level_values(0)

            data = data.rename(
                columns={
                    "Open": "open",
                    "High": "high",
                    "Low": "low",
                    "Close": "close",
                    "Adj Close": "adjusted_close",
                    "Volume": "volume",
                }
            )

            required_columns = [
                "open",
                "high",
                "low",
                "close",
                "volume",
            ]

            missing_columns = [
                column
                for column in required_columns
                if column not in data.columns
            ]

            if missing_columns:
                raise ValueError(
                    "Yahoo Finance response is missing columns=%s",
                    missing_columns,
                )

            data = data[
                [
                    "open",
                    "high",
                    "low",
                    "close",
                    "volume",
                ]
            ].copy()

            data = data.dropna()

            if data.empty:
                raise ValueError(
                    f"No valid historical data for ticker={ticker}"
                )

            data = data.tail(self.periods)

            logger.info(
                "Yahoo Finance data fetched ticker=%s rows=%s",
                ticker,
                len(data),
            )

            return data

        except Exception:
            logger.exception(
                "Failed to fetch Yahoo Finance data ticker=%s",
                ticker,
            )
            raise

    def get_price(self, ticker: str) -> float:
        logger.info(
            "Fetching Yahoo Finance price ticker=%s",
            ticker,
        )

        history = self.get_history(ticker)

        price = float(history["close"].iloc[-1])

        logger.info(
            "Yahoo Finance current price ticker=%s price=%.2f",
            ticker,
            price,
        )

        return price