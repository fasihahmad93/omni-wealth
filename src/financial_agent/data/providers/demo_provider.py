import logging

import numpy as np
import pandas as pd

from .base import MarketDataProvider

logger = logging.getLogger(__name__)


class DemoMarketDataProvider(MarketDataProvider):

    def __init__(self, periods: int = 252):
        super().__init__()

        logger.info(
            "Initializing DemoMarketDataProvider periods=%s",
            periods,
        )

        if periods <= 0:
            raise ValueError("periods must be greater than zero")

        self.periods = periods

    def get_history(self, ticker: str) -> pd.DataFrame:
        logger.info(
            "Fetching demo price history ticker=%s",
            ticker,
        )

        rng = np.random.default_rng(
            abs(hash(ticker)) % (2**32)
        )

        returns = rng.normal(
            0.0005,
            0.018,
            self.periods,
        )

        close = 100 * np.exp(
            np.cumsum(returns)
        )

        volume = rng.integers(
            900_000,
            2_000_000,
            self.periods,
        )

        return pd.DataFrame(
            {
                "open": close,
                "high": close * 1.01,
                "low": close * 0.99,
                "close": close,
                "volume": volume,
            }
        )

    def get_price(self, ticker: str) -> float:
        logger.info(
            "Fetching demo current price ticker=%s",
            ticker,
        )

        history = self.get_history(ticker)

        return float(history["close"].iloc[-1])