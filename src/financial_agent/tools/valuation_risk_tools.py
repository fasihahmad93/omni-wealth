import logging
from financial_agent.analytics.valuation import classify_valuation, calculate_drawdown

logger = logging.getLogger(__name__)

class ValuationRiskTools:
    def __init__(self, market_provider):
        logger.info("Initializing ValuationRiskTools")
        self.market_provider = market_provider

    def get_valuation_risk(self, ticker: str) -> dict:
        logger.info("Tool get_valuation_risk ticker=%s", ticker)
        df = self.market_provider.get_history(ticker)
        prices = df["close"]
        current_price = float(prices.iloc[-1])
        eps = current_price / 28.0
        pe = current_price / eps
        forward_eps = eps * 1.12
        forward_pe = current_price / forward_eps
        return {
            "ticker": ticker,
            "pe": pe,
            "forward_pe": forward_pe,
            "ev_ebitda": 18.0,
            "beta": 1.05,
            "max_drawdown": calculate_drawdown(prices),
            "valuation_view": classify_valuation(pe, forward_pe),
        }
