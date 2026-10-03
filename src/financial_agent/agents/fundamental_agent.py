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
        growth = (
            classify_growth(snapshot.revenue_growth, snapshot.earnings_growth)
            if snapshot.revenue_growth is not None and snapshot.earnings_growth is not None
            else "not available"
        )
        profitability = (
            classify_profitability(snapshot.roe, snapshot.roce)
            if snapshot.roe is not None and snapshot.roce is not None
            else "not available"
        )
        balance = (
            classify_balance_sheet(snapshot.debt_to_equity)
            if snapshot.debt_to_equity is not None
            else "not available"
        )
        cash_flow = (
            "not available"
            if snapshot.free_cash_flow is None or snapshot.operating_cash_flow is None
            else "strong"
            if snapshot.free_cash_flow > 0 and snapshot.operating_cash_flow > 0
            else "weak"
        )
        quality = (
            "not available"
            if "not available" in {growth, profitability, balance}
            else "strong"
            if growth == "strong" and profitability == "strong" and balance == "healthy"
            else "moderate"
        )
        strengths = []
        if snapshot.revenue_growth is not None and snapshot.revenue_growth > 0:
            strengths.append("Positive revenue growth")
        if snapshot.earnings_growth is not None and snapshot.earnings_growth > 0:
            strengths.append("Positive earnings growth")
        if snapshot.free_cash_flow is not None and snapshot.free_cash_flow > 0:
            strengths.append("Positive free cash flow")
        result = FundamentalAnalysis(
            ticker=ticker,
            business_quality=quality,
            growth=growth,
            profitability=profitability,
            balance_sheet=balance,
            cash_flow=cash_flow,
            snapshot=snapshot,
            strengths=strengths,
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
