import logging

from ..tools.market_tools import MarketTools

logger = logging.getLogger(__name__)


class MarketAgent:

    def __init__(self, market_tools: MarketTools):
        logger.info("Initializing MarketAgent")

        self.market_tools = market_tools

    def analyze(self, ticker: str) -> dict:
        logger.info(
            "MarketAgent analyzing ticker=%s",
            ticker,
        )

        snapshot = self.market_tools.get_market_snapshot(
            ticker
        )

        return_1m = snapshot["return_1m"]
        return_1y = snapshot["return_1y"]

        if return_1m > 0 and return_1y > 0:
            trend = "bullish"

        elif return_1m < 0 and return_1y < 0:
            trend = "bearish"

        else:
            trend = "mixed"

        result = {
            "ticker": ticker,
            "price": snapshot["price"],
            "return_1d": snapshot["return_1d"],
            "return_1m": return_1m,
            "return_3m": snapshot["return_3m"],
            "return_1y": return_1y,
            "volatility": snapshot["volatility"],
            "average_volume": snapshot["average_volume"],
            "trend": trend,
        }

        logger.info(
            "MarketAgent completed ticker=%s trend=%s",
            ticker,
            trend,
        )

        return result