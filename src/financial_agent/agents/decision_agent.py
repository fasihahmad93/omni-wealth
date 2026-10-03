import logging
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

        if market.trend == "bullish":
            buy_signals += 1
            reasons.append("Price is above the 200-day moving average.")
        else:
            sell_signals += 1
            risks.append("Price is below the 200-day moving average.")

        if fundamental.business_quality == "strong":
            buy_signals += 1
            reasons.append("Fundamental quality is classified as strong.")
        elif fundamental.business_quality == "moderate":
            reasons.append("Fundamental quality is classified as moderate.")
        elif fundamental.business_quality == "not available":
            reasons.append("Fundamental quality could not be assessed because metrics are unavailable.")
        else:
            sell_signals += 1
            risks.append("Fundamental quality is classified as weak.")

        if news.sentiment == "positive":
            buy_signals += 1
            reasons.append("Recent demo news sentiment is positive.")
        elif news.sentiment == "negative":
            sell_signals += 1
            risks.append("Recent news sentiment is negative.")

        if valuation.valuation_view == "reasonable":
            buy_signals += 1
            reasons.append("Valuation is classified as reasonable.")
        elif valuation.valuation_view == "expensive":
            sell_signals += 1
            risks.append("Valuation is classified as expensive.")

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
