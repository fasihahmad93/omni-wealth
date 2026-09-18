import logging

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

        snapshot = {
            "ticker": ticker,
            "price": float(close.iloc[-1]),
            "return_1d": float(
                close.pct_change().iloc[-1]
            ),
            "return_1m": float(
                close.pct_change(21).iloc[-1]
            ),
            "return_3m": float(
                close.pct_change(63).iloc[-1]
            ),
            "return_1y": float(
                close.iloc[-1] / close.iloc[0] - 1
            ),
            "average_volume": float(
                history["volume"].mean()
            ),
            "volatility": float(
                close.pct_change().std()
            ),
        }

        logger.info(
            "Market snapshot completed ticker=%s",
            ticker,
        )

        return snapshot