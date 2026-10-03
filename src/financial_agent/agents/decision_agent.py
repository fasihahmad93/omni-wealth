import logging
from collections.abc import Mapping

from financial_agent.schemas.decision import InvestmentDecision

logger = logging.getLogger(__name__)

class DecisionAgent:
    def __init__(self):
        logger.info("Initializing DecisionAgent")

    def decide(self, ticker, market, fundamental, news, valuation) -> InvestmentDecision:
        logger.info("DecisionAgent deciding ticker=%s", ticker)
        buy_signals = 0
        sell_signals = 0
        reasons = []
        risks = []

        market_trend = self._value(market, "trend")
        if market_trend == "bullish":
            buy_signals += 1
            reasons.append("Recent price returns indicate a bullish market trend.")
        elif market_trend == "bearish":
            sell_signals += 1
            risks.append("Recent price returns indicate a bearish market trend.")
        else:
            reasons.append("Market trend is mixed or unavailable; no directional signal counted.")

        business_quality = self._value(fundamental, "business_quality")
        if business_quality == "strong":
            buy_signals += 1
            reasons.append("Fundamental quality is classified as strong.")
        elif business_quality == "moderate":
            reasons.append("Fundamental quality is classified as moderate.")
        elif business_quality == "not available":
            reasons.append("Fundamental quality could not be assessed because metrics are unavailable.")
        elif business_quality == "weak":
            sell_signals += 1
            risks.append("Fundamental quality is classified as weak.")

        sentiment = self._value(news, "sentiment")
        if sentiment == "positive":
            buy_signals += 1
            reasons.append("Recent news sentiment is positive.")
        elif sentiment == "negative":
            sell_signals += 1
            risks.append("Recent news sentiment is negative.")
        elif sentiment == "not available":
            reasons.append("News sentiment is unavailable; no directional signal counted.")

        valuation_view = self._value(valuation, "valuation_view")
        if valuation_view == "reasonable":
            buy_signals += 1
            reasons.append("Valuation is classified as reasonable.")
        elif valuation_view == "expensive":
            sell_signals += 1
            risks.append("Valuation is classified as expensive.")
        elif valuation_view in {"elevated", "not available"}:
            reasons.append("Valuation is elevated or unavailable; no directional signal counted.")

        decision = "BUY" if buy_signals >= 3 and buy_signals > sell_signals else "SELL" if sell_signals >= 3 and sell_signals > buy_signals else "HOLD"
        thesis = f"Decision is based on {buy_signals} positive and {sell_signals} negative analytical signals."
        result = InvestmentDecision(
            ticker=ticker,
            decision=decision,
            thesis=thesis,
            key_reasons=reasons,
            risks=risks,
        )
        logger.info(
            "DecisionAgent output ticker=%s decision=%s buy_signals=%s sell_signals=%s key_reasons=%s risks=%s",
            ticker,
            result.decision,
            buy_signals,
            sell_signals,
            result.key_reasons,
            result.risks,
        )
        return result

    @staticmethod
    def _value(component, field: str):
        if isinstance(component, Mapping):
            return component.get(field)
        return getattr(component, field, None)
