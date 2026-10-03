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
        try:
            metrics = self.market_provider.get_valuation_metrics(ticker)
        except Exception:
            logger.exception("Valuation metrics unavailable ticker=%s", ticker)
            metrics = {}

        pe = metrics.get("pe")
        forward_pe = metrics.get("forward_pe")
        sector_pe = metrics.get("sector_pe")
        valuation_view = (
            classify_valuation(pe, forward_pe, sector_pe)
            if pe is not None and forward_pe is not None and sector_pe is not None
            else "not available"
        )
        return {
            "ticker": ticker,
            "pe": pe,
            "forward_pe": forward_pe,
            "ev_ebitda": metrics.get("ev_ebitda"),
            "beta": metrics.get("beta"),
            "max_drawdown": calculate_drawdown(prices),
            "valuation_view": valuation_view,
        }
