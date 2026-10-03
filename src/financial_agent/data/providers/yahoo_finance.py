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

    def get_valuation_metrics(self, ticker: str) -> dict[str, float | None]:
        logger.info("Fetching Yahoo Finance valuation metrics ticker=%s", ticker)
        if not ticker or not ticker.strip():
            raise ValueError("ticker cannot be empty")

        info = yf.Ticker(ticker.strip().upper()).info or {}

        def as_float(value) -> float | None:
            try:
                return float(value) if value is not None else None
            except (TypeError, ValueError):
                return None

        metrics = {
            "pe": as_float(info.get("trailingPE")),
            "forward_pe": as_float(info.get("forwardPE")),
            "ev_ebitda": as_float(info.get("enterpriseToEbitda")),
            "beta": as_float(info.get("beta")),
            "sector_pe": as_float(info.get("sectorTrailingPE")),
        }
        logger.info(
            "Yahoo Finance valuation metrics fetched ticker=%s available=%s",
            ticker,
            [name for name, value in metrics.items() if value is not None],
        )
        return metrics