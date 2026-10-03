import logging

import pandas as pd

from ..analytics.technical import (
    calculate_macd,
    calculate_rsi,
    calculate_volatility,
)
from ..data.providers.base import MarketDataProvider

logger = logging.getLogger(__name__)


class MarketTools:

    def __init__(self, provider: MarketDataProvider):
        logger.info(
            "Initializing MarketTools provider=%s",
            provider.__class__.__name__,
        )

        self.provider = provider

    def get_price(self, ticker: str) -> float:
        logger.info(
            "MarketTools.get_price ticker=%s",
            ticker,
        )

        price = self.provider.get_price(ticker)

        logger.info(
            "MarketTools.get_price completed ticker=%s price=%.2f",
            ticker,
            price,
        )

        return price

    def get_market_snapshot(self, ticker: str) -> dict:
        logger.info(
            "MarketTools.get_market_snapshot ticker=%s",
            ticker,
        )

        history = self.provider.get_history(ticker)

        close = history["close"]
        current_price = float(close.iloc[-1])

        def period_return(period: int) -> float | None:
            if len(close) <= period:
                return None
            value = close.pct_change(period).iloc[-1]
            return float(value) if pd.notna(value) else None

        rsi = calculate_rsi(close) if len(close) > 14 else None
        macd = calculate_macd(close) if len(close) else None
        volatility = calculate_volatility(close) if len(close) > 20 else None
        sma_50 = float(close.tail(50).mean()) if len(close) >= 50 else None
        sma_200 = float(close.tail(200).mean()) if len(close) >= 200 else None

        snapshot = {
            "ticker": ticker,
            "price": current_price,
            "current_price": current_price,
            "return_1d": period_return(1),
            "return_1m": period_return(21),
            "return_3m": period_return(63),
            "return_1y": (
                float(current_price / close.iloc[0] - 1)
                if len(close) > 1
                else None
            ),
            "volume": float(history["volume"].iloc[-1]),
            "average_volume": float(
                history["volume"].mean()
            ),
            "rsi": rsi,
            "macd": macd,
            "sma_50": sma_50,
            "sma_200": sma_200,
            "volatility": volatility,
        }

        logger.info(
            "Market snapshot completed ticker=%s",
            ticker,
        )

        return snapshot