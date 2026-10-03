import logging

from ..tools.market_tools import MarketTools
from ..schemas.market import MarketAnalysis, MarketSnapshot

logger = logging.getLogger(__name__)


class MarketAgent:

    def __init__(self, market_tools: MarketTools):
        logger.info("Initializing MarketAgent")

        self.market_tools = market_tools

    def analyze(self, ticker: str) -> MarketAnalysis:
        logger.info(
            "MarketAgent analyzing ticker=%s",
            ticker,
        )

        snapshot = self.market_tools.get_market_snapshot(
            ticker
        )

        return_1m = snapshot["return_1m"]
        return_1y = snapshot["return_1y"]

        if return_1m is None or return_1y is None:
            trend = "not available"
        elif return_1m > 0 and return_1y > 0:
            trend = "bullish"

        elif return_1m < 0 and return_1y < 0:
            trend = "bearish"

        else:
            trend = "mixed"

        rsi = snapshot["rsi"]
        macd = snapshot["macd"]
        momentum = (
            "not available"
            if rsi is None or macd is None
            else "overbought"
            if rsi >= 70
            else "oversold"
            if rsi <= 30
            else "positive"
            if macd > 0
            else "negative"
            if macd < 0
            else "neutral"
        )
        volatility = snapshot["volatility"]
        volatility_regime = (
            "not available"
            if volatility is None
            else "high"
            if volatility >= 0.03
            else "normal"
        )
        signals = []
        if trend in {"bullish", "bearish"}:
            signals.append(f"Price returns indicate a {trend} trend.")
        if momentum in {"overbought", "oversold"}:
            signals.append(f"RSI indicates {momentum} momentum.")

        market_snapshot = MarketSnapshot(
            ticker=ticker,
            current_price=snapshot["current_price"],
            return_1m=return_1m,
            return_3m=snapshot["return_3m"],
            return_1y=return_1y,
            volume=snapshot["volume"],
            average_volume=snapshot["average_volume"],
            rsi=rsi,
            macd=macd,
            sma_50=snapshot["sma_50"],
            sma_200=snapshot["sma_200"],
            volatility=volatility,
        )
        result = MarketAnalysis(
            ticker=ticker,
            trend=trend,
            momentum=momentum,
            volatility_regime=volatility_regime,
            snapshot=market_snapshot,
            key_signals=signals,
        )

        logger.info(
            "MarketAgent completed ticker=%s trend=%s",
            ticker,
            trend,
        )

        return result