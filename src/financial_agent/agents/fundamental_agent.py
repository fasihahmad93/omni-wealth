import logging
from financial_agent.analytics.fundamentals import classify_growth, classify_balance_sheet, classify_profitability
from financial_agent.schemas.fundamentals import FundamentalAnalysis, FundamentalSnapshot

logger = logging.getLogger(__name__)

class FundamentalAgent:
    def __init__(self, tools):
        logger.info("Initializing FundamentalAgent")
        self.tools = tools

    def analyze(self, ticker: str) -> FundamentalAnalysis:
        logger.info("FundamentalAgent analyzing ticker=%s", ticker)
        raw = self.tools.get_fundamentals(ticker)
        snapshot = FundamentalSnapshot(ticker=ticker, **raw)
        growth = classify_growth(snapshot.revenue_growth, snapshot.earnings_growth)
        profitability = classify_profitability(snapshot.roe, snapshot.roce)
        balance = classify_balance_sheet(snapshot.debt_to_equity)
        cash_flow = "strong" if snapshot.free_cash_flow > 0 and snapshot.operating_cash_flow > 0 else "weak"
        quality = "strong" if growth == "strong" and profitability == "strong" and balance == "healthy" else "moderate"
        result = FundamentalAnalysis(
            ticker=ticker,
            business_quality=quality,
            growth=growth,
            profitability=profitability,
            balance_sheet=balance,
            cash_flow=cash_flow,
            snapshot=snapshot,
            strengths=["Positive earnings growth", "Positive free cash flow"],
            risks=["Growth and margins can change with the economic cycle"],
        )
        logger.info(
            "FundamentalAgent output ticker=%s quality=%s growth=%s profitability=%s balance_sheet=%s cash_flow=%s",
            ticker,
            result.business_quality,
            result.growth,
            result.profitability,
            result.balance_sheet,
            result.cash_flow,
        )
        return result
